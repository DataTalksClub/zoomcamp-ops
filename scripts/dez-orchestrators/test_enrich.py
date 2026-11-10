import json
from pathlib import Path
import tempfile
import unittest
from enrich import call

class BudgetTests(unittest.TestCase):
    def test_over_cap_is_refused_before_loading_key(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'treg-ledger.json').write_text(json.dumps([{'charged_micro':9_950_000}]))
            with self.assertRaisesRegex(ValueError,'exceed'):
                call(p,'unused',{},0.1)

    def test_unknown_charge_blocks_more_spend(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'treg-ledger.json').write_text(json.dumps([{'charged_micro':None}]))
            with self.assertRaisesRegex(ValueError,'Unsettled'):
                call(p,'unused',{},0.001)

if __name__=='__main__':unittest.main()
