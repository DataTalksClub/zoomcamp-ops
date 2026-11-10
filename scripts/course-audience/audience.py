#!/usr/bin/env python3
"""Course-agnostic final-project audience pipeline. See README.md for the runbook.

  audience.py fetch      --course de-zoomcamp --years 2025 2026 --output DIR
  audience.py scan       --output DIR --toolsets tools/orchestrators.json tools/warehouses.json
  audience.py profiles   --course de-zoomcamp --years 2025 2026 --output DIR  (opt-in public CMP profiles)
  audience.py identities --output DIR            (CMP + public GitHub identity evidence)
  audience.py recheck    --output DIR            (re-check rejected candidates; needs recheck-candidates.json)
  audience.py linkedin   --output DIR --cap-usd 10 --stop-usd 9   (Treg, budget-guarded)
  audience.py github-linkedin --output DIR       (Treg name search for authors without any LinkedIn link)
  audience.py candidate-profiles --output DIR    (read up to 2 name-matching candidates to look for a linking fact)
  audience.py reconcile  --output DIR            (settle calls interrupted mid-flight via idempotent replay)
  audience.py classify   --output DIR            (writes enrichment-all.csv)
  audience.py aggregate  --output DIR            (writes audience-summary.md)
  audience.py homework   --output DIR            (per-homework unique submitters)
"""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('action', choices=['fetch', 'scan', 'identities', 'profiles', 'recheck', 'linkedin', 'github-linkedin', 'candidate-profiles', 'reconcile', 'classify', 'aggregate', 'homework'])
    p.add_argument('--output', type=Path, required=True, help='Private report directory outside git')
    p.add_argument('--course', help='Course family slug, e.g. de-zoomcamp, ml-zoomcamp, llm-zoomcamp')
    p.add_argument('--years', nargs='+', default=[])
    p.add_argument('--toolsets', nargs='+', default=[str(HERE / 'tools' / 'orchestrators.json')])
    p.add_argument('--workers', type=int, default=6)
    p.add_argument('--cap-usd', type=float, default=10.0)
    p.add_argument('--stop-usd', type=float, default=9.0)
    p.add_argument('--limit', type=int, default=0, help='Max Treg lookups in this run (0 = budget-bound only)')
    p.add_argument('--dry-run', action='store_true', help='Print the Treg estimate and stop')
    p.add_argument('--hide-labels', nargs='*', default=[], help='Tool labels to keep out of the audience summary (sponsor sensitivity)')
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    if a.action == 'fetch':
        from cmp_fetch import fetch
        print(json.dumps(fetch(a.output, a.course, a.years), indent=2))
    elif a.action == 'scan':
        from scan import scan
        print(json.dumps(scan(a.output, a.toolsets, a.workers), indent=2))
    elif a.action == 'profiles':
        from cmp_profiles import crawl
        print(len(crawl(a.output, a.course, a.years)))
    elif a.action == 'recheck':
        from rechecks import recheck
        print(json.dumps(recheck(a.output), indent=2))
    elif a.action == 'identities':
        from identities import build
        print(json.dumps(build(a.output), indent=2))
    elif a.action == 'linkedin':
        from treg_enrich import linkedin_profiles
        print(json.dumps(linkedin_profiles(a.output, a.cap_usd, a.stop_usd, a.limit, a.dry_run, a.workers), indent=2))
    elif a.action == 'github-linkedin':
        from treg_enrich import github_to_linkedin
        print(json.dumps(github_to_linkedin(a.output, a.cap_usd, a.stop_usd, a.limit, a.dry_run, a.workers), indent=2))
    elif a.action == 'candidate-profiles':
        from treg_enrich import candidate_profiles
        print(json.dumps(candidate_profiles(a.output, a.cap_usd, a.stop_usd, a.limit, a.dry_run, a.workers), indent=2))
    elif a.action == 'reconcile':
        from treg_budget import Ledger
        print(json.dumps(Ledger(a.output, a.cap_usd, a.stop_usd).reconcile(), indent=2))
    elif a.action == 'classify':
        from classify import classify_all
        print(json.dumps(classify_all(a.output), indent=2))
    elif a.action == 'aggregate':
        from aggregate import aggregate
        print(aggregate(a.output, a.hide_labels))
    elif a.action == 'homework':
        from aggregate import homework_counts
        print(json.dumps(homework_counts(a.output), indent=2))


if __name__ == '__main__':
    main()
