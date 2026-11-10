# Final-project orchestrator audit

Fetch the final-project attempt exports from CMP, normalize GitHub repository
URLs, scan archives at submitted commits using authenticated `gh`, and write a
CSV with executable evidence and separate weak documentation mentions. Archives
are read without extracting files or executing any project code.

Requirements: Python 3.10+, `gh` authenticated on the host, and the CMP staff
`AUTH_TOKEN`. No Python dependencies are required. Output must be outside git.

```bash
set -a
. /path/to/cmp/.env
set +a
python3 scripts/dez-orchestrators/analyze.py fetch --output /absolute/private/report-dir
python3 scripts/dez-orchestrators/analyze.py scan --output /absolute/private/report-dir --workers 4
python3 -m unittest discover -s scripts/dez-orchestrators -p 'test_*.py'
```

CMP's course endpoint determines final-project attempt slugs; midterms are
excluded. The export endpoint returns a `submissions` array without pagination.
Fetch retains only identifiers needed for deduplication, repository URLs, commits,
and scores in an owner-only cache; student emails are discarded. Repositories
are grouped case-insensitively per year across all final-project attempts.
The latest attempt/row determines the scanned commit. Raw submission totals and
student totals must be reported separately from distinct-repository counts.

The detector recognizes Kestra, Airflow, Astronomer, Dagster, Prefect, Mage,
Luigi, Argo Workflows, Step Functions, Data Factory, Flyte, Temporal, Hamilton,
and Databricks Workflows. Multiple labels may coexist; Astronomer also implies
Airflow. Documentation mentions are weak evidence and do not establish use.
Explicit tree/blob URLs restrict evidence to the submitted project path, while
common homework/module paths are excluded from whole-repository matches.
Manually review ambiguous course repositories, weak mentions, and custom schedulers
before publishing conclusions. `none` means no executable evidence detected;
`unknown` means unavailable/unscannable, including invalid URLs. These are static
source observations, not proof a pipeline ran or that a project is production ready.

Only text/config files up to 2 MB are read, up to 60 MB text per repository;
archives above 150 MB are rejected after download. Dependencies, binary data,
lockfiles and environments are excluded. A failed submitted commit stays
`unknown`; the script never silently substitutes today's default branch. A missing
or malformed commit uses the default archive and is visible in `commit_id`.
Caches make reruns inexpensive. Delete the relevant `cache/scans/*.json` to retry
access failures after correcting the source. Use low concurrency and inspect
`gh api rate_limit` before and during large runs. GitHub rate-limit failures remain
explicit in the CSV and must be retried after reset before claiming full coverage.

For enrichment, read public GitHub profiles and public web/LinkedIn first. Read
Treg's current catalog parameters and cost, calculate the entire remaining author
estimate before any billable calls, and refuse estimates over $10. The optional
`enrich.py` helper reads the owner-only `/tmp/treg-api-key` file populated by
`dataops secrets get treg --field api_key --out /tmp/treg-api-key`. It uses a
per-call reservation header, a persistent micro-USD ledger and idempotency keys;
an unsettled charge blocks further spending until reconciled. Catalog discovery
is separate and must precede calls. Never use private CMP emails for enrichment.
Store result files, employer data, reports, cache, and ledger outside git.

After scanning, use `review.py --output DIR` to fetch candidate configuration
files for additional frameworks and scheduled pipelines, and `recover.py --output
DIR` to inspect source/configuration through the tree API when an archive exceeds
limits. Rerun `analyze.py scan` after these helpers finish to rebuild the scoped
CSV. These helpers modify only the external cache. Scheduler labels (GitHub
Actions, Google Cloud Scheduler and AWS EventBridge) are reported separately from
workflow frameworks; normal CI without a scheduled data job does not count.
Bruin pipeline definitions follow https://getbruin.com/docs/bruin/pipelines/definition.html.

Curate `shortlist.json` outside git with 10–20 objects containing `repo`, `year`
and `why`. Write `enrichment.csv` with `author`, `GitHub`, `employer`, `source`
(public or treg), `source_url`, `bio` and `notes`. Render reconciled summary and
shortlist reports with `python3 scripts/dez-orchestrators/report.py --output DIR`.
The renderer verifies that CSV submission row counts reconcile with all exports.
Review all reports manually, including private/public identity conflicts, before
using them in a pitch. Emit the Treg usage narrative from the actual ledger,
never from quoted provider prices alone.

> Superseded for new research by the course-agnostic pipeline in [scripts/course-audience](../course-audience/README.md) (configurable tool sets, identity linking, budget-guarded enrichment, audience aggregates).
