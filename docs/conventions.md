# Zoomcamp Conventions

The rules that keep every camp reading the same way. When in doubt, match these
over what any single existing camp currently does.

**Scope.** This page owns prose and presentation: the banner block, heading
style, wording, and the shape of the recurring README sections. It does **not**
own structure. Where files live, what they are called, what a unit page must
contain and what the YAML manifests must say are in
[`STRUCTURE.md`](../STRUCTURE.md) and
[`docs/curriculum-contract.md`](curriculum-contract.md).

This split is deliberate. Until recently both files stated the module folder
naming rule, the `N.M` lesson numbering rule and the syllabus link format, and
the copies had already started to disagree. Two documents restating one rule is
the same failure as two YAML keys restating one name: they drift, and then
nobody knows which is the spec. So: one rule, one home, and a link from the
other.

| Question | Where the answer lives |
|----------|------------------------|
| Where does this file go? What is it called? | `STRUCTURE.md` §1 |
| What must a unit page contain? | `STRUCTURE.md` §5 |
| What does the website's parser require? | `docs/curriculum-contract.md` |
| How should this heading be worded? Which section order? | here |

---

## Banner block (top of root README)

Always in this order:

1. Centered image (`images/<banner>`), `width="80%"`.
2. `<h1>` title: `<Course> Zoomcamp: A Free <N>-Week Course on <topic>`.
3. One-line tagline in a centered `<p>`.
4. Airtable signup button (the standard 50px image link).
5. Inline link row, `•`-separated: Join Slack · #channel · Telegram · Playlist · FAQ.
6. Status badges: PRs welcome, Join Slack (Star-the-repo optional).

## Headings

- No emoji in `##`/`###` headings. Emoji are allowed only inside the Quick
  Links *table* cells. (Rationale: emoji break heading anchors and make the
  auto-TOC inconsistent across camps.)
- No bold formatting (`**text**`) anywhere — in READMEs, module pages, units or
  docs. Use plain text; rely on headings and lists for structure.
- Standardized section names — use these exact strings:
  - `How to Take the Course` (not "How to Join", "How to Enroll", "How to Take X Zoomcamp")
  - `Community & Support`
  - `About DataTalks.Club`
  - `Getting Help on Slack`
  - `Learning in Public`
  - `Community Notes` (in module READMEs and units)
- Root README heading levels: top sections are `##`; their sub-parts are `###`.
- Module README: title `#`, unit index entries `##` numbered `N.M`.
- **Unit page: title `#`, unnumbered, and it is the only `#` in the file.**
  A unit's number comes from its `NN-` filename prefix; writing `## 3.3 Confusion
  Table` at the top of a unit states the title twice and the number twice, and
  the published page then shows the heading twice. Sections inside a unit are
  `##`. Full rule set: `STRUCTURE.md` §5.

## Table of contents

Don't hand-maintain a TOC. GitHub renders an automatic outline from the
headings; a manual TOC just drifts.

The same argument applies to per-unit prev/next links, "back to the course"
lines and `## Navigation` blocks: the site renders navigation from the unit
order, GitHub navigates by the module README and the numbered directory listing,
and the hand-written copies have already drifted in wording between neighbouring
files. Don't write them (`U8`).

## Writing a unit

The full rules are `STRUCTURE.md` §5; the ones that are writing habits rather
than structure:

- Open with the title as `#`, then one or two sentences saying what the unit
  covers, before any heading. A reader who lands from search should know in one
  screen whether they are in the right place.
- Put the video in frontmatter, not in the prose, when you are writing a new
  unit: GitHub renders frontmatter as a small table at the top of the file, so
  it stays visible, and it is where the site will read it. Do **not** convert an
  existing unit's video yet — the site does not read frontmatter video today and
  the conversion would remove the video from a published page. `STRUCTURE.md`
  §5 U6 has the detail and the checker says so too.
- Keep every asset the unit needs inside the module directory: images in
  `images/`, notebooks and scripts in `code/`. No `../` reaching into another
  module for a figure, no hotlinking an image from another repo or an external
  host, and no absolute GitHub URLs back into this repo for something that is
  sitting next to the file.
- Link a sibling unit by filename (`[the next unit](02-rules-vs-ml.md)`), the
  homework as `homework.md`, and another module in the same cohort as
  `../02-regression/01-linear-regression.md`. Anything outside the cohort —
  a past cohort's archive, another repository — is an absolute GitHub URL.
- `## Notes` sections contributed by the community are content. They stay.

## Fixing a typo that exists in three cohorts

Fix it in the current cohort. Past cohorts are frozen archives and the drift is
the record of what was taught; only factual or breaking errors get backported,
by a maintainer, per cohort, explicitly. Full policy and the reasoning:
`STRUCTURE.md` §6.

## Filenames

Shared root docs use the same names across all camps so cross-links and tooling
are portable:

| File | Purpose |
|------|---------|
| `README.md` | GitHub landing page |
| `SITE.md` | the website's course description |
| `after-sign-up.md` | what to do after registering |
| `learning-in-public.md` | learning-in-public guide |
| `certificate.md` | certificate instructions (singular) |
| `awesome-<topic>.md` | optional curated resource list |

Directory and unit naming (`cohorts/<year>/NN-module/NN-unit.md`) is structural —
see `STRUCTURE.md` §1.

## Title / wording

- Duration is always phrased as "A Free N-Week Course" (use weeks, not months).
- Course name capitalization: `Machine Learning Zoomcamp`, `MLOps Zoomcamp`,
  `Data Engineering Zoomcamp`, `LLM Zoomcamp`.
- Cohort README title: `<Course> Zoomcamp <Year> Cohort` — not "Edition", not a
  bare year.

## Section patterns

- Quick Links: a plain table (no emoji in cells) that always includes a
  Documentation row linking the shared Zoomcamp Logistics docs and the course's
  own docs page.
- How to Take the Course: a Live Cohort vs Self-Paced comparison table (rows:
  Start, Lectures, Homework, Leaderboard, Peer Review, Certificate, Cost,
  Register) followed by a short self-paced steps list. No mermaid diagrams.
- Syllabus: one `### [Module N: Title](cohorts/<current-year>/NN-folder/)`
  heading per module, each with a bullet list of topics, plus one line saying
  earlier cohorts live in sibling year directories. No wide tables.
- Certificate: the certificate image (`images/<course>-zoomcamp-certificate.jpg`),
  the requirements, and a link to the docs certificate/certification page.
- FAQ: keep it short and link to the full FAQ at
  `datatalks.club/faq/<course>-zoomcamp.html` rather than inlining a long Q&A.
- Contributing (under Community & Support): one paragraph — typo fixes go to the
  file under `cohorts/<current-year>/`, new units start from
  [`templates/unit.md`](../templates/unit.md), and the PR checker reports what is
  wrong before a reviewer has to.
- Long add-on sections (e.g. an AI-Shipping-Labs-style block): keep a brief
  summary in the README and link to the docs page for the details.
- Sponsors: the heading is `## Sponsors` (not "Sponsors & Supporters"). Show
  logos only if the course actually has sponsors; otherwise a one-line contact.

## Social links

- Use X, not Twitter: `<a href="https://x.com/DataTalksClub">X</a>`.

## Tooling

- Python helper scripts use `uv`. Two shapes are in use and both are fine: a
  committed `pyproject.toml` + `uv.lock` (see `scripts/generate-thumbnails`) or
  PEP 723 inline metadata in the script itself (see
  `scripts/check-zoomcamp`). Run with `uv run <script>.py`.
- Every course repository runs [`scripts/check-zoomcamp`](../scripts/check-zoomcamp/)
  on pull requests, via the pinned reusable workflow in
  [`templates/workflows/curriculum-check.yml`](../templates/workflows/curriculum-check.yml).
  It is the early gate; the website's parser is the authority (`STRUCTURE.md` §7).
- Thumbnails are self-hosted (committed under `images/`), generated by
  `scripts/generate-thumbnails`, not fetched from external services at render
  time. They belong in module READMEs and landing pages; a new unit's video
  goes in frontmatter (see the U6 caveat above).

## Reference implementations

When unsure how something should look, copy from the camp that does it best:

- Cohort curriculum layout (`cohorts/<year>/NN-module/`): LLM Zoomcamp
- Banner + badges: LLM Zoomcamp
- Syllabus linking into the current cohort: MLOps Zoomcamp
- Thumbnail tooling: Data Engineering Zoomcamp (`scripts/generate_thumbnails.py`)
- Video chopping/upload pipeline: LLM Zoomcamp (`scripts/youtube-upload`, `scripts/chop-specs`)

Reference implementations are examples, not the spec. Every one of these repos
still has findings against `check-zoomcamp`; when a camp and this documentation
disagree, the documentation wins and the camp has a to-do.
