# Zoomcamp Template

The shared template and reference for DataTalks.Club Zoomcamps —
[ML](https://github.com/DataTalksClub/machine-learning-zoomcamp),
[MLOps](https://github.com/DataTalksClub/mlops-zoomcamp),
[Data Engineering](https://github.com/DataTalksClub/data-engineering-zoomcamp),
[LLM](https://github.com/DataTalksClub/llm-zoomcamp), and any new camp.

This repo exists so every zoomcamp is organized the same way and so we stop
re-inventing the same helper scripts in each one. Use it two ways:

- Starting a new zoomcamp → copy the templates and follow the checklist.
- Maintaining an existing zoomcamp → bring its READMEs and scripts in line
  with the conventions here.

## What's inside

| Path | What it is |
|------|------------|
| [`STRUCTURE.md`](STRUCTURE.md) | The canonical repo layout, unit page rules, and the checker's rule index |
| [`docs/curriculum-contract.md`](docs/curriculum-contract.md) | What the website's ingestion parser requires, field by field |
| [`docs/conventions.md`](docs/conventions.md) | Prose and presentation: headings, banner block, section patterns |
| [`docs/new-zoomcamp-checklist.md`](docs/new-zoomcamp-checklist.md) | Step-by-step to spin up a new camp from these templates |
| [`templates/`](templates/) | Copy-paste templates: unit, module, cohort, root README, CI workflow |
| [`scripts/check-zoomcamp/`](scripts/check-zoomcamp/) | The conformance checker every course repo runs on pull requests |
| [`scripts/`](scripts/) | Reusable helper scripts collected from all camps ([index](scripts/README.md)) |
| [`docs/`](docs/) | Operational guides (video pipeline, workshop best practices) |

## Quick start for a new camp

```bash
# 1. copy the templates into your new repo
cp templates/root-README.md        <new-camp>/README.md
cp templates/cohorts-README.md     <new-camp>/cohorts/README.md
cp templates/cohort-README.md      <new-camp>/cohorts/2026/README.md
cp templates/module-README.md      <new-camp>/cohorts/2026/01-intro/README.md
cp templates/unit.md               <new-camp>/cohorts/2026/01-intro/01-what-is-it.md
cp templates/after-sign-up.md      <new-camp>/
cp templates/learning-in-public.md <new-camp>/
cp templates/workflows/curriculum-check.yml <new-camp>/.github/workflows/

# 2. fill in the {{PLACEHOLDERS}}, then follow:
#    docs/new-zoomcamp-checklist.md

# 3. check it before pushing
uv run https://raw.githubusercontent.com/DataTalksClub/zoomcamp-template/main/scripts/check-zoomcamp/check_zoomcamp.py <new-camp>
```

## Why this exists

The four camps drifted apart over the years — different heading names
("How to Join" vs "How to Take" vs "How to Enroll"), emoji in some and not
others, table-of-contents in one, badges in another, and copies of the same
thumbnail/video scripts in each repo with small variations. This repo is the
single source of truth so new camps start consistent and old ones converge.

Writing a convention down turned out not to be enough: the camps also diverged
in the curriculum layout the website ingests, and nothing checked. So the spec
now comes with [`scripts/check-zoomcamp`](scripts/check-zoomcamp/), which every
course repository runs on pull requests. A rule and its check live in the same
commit here, and a course repo pins one SHA to get both.

See [`STRUCTURE.md`](STRUCTURE.md) for the full spec.
