import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from scan import load_toolsets, detect, apply_implies, relevant, repo_name  # noqa: E402
from identities import domain_kind, linkedin_ids, x_ids  # noqa: E402
from classify import seniority, role_family, role_timing, parse_date, country_of, corroborate, FREELANCE_RE  # noqa: E402
from cmp_fetch import email_domain  # noqa: E402
from treg_budget import Ledger, BudgetExceeded  # noqa: E402
from aggregate import aggregate  # noqa: E402
from classify import FIELDS  # noqa: E402
from treg_enrich import candidate_slugs, profile_slug  # noqa: E402

TOOLS = HERE / 'tools'


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.orch, self.wh = load_toolsets([TOOLS / 'orchestrators.json', TOOLS / 'warehouses.json'])

    def test_warehouses_detected_from_code_and_deps(self):
        files = [('load.py', 'import snowflake.connector\nfrom google.cloud import bigquery\n'),
                 ('requirements.txt', 'dbt-databricks==1.8\nduckdb>=1.0\n'),
                 ('dbt/profiles.yml', 'dev:\n  outputs:\n    prod:\n      type: redshift\n')]
        ev, _ = detect(files, self.wh)
        self.assertEqual({'Snowflake', 'BigQuery', 'Databricks', 'DuckDB', 'Redshift'}, set(ev))

    def test_vendored_dbt_packages_and_docs_do_not_count(self):
        files = [('dbt/dbt_packages/dbt_utils/integration_tests/ci/sample.profiles.yml', 'type: snowflake'),
                 ('README.md', 'We load data into Snowflake'),
                 ('notes.py', '# data comes from Snowflake later')]
        ev, weak = detect(files, self.wh)
        self.assertEqual({}, ev)
        self.assertTrue(any('README.md' in w for w in weak))

    def test_astronomer_implies_airflow_and_homework_paths_excluded(self):
        ev, _ = detect([('Dockerfile', 'FROM quay.io/astronomer/astro-runtime:12'), ('02-workflow-orchestration/flow.yml', 'type: io.kestra.core.tasks.log.Log')], self.orch)
        ev = {k: [e for e in v if relevant(e, '')] for k, v in ev.items()}
        ev = apply_implies({k: v for k, v in ev.items() if v}, self.orch)
        self.assertEqual({'Astronomer', 'Airflow'}, set(ev))

    def test_repo_name(self):
        self.assertEqual('a/b', repo_name('https://github.com/a/b.git'))
        self.assertEqual('a/b', repo_name('https://github.com/a/b/tree/main/project'))
        self.assertEqual('', repo_name('https://gitlab.com/a/b'))


class IdentityTests(unittest.TestCase):
    def test_email_reduced_to_domain(self):
        self.assertEqual('acme.com', email_domain('Jane.Doe@ACME.com'))
        self.assertEqual('', email_domain(None))

    def test_domain_kinds(self):
        self.assertEqual('free', domain_kind('gmail.com'))
        self.assertEqual('academic', domain_kind('student.uni-example.ac.uk'))
        self.assertEqual('academic', domain_kind('mit.edu'))
        self.assertEqual('corporate', domain_kind('accenture.com'))

    def test_linkedin_ids_from_posts_and_profiles(self):
        ids = linkedin_ids(['https://www.linkedin.com/posts/jane-doe-123_dezoomcamp-activity-1-x',
                            'https://linkedin.com/in/Jane-Doe-123/', 'https://www.linkedin.com/feed/update/urn:li:activity:1'])
        self.assertEqual({'jane-doe-123': 2}, dict(ids))
        self.assertEqual({'jdoe': 1}, dict(x_ids(['https://x.com/jdoe/status/1'])))


class ClassifyTests(unittest.TestCase):
    def test_seniority_and_family(self):
        self.assertEqual('senior', seniority('Senior Data Engineer', ''))
        self.assertEqual('lead+', seniority('Head of Data', ''))
        self.assertEqual('student', seniority('MSc Student', ''))
        self.assertEqual('job seeker', seniority('', 'Open to work | aspiring data engineer', True, False))
        self.assertEqual('analytics eng', role_family('Analytics Engineer'))
        self.assertEqual('DE', role_family('Data Platform Engineer'))
        self.assertEqual('DA', role_family('BI Analyst'))
        self.assertTrue(FREELANCE_RE.search('Freelance Data Engineer'))
        self.assertTrue(FREELANCE_RE.search('Independent Data Consultant'))

    def test_timing(self):
        self.assertEqual('after course', role_timing(parse_date('Jun 2026'), 2026))
        self.assertEqual('before course', role_timing(parse_date('2023'), 2026))
        self.assertEqual('during course', role_timing(parse_date('Feb 2026'), 2026))
        self.assertIsNone(parse_date('Present'))

    def test_country_aliases(self):
        self.assertEqual('United States', country_of('Austin, TX'))
        self.assertEqual('Germany', country_of('Berlin, Germany'))

    def test_name_match_needs_corroboration(self):
        author = {'github_profile': {'location': 'Berlin, Germany', 'company': ''}, 'email_domain': ''}
        self.assertEqual('low', corroborate(author, {'headline': 'Baker', 'location': 'Paris, France'})[0])
        self.assertEqual('medium', corroborate(author, {'headline': 'Data Engineer', 'location': 'Berlin, Germany'})[0])


class CandidateTests(unittest.TestCase):
    def test_language_suffixes_deduplicate_before_candidate_limit(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'cache').mkdir()
            (p / 'cache' / 'li-search-jane-doe.json').write_text(json.dumps({'rows': [
                {'name': 'Jane Doe', 'profile_id': s}
                for s in ['jane-doe/en', '../bad', 'jane-doe/fr', 'jane-doe-2']
            ]}))
            author = {'self_submitted_linkedin': [], 'github_declared_linkedin': [],
                      'github_profile': {'name': 'Jane Doe'}}
            self.assertEqual(['jane-doe', 'jane-doe-2'], candidate_slugs(p, author))

    def test_encoded_identifiers_remain_safe_cache_names(self):
        self.assertEqual('%c5%82ukasz-doe', profile_slug('%C5%82ukasz-doe/en'))
        self.assertEqual('', profile_slug('../escape'))
        self.assertEqual('', profile_slug('bad%zz'))


class AggregateTests(unittest.TestCase):
    def test_country_uses_only_enriched_unflagged_authors(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            with (p / 'enrichment-all.csv').open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                for confidence, enriched, flag, country in [
                    ('high', 'yes', '', 'Germany'),
                    ('none', '', '', 'France'),
                    ('low', '', 'low-confidence', 'Spain'),
                    ('rejected', '', 'rejected', 'Italy'),
                ]:
                    row = dict.fromkeys(FIELDS, '')
                    row.update(confidence=confidence, enriched=enriched, flag=flag,
                               country=country, years='2025', seniority='unknown', role_family='unknown')
                    writer.writerow(row)
            with patch('aggregate.warehouse_summary', return_value=([], {}, {})):
                aggregate(p, ['Airflow', 'Astronomer'])
            stats = json.loads((p / 'audience-stats.json').read_text())
            self.assertEqual([['Germany', 1]], stats['countries_top'])
            self.assertEqual(1, stats['enriched'])


class BudgetTests(unittest.TestCase):
    def test_reservation_past_stop_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'cache').mkdir()
            (p / 'treg-ledger.json').write_text(json.dumps([{'request_id': 'x', 'charged_micro': 8_999_000}]))
            led = Ledger(p, 10, 9)
            with self.assertRaises(BudgetExceeded):
                led.reserve('t', {}, 0.0042)

    def test_unsettled_blocks_spend(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'cache').mkdir()
            (p / 'treg-ledger.json').write_text(json.dumps([{'request_id': 'x', 'charged_micro': None}]))
            with self.assertRaisesRegex(BudgetExceeded, 'Unsettled'):
                Ledger(p, 10, 9).reserve('t', {}, 0.001)

    def test_second_process_is_locked_out(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'cache').mkdir()
            first = Ledger(p, 10, 9)  # noqa: F841 (holds the lock)
            with self.assertRaisesRegex(BudgetExceeded, 'lock'):
                Ledger(p, 10, 9)


if __name__ == '__main__':
    unittest.main()
