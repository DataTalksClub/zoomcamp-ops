import json
from pathlib import Path
import tempfile
import unittest

from rest import improve, role_claim, safe, redact, apply_reviewed, merge
import csv
from unittest.mock import patch
from employers import analyze
from classify import FIELDS


class PublicAuditTests(unittest.TestCase):
    def test_project_topics_and_seeking_roles_are_not_current_occupation(self):
        self.assertEqual('', role_claim('This project trains data engineers.'))
        self.assertEqual('', role_claim("I'm currently looking for opportunities as Software Engineer."))
        self.assertEqual('', role_claim('I was a Data Engineer at Example.'))
        self.assertEqual('Data Engineer', role_claim("I'm a **Data Engineer** working on pipelines."))

    def test_flagged_identity_and_historical_domain_cannot_become_employment(self):
        row=dict.fromkeys(FIELDS,'');row.update(confidence='none',seniority='unknown')
        evidence={'sources':[], 'commit_domains':[{'domain':'example.com','kind':'corporate'}]}
        out=improve(row,evidence)
        self.assertEqual('',out['company']);self.assertEqual('none',out['confidence'])
        row.update(flag='rejected',confidence='rejected')
        evidence['sources']=[{'kind':'github_profile','url':'https://github.com/test','text':'Data Engineer'}]
        self.assertEqual(row,improve(row,evidence))

    def test_reviewed_own_source_can_replace_flag_without_confirming_candidate(self):
        row=dict.fromkeys(FIELDS,'');row.update(confidence='rejected',flag='rejected')
        evidence={'sources':[{'kind':'profile_readme','url':'https://github.com/a/a','text':'Data Engineer | Graduate'}]}
        fact={'kind':'profile_readme','quote':'Data Engineer | Graduate','title':'Data Engineer'}
        result=apply_reviewed(row,evidence,fact)
        self.assertEqual('high',result['confidence']);self.assertEqual('',result['flag'])
        self.assertEqual('',result['company'])
        self.assertIn('candidate remains unconfirmed',result['notes'])
        with self.assertRaises(AssertionError):
            apply_reviewed(row,evidence,dict(fact,quote='Invented company'))

    def test_redaction_preserves_json_escapes(self):
        data={'text':'A line\nname@example.com', 'list':['other@example.com']}
        encoded=json.dumps(redact(data))
        self.assertEqual({'text':'A line\n[address removed]','list':['[address removed]']},json.loads(encoded))

    def test_merge_preserves_accepted_predecessor_and_excludes_flagged_rows(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'cache/rest').mkdir(parents=True)
            original=[];audit=[];authors=[]
            for n in range(3):
                row=dict.fromkeys(FIELDS,'');row.update(student_key=f'cmp-{n}',github=f'user{n}',confidence='none',seniority='unknown')
                if n==0:row.update(company='Original',enriched='yes',confidence='high')
                original.append(row);new=dict(row,title='Data Engineer',enriched='yes',confidence='high',audit_sources='1',audit_checks='')
                if n==2:new['flag']='rejected'
                audit.append(new);authors.append({'student_id':n,'github_profile':{}})
            (p/'cache/authors.json').write_text(json.dumps(authors))
            for filename,rows,fields in [('enrichment-all.csv',original,FIELDS),('enrichment-rest.csv',audit,FIELDS+['audit_sources','audit_checks'])]:
                with (p/filename).open('w',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
            with patch('aggregate.aggregate'),patch('employers.append',return_value={'enriched_authors':2}),patch('builtins.print'):
                merge(p,99999999)
            with (p/'enrichment-all.csv').open() as f:
                rows=list(csv.DictReader(f))
            self.assertEqual('Original',rows[0]['company']);self.assertEqual('',rows[0]['title'])
            self.assertEqual('Data Engineer',rows[1]['title']);self.assertEqual('',rows[2]['enriched'])

    def test_no_email_leaves_source_redaction(self):
        self.assertEqual('Contact [address removed]',safe('Contact name@example.com'))


class EmployerTests(unittest.TestCase):
    def test_unknowns_and_domain_only_do_not_inflate_enterprise_share(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'company-metadata.json').write_text(json.dumps({'example':{'industry':'Software / cloud','segment':'enterprise','size':'large','sources':['https://example.com/about']},'unsourced':{'segment':'startup'}}))
            def row(c,e='github_profile',free=''):
                return dict(company=c,evidence_type=e,notes='',freelance=free)
            result=analyze(p,[row('Example'),row('Unknown'),row('Unsourced'),row('Domain','domain_signal'),row('Independent',free='freelance')])
            self.assertEqual(3,result['authors_with_named_employer'])
            self.assertEqual(1,result['domain_only_excluded'])
            self.assertEqual({'enterprise':1,'unknown':2},result['segment'])
            self.assertEqual(33.3,result['segment_share_of_named_employer_pct']['enterprise'])
            self.assertEqual(20.0,result['segment_share_of_enriched_pct']['enterprise'])
