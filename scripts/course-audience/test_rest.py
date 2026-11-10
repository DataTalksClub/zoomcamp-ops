import json
from pathlib import Path
import tempfile
import unittest

from rest import improve, role_claim, safe
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
