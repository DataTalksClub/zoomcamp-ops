# Course final-project audience pipeline (course-agnostic runbook)

Repeatable research for sponsor case studies: who builds the final projects of a
DataTalksClub course, where they work, and which tools their projects use. Works for
any CMP course family (`de-zoomcamp`, `ml-zoomcamp`, `mlops-zoomcamp`, `llm-zoomcamp`,
`ai-dev-tools`, ...) and any set of cohort years. First used for the DE Zoomcamp 2025+2026
Astronomer (module 2, orchestration) and Snowflake (module 3, data warehouse) pitches.

Everything this pipeline writes is **private student data**. Keep the output directory
outside git (for example `~/tmp/agent-reports/<date>-<course>-audience/`, mode 700). The
repository `.gitignore` also blocks the usual names (`enrichment*.csv`, `*-unique-submitters.csv`,
`audience-*`, `treg-ledger.json`, `cache/`). Never commit outputs, caches or the ledger.

## Requirements

- Python 3.10+; no required dependencies. Optional: `geonamescache` for city -> country
  (`uv venv .venv && uv pip install --python .venv/bin/python geonamescache`).
- `gh` authenticated (repository archives, public GitHub profiles, commit authors).
  One full run uses about 2 core API calls per author plus one per repository; the quota is
  shared with every other session of the account, so check `gh api rate_limit` first. Scans
  wait and retry on rate-limit errors and never cache them.
- CMP staff token: `set -a; . ~/git/course-management-agent/.env; set +a` (never print it).
- Treg key, only for paid steps: `dataops secrets get treg --field api_key --out /tmp/treg-api-key`
  (mode 600, delete after the run) and the Treg CLI (`curl -fsSL https://treg.to/install.sh | sh`).

## Steps

```bash
P=scripts/course-audience/audience.py
D=~/tmp/agent-reports/2026-11-10-dez-audience      # private, outside git
COURSE=de-zoomcamp; YEARS="2025 2026"

# 1. Pull submissions from CMP (final-project attempts + all homeworks). Emails are reduced to
#    their domain in memory; addresses are never written.
python3 $P fetch --course $COURSE --years $YEARS --output $D

# 2. Dedup repositories and grep them against configurable tool lists (one archive download per repo,
#    every tool set applied in the same pass). Writes <toolset>.csv and scan-counts.json.
python3 $P scan --output $D --workers 8 \
  --toolsets scripts/course-audience/tools/orchestrators.json scripts/course-audience/tools/warehouses.json

# 3. Identity evidence: opt-in public CMP profiles, then CMP learning-in-public links, GitHub
#    profiles/social accounts, personal sites, commit-author names, email-domain kind.
python3 $P profiles   --course $COURSE --years $YEARS --output $D
python3 $P identities --output $D

# 4. Re-check earlier rejected/low-confidence candidates (optional input recheck-candidates.json).
python3 $P recheck --output $D

# 5. Paid enrichment with the budget guard (dry-run first, then run). Stops before --stop-usd.
python3 $P linkedin           --output $D --cap-usd 10 --stop-usd 9 --dry-run
python3 $P linkedin           --output $D --cap-usd 10 --stop-usd 9
python3 $P github-linkedin    --output $D --cap-usd 10 --stop-usd 9 --workers 16   # name search
python3 $P candidate-profiles --output $D --cap-usd 10 --stop-usd 9
python3 $P reconcile          --output $D     # only if a paid run was interrupted

# 6. Classify and aggregate. --hide-labels guards sponsor-sensitive usage numbers.
python3 $P classify  --output $D
python3 $P aggregate --output $D --hide-labels Airflow Astronomer
python3 $P homework  --output $D             # unique submitters per homework (e.g. HW3)
python3 -m unittest discover -s scripts/course-audience -p 'test_*.py'
```

Outputs in `$D`: `enrichment-all.csv` (one row per author, GitHub handle + CMP id, never an
email), `audience-summary.md`, `audience-stats.json`, `<toolset>.csv`, `warehouses-summary.md`,
`identity-stats.json`, `rechecks.json`, `treg-ledger.json`. Copy the sponsor-facing files where
the request says; keep the cache private.

## 1. CMP pull

`/api/courses/<slug>/` lists projects and homeworks. Final projects are entries whose title or
slug matches project/capstone/final (midterms excluded). `/projects/<slug>/submissions` and
`/homeworks/<slug>/submissions` are exports without pagination; the script fails loudly if the
envelope changes. Kept fields: ids, links, commits, scores, `learning_in_public_links` and the
email domain. HW unique submitters = distinct `student_id` per homework export.

## 2. Repository dedup and tool grep

GitHub links are normalized case-insensitively to `owner/repo` (trailing slash, `.git`,
tree/blob removed). Attempts of the same repository within a year are merged; the latest attempt
selects the commit. Archives are fetched at the submitted commit with `gh api .../tarball/<sha>`
and read in memory (no extraction, no code execution). Limits: 2 MB per text file, 60 MB text,
150 MB archive. A submitted tree/blob path limits evidence to that directory; homework/module
directories are excluded; vendored `dbt_packages`, `dbt_modules`, `integration_tests` and
`jsonschemas` are skipped because they mention every warehouse. Markdown/notes are weak mentions
and never count. `none` = scanned, no evidence; `unknown` = not scannable (private, deleted,
non-GitHub, too large) and is reported, never dropped.

Tool sets are JSON files in `tools/`. Add one per research question:

```json
{"name": "warehouses", "version": 1, "mention_regex": "...",
 "implies": {"Astronomer": ["Airflow"]},
 "tools": {"Snowflake": {"patterns": ["snowflake\\.connector", "..."],
                         "packages": ["snowflake-connector-python", "dbt-snowflake"],
                         "file_rules": [{"path": "(^|/)profiles\\.yml$", "content_all": ["type:\\s*snowflake"], "label": "dbt profile"}]}}}
```

`patterns` are case-insensitive regexes (`(?-i:...)` for case-sensitive imports), `packages` are
matched in dependency files, `file_rules` match a path plus required content. Bump `version`
after changing a set: the scan cache key includes it.

## 3. Identity matching rules

One author = one CMP student id; the GitHub handle is the owner of the submitted repository.
Evidence types, strongest first:

| Rank | Evidence type | What it is | Result |
| --- | --- | --- | --- |
| 1 | `self_submitted_linkedin` | A `linkedin.com/in/<id>` or `/posts/<id>_...` URL the student submitted in CMP (learning-in-public links on homework/project submissions, or the opt-in public profile on the leaderboard) | **Confirmed** identity |
| 2 | `github_declared_linkedin` | LinkedIn URL on the author's own GitHub profile (social accounts, blog, bio) or on the personal site linked from it | **Confirmed** identity |
| 3 | `github_profile` | Company/bio the author wrote on their own GitHub account | Self-declared; high confidence for that field |
| 4 | `domain_signal` | Corporate email domain in CMP (not gmail/outlook/yahoo/proton/...; academic domains mark students) | **Company signal only**, never an identity link; medium confidence |
| 5 | `name_search_confirmed` | Treg name search candidate whose full profile carries a linking fact: the Data Engineering Zoomcamp certificate, a link to the GitHub account, the project name, or a DataTalksClub/Zoomcamp mention | Confirmed (high) |
| 6 | `name_search_corroborated` | Same-name candidate with corroboration: company equals GitHub company, email domain matches, or location country matches GitHub location *and* a data headline | Medium |
| - | anything weaker | Same name only, provider guess, conflicting name | **Low / rejected**: kept in the CSV with `flag`, excluded from aggregates |

Rules:
- A self-submitted or declared link always wins over any provider candidate.
- Commit author names and commit email domains are evidence for re-checks; write only
  "email domain matches", never the address.
- CMP display names are random ("Adoring Gould") unless the student enabled a public profile;
  only public-profile names are used.
- Re-check rejected candidates (`recheck`): list every check made (CMP links, GitHub/personal
  site, commit names, commit/CMP email domain kind, candidate profile facts) and confirm only on a
  linking fact; otherwise keep rejected with the reasons.

## 4. Enrichment and budget guard

Public sources first (CMP, GitHub API, personal sites). Treg only where they have nothing:
`anyapi.linkedin.user.profile.full` by confirmed URL (about $0.003-0.0042), then
`crawl4ai.linkedin.search.people` by first/last name ($0.0036, free on no rows) and full reads of at
most two name-matching candidates. `treg_budget.Ledger`:

- reserves each call's ceiling before it starts and refuses when spent + open reservations + the
  next reservation would pass `--stop-usd` (default $9 under a $10 cap), even with parallel workers;
- holds an exclusive file lock, so a second spending process on the same directory is refused;
- keeps the micro-USD charge from Treg's `charged_micro` per call (never provider credits);
- leaves a call whose charge is unknown unsettled and blocks new spend; `reconcile` replays it with
  the same `Idempotency-Key` (no new charge) and books it at its reserved ceiling.

Continue an earlier analysis by copying its `treg-ledger.json` into the new directory so the
cap covers the whole job. Do not kill a paid run with `pkill -f` from a shell whose own command
line contains the pattern.

## 5. Classification and aggregates

Current role = LinkedIn experience with end date Present (else current position; an ended latest
role gives no current employer). Role timing compares the role start with the cohort window
(`COURSE_WINDOW` in `classify.py`, Jan-Apr for DE Zoomcamp; adjust per course): before, during,
after. Seniority: student, job seeker (open to work / seeking / career switch with no current
employer), junior, mid, senior, lead+ (lead, head, principal, staff, manager, architect, founder,
director). Role family: DE, analytics eng, DA, DS/ML, SWE, other. **Freelance segment**: LinkedIn
employment type Freelance / Self-employed / Contract or a freelance/independent/contractor title;
reported separately (`freelance`, `self-employed`, `contract`) with a notable list, because these
people are the technical lead for their clients and pick the platform. Country: LinkedIn country,
else GitHub location. Notable companies: normalized employer names (suffixes and "via <agency>"
removed) matched against a brand list, plus every employer with two or more authors.

Aggregates use only rows with `enriched=yes` and no flag. `--hide-labels` makes `aggregate` fail
if usage numbers for those tools appear in `audience-summary.md` (sponsor sensitivity: for the
Astronomer pitch, Airflow usage numbers stay in the raw CSVs only).

## Data protection checklist

- No email address in any output, report, commit or message (the classifier asserts this).
- Outputs, caches, ledger and recheck inputs stay in the private report directory.
- Delete `/tmp/treg-api-key` after the paid steps.

## Remaining-author audit and employer analysis

Preserve the target set before a concurrent enrichment run updates it:

```bash
python3 scripts/course-audience/rest.py baseline --output "$D" --baseline-enriched 538
python3 scripts/course-audience/rest.py gather --output "$D" --workers 8
# Wait for the existing enrichment owner to exit before any new paid calls.
python3 scripts/course-audience/rest.py search --output "$D" --workers 8
# Review exact own-source quotes in private rest-reviewed.json, then rerun gather.
python3 scripts/course-audience/rest.py gather --output "$D" --workers 8
python3 scripts/course-audience/rest.py merge --output "$D" --predecessor-pid ORIGINAL_PID
```

`gather` writes `enrichment-rest.csv` and redacted evidence under `cache/rest/`.
It checks profile bios, profile READMEs, six pinned repositories, submitted project
READMEs, directly linked public sites and attributable commit domains. Technical
project topics do not establish an occupation. Commit domains remain historical
signals and never establish current employment. Failed or unavailable sources stay
in the audit. No Slack lookup runs without an existing display-name dataset.

`search` uses the shared ledger lock, a $0.005 ceiling per routed web search and the
$9 stop line under the shared $10 cap. Search results alone do not confirm identity;
review a linking fact before accepting an external profile. Review quoted facts
in `rest-reviewed.json` using the `apply_reviewed` schema in `rest.py`; only exact
quotes from the author's own profile, profile README or directly linked site can
replace an unconfirmed candidate. The candidate itself remains unconfirmed.

Employer metadata belongs in private `company-metadata.json`, keyed by
`aggregate.company_key(name)`. Each entry has `industry`, `segment`, `size` and
`sources` (primary-source URLs). Unsupported metadata stays unknown. Employer
counts exclude domain-only affiliations, educational/student affiliations,
independent practitioners and placeholders. Business-model segments are exclusive:
agency/consultancy takes precedence over enterprise size. State the enterprise
and startup definitions used in the report. A small unfamiliar firm is not assumed
to be a startup. The report includes top employers, industry and segment shares,
explicit denominators, and named companies relevant to sponsor pitches.

`merge` preserves accepted predecessor rows and merges only high/medium,
unflagged findings. It regenerates the summary and stats, then adds employer
analysis and the before/after coverage and shared spend. Run it again after a
later `classify` or `aggregate` to restore these additions. Keep all audit inputs,
metadata and outputs outside git.
