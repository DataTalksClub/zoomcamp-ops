# Zoomcamp Structure Spec

The canonical layout every DataTalks.Club zoomcamp follows. This file owns
structure: where files live, what they are called, and what the website's
ingestion pipeline requires of them.

Two neighbouring documents own the rest, and none of the three restate each
other:

| Document | Owns |
|----------|------|
| `STRUCTURE.md` (this file) | layout, filenames, unit page rules, the rule index |
| [`docs/conventions.md`](docs/conventions.md) | prose and presentation: banner block, heading style, wording, section patterns |
| [`docs/curriculum-contract.md`](docs/curriculum-contract.md) | the machine-readable contract: every YAML field, every diagnostic the parser emits |

Where any of them disagrees with the website's parser, the parser is right —
see [§7](#7-who-is-the-authority).

---

## 1. Repo layout

```
<course>-zoomcamp/
├── README.md                    # GitHub landing page (see §2)
├── SITE.md                      # website course description — fixed name
├── course.yaml                  # course identity (see docs/curriculum-contract.md)
├── cohorts/
│   ├── README.md                # explains this layout, names the live cohort
│   ├── 2026/                    # directory name IS the cohort identifier
│   │   ├── cohort.yaml          # cohort identity + dates
│   │   ├── README.md            # human schedule page (see §4)
│   │   ├── 01-intro/            # directory name IS the module slug
│   │   │   ├── module.yaml      # module identity
│   │   │   ├── README.md        # GitHub-facing module index (never ingested)
│   │   │   ├── 01-what-is-ml.md # units: NN-kebab.md siblings; stem IS the unit slug
│   │   │   ├── 02-rules-vs-ml.md
│   │   │   ├── homework.md      # homework instructions — fixed name
│   │   │   ├── homework.yaml    # homework identity, due date, form, questions
│   │   │   ├── images/          # every image any unit in this module references
│   │   │   └── code/            # notebooks and scripts the units link
│   │   ├── 02-regression/
│   │   └── project.md           # non-module cohort files are allowed
│   ├── 2025/                    # earlier cohorts: frozen (see §6)
│   └── 2024/
├── images/                      # repo branding only; never referenced by a unit
├── projects/                    # (optional) project instructions + gallery
├── archive/                     # (optional) unmaintained material, un-numbered
├── scripts/                     # camp-specific helper scripts
├── after-sign-up.md             # shared root docs, same filenames in every camp
├── learning-in-public.md
├── certificate.md
├── awesome-<topic>.md           # (optional) curated resource list
└── .github/
    ├── FUNDING.yml
    └── workflows/curriculum-check.yml   # calls the shared checker (§7)
```

The load-bearing rules. Each is checked by
[`scripts/check-zoomcamp`](scripts/check-zoomcamp/) and the rule ID is given so
a failure message points back here.

1. **Curriculum lives under `cohorts/<year>/`. Nothing curricular lives at the
   repo root.** `course.yaml` is the only manifest outside `cohorts/`, and there
   are no numbered module directories at the root. — `L001`, `L002`, `L003`,
   `L004`
2. **Names are identity.** Cohort identifier = directory name. Module slug =
   directory name (`NN-kebab-case`). Unit slug = file stem. Nothing restates
   them in YAML. — `L005`, `M004`, `M007`
3. **Units are siblings of `module.yaml`**, named `NN-kebab.md`, ordered by
   their numeric prefix, which must be unique within the module. `README.md` and
   `homework.md` are the only other top-level `.md` files a module directory may
   contain. There is no `lessons/` subdirectory. — `L006`, `L007`
4. **A module directory is self-contained.** Every image a unit uses is under
   that module's `images/`; every companion file is under the module directory.
   No `../` reference leaves it, apart from the one exception in `U5`. — `U004`
5. **One module, one homework, side by side.** `homework.yaml` and `homework.md`
   sit in the module directory they belong to. Neither is mapped anywhere by
   `cohort.yaml`. — `L008`, `M005`, `M008`
6. **A cohort year is a snapshot.** Starting cohort N+1 copies cohort N's tree
   and edits it. Published years share no files (§6). — `M005`
7. **Every module directory has a `README.md`.** GitHub readers need an index;
   the website never reads it. — `L009`
8. **`SITE.md` at the root is the website's course description.** Fixed name, no
   pointer field. The root `README.md` is a GitHub landing page and is never
   used as a description. — `L010`, `M009`

Naming conventions that survive from the old spec unchanged:

- Module directories are `NN-kebab-name` (`01-intro`, `02-experiment-tracking`),
  two-digit zero-padded, so they sort correctly. Prefix gaps are legal
  (ml-zoomcamp has no `07-*` module); order is sort order of the prefix, and the
  prefix is not required to be dense.
- Shared helper docs live at the repo root with the same filenames across all
  camps (`after-sign-up.md`, `learning-in-public.md`, `certificate.md`).
- Reusable cross-camp scripts live in [this template's `scripts/`](scripts/);
  copy what you need rather than re-writing.

### 1.1 Slugs are frozen; conventions bind forward

Every path segment above is a published URL segment:

```
/courses/<family>/<year>/modules/<module>/<unit>
     course.yaml:slug  ^      ^dir name  ^file stem
                  cohort dir name
```

So **renaming a file or directory in a published cohort moves a live URL**.
Some existing names violate the rules above and are staying that way:
ml-zoomcamp's `install.md` and `updates.md`, ai-dev-tools-zoomcamp's four
`lesson.md` files, llm-zoomcamp's `homework-01`-style homework slugs. They are
grandfathered, not mistakes to fix.

The convention binds **forward**: new units, new modules and new cohorts follow
it. Record each grandfathered path in the repo's `.zoomcamp-check.yaml` with a
reason (§7) so the exception is visible in review instead of being rediscovered
by whoever "fixes" it and breaks a public link.

---

## 2. Root `README.md` — canonical section order

Banner block first (image → title → tagline → signup button → link row →
badges), then these `##` sections in this order:

```
## Quick Links            — table: materials, video, Documentation, platform, Slack, Telegram, FAQ
## About the Course       — what you'll learn + duration
## Who Should Join        — target audience
## Prerequisites
## How to Take the Course — Live Cohort vs Self-Paced comparison table (see below)
## Syllabus               — one ### heading per module + bullet topics (see below)
## Projects / Capstone    — or "Final Project" (use the name that fits the course)
## Certificate            — certificate image + requirements + docs link (see below)
## Instructors
## Testimonials
## Community & Support
   ### Getting Help on Slack
   ### Learning in Public
   ### Contributing
## Sponsors
## About DataTalks.Club
```

Sections that only some courses have (FAQ, an AI-Shipping-Labs-style add-on) are
optional; place them after Community & Support and before About DataTalks.Club.
Only include a section when there is real content for it — do not add an empty
Instructors or Testimonials section just for symmetry.

Key conventions for the variable sections:

- Quick Links: plain table, no emoji in cells. Always include a Documentation row
  linking the shared Zoomcamp Logistics docs and the course's own docs page.
- How to Take the Course: a Live Cohort vs Self-Paced comparison table (Start,
  Lectures, Homework, Leaderboard, Peer Review, Certificate, Cost, Register) plus
  a short self-paced steps list. No mermaid diagrams.
- Syllabus: one `### [Module N: Title](cohorts/<current-year>/NN-folder/)`
  heading per module, each followed by a bullet list of topics. The links point
  into the current cohort, and one line says earlier cohorts live in sibling
  year directories. No wide tables.
- Certificate: the certificate image, the requirements, and a link to the docs
  certificate/certification page.
- Contributing: one paragraph — typo fixes go to the file under
  `cohorts/<current-year>/`, new units start from
  [`templates/unit.md`](templates/unit.md), and the PR checker will say what is
  wrong before a human has to.

Template: [`templates/root-README.md`](templates/root-README.md).

---

## 3. Module `cohorts/<year>/NN-name/README.md` — canonical template

The module README is a GitHub index page. It is **not ingested by the website**
and it is not where lesson content lives: the units are sibling files, and this
page links them.

```
# Module N: <Title>

<1–2 sentence module overview>

## N.1 [<Unit Title>](NN-unit-slug.md)   — one-line blurb
## N.2 [<Unit Title>](NN-unit-slug.md)
...
## Homework                              — link to the sibling homework.md
## Optional / Extras                     — optional
## Community Notes                       — standardized title
```

- Module title is `#` (h1); the unit index entries are `##`.
- `N.M` numbering belongs **here**, in the hand-written index, and nowhere else.
  A unit's own H1 is never numbered (rule `U2`, §5): its number comes from the
  filename prefix and the site renders it.
- Do not inline video thumbnails per lesson. The video lives in the unit's
  frontmatter `video_url` (`U6`), which GitHub renders as a small table at the
  top of the unit page.
- Every relative link must resolve (`L012`). Keep long install/setup
  instructions in a linked unit, not inline, so the index stays scannable.

Template: [`templates/module-README.md`](templates/module-README.md).

---

## 4. Cohort `cohorts/<year>/README.md` — canonical template

```
# <Course> Zoomcamp <Year> Cohort

* Start date, registration link, office-hours info

## Schedule              — table: module | topic | start | materials | homework
## Deadlines
## Office Hours
```

- Title is always `# <Course> Zoomcamp <Year> Cohort` (not "Edition", not bare year).
- Materials and homework links are **siblings**: `01-intro/` and
  `01-intro/homework.md`, not `../../01-intro/`. The modules live in this
  directory now.

Template: [`templates/cohort-README.md`](templates/cohort-README.md).

`cohorts/README.md` is a separate, short page that names the live cohort and
states the frozen-cohort policy (§6). Every repo has one — `L011`.

---

## 5. The unit page

A unit is one markdown file, and it is the thing the website publishes. Start
from [`templates/unit.md`](templates/unit.md).

```markdown
---
video_url: https://www.youtube.com/watch?v=XXXXXXXXXXX
code:
  - label: Notebook
    path: code/01-example.ipynb
---
# Introduction to Machine Learning

One- or two-sentence summary of what this unit covers.

Body prose. Images as `![alt](images/rules-vs-ml.png)`. Links to sibling units
by filename (`[the next unit](02-rules-vs-ml.md)`), to the homework as
`[homework](homework.md)`, to the module page as `[module overview](README.md)`.
```

| # | Rule | Rule ID |
|---|------|---------|
| U1 | Optional YAML frontmatter with **only** `video_url` and `code` keys (and, from Phase 3, `content_id`). `video_url` must be an `https` YouTube URL; each `code` entry is exactly `{label, path}` and the path must resolve inside the module directory. This is parser law today: any other key is rejected outright. | `U001` |
| U2 | The first content line is exactly one `#` H1, and it is the unit's title. No `##`-as-title, no `N.M` numeric prefix — numbering comes from the file's `NN-` prefix and the site renders it. The H1 is the single source of the title; if `module.yaml` still declares one, the two must agree. | `U002`, `M012` |
| U3 | No other H1 in the body; sections are `##`. | `U003` |
| U4 | Every image reference is a relative path inside the module directory (`images/...`). No `../`, no absolute GitHub URLs to this repo, no external image hosts for curriculum figures, and no URL-encoded separators (`images%2Ffoo.png` — generic rewriting tools produce these and silently miss them later). | `U004` |
| U5 | Every relative link stays inside the module directory, with one exception: a link to another module's material in the same cohort climbs exactly one level (`../02-regression/05-linear-regression.md`). Nothing relative climbs past the cohort directory; targets outside it (past cohorts, other repos) are written as absolute GitHub URLs. Every relative target must exist. | `U005` |
| U6 | Video links live **only** in frontmatter `video_url` — never as body prose, never as a thumbnail-image-wrapped link. The site renders a real player frame from the frontmatter; a body thumbnail becomes a duplicate dead-weight image on the published page. | `U006` |
| U7 | Companion files the unit teaches from are declared in frontmatter `code:` (label + path), resolved beside the unit file, so the site can render a "code for this lesson" block. A unit that walks through no files simply has no `code:` key. | `U001` (path resolution) |
| U8 | No trailing navigation furniture: no `## Navigation` blocks, no `[← Prev] \| [Next →]` lines, no "back to the course" links. Navigation is derived data — the site renders real prev/next, and on GitHub the module `README.md` index and the numbered directory listing navigate. Community `## Notes` sections are content, not furniture: they stay. | `U008` |
| U9 | `homework.md` follows the same title rule: one leading H1 equal to the homework's title. | `U009` |
| U10 | *(from Phase 3 on)* frontmatter carries the unit's `content_id`, minted once per unit and never copied. Identity then travels with the file, so a rename preserves read-state and provenance. | `U010` |

Two things that are **not** rules: how long a unit is, and whether it has a
video. Twenty of today's units have no video; under U6 that is an absent key,
not an error.

---

## 6. Cohort years: duplication, freezing and backports

**A cohort year is a full copy, not a reference.** Starting the 2027 cohort
copies `cohorts/2026/` to `cohorts/2027/` and edits it. There is no shared
`content/` root, no manifest pointing across years, and no symlinks.

Why, since duplication normally smells:

- **A published cohort is a historical record, and sharing breaks it silently.**
  Every push re-imports the whole repository. If 2026 and 2027 shared unit
  files, every 2027-era edit would rewrite the *published 2026 pages* — pages
  2026 students hold read-state and submissions against — with nobody deciding
  that. With per-year trees, a 2026 page changes only when someone deliberately
  edits `cohorts/2026/`.
- **The pipeline already enforces the isolation.** Modules may not be referenced
  across cohorts, homework may not cross either, unit paths may not contain
  `..`, and the snapshot builder refuses symlinks outright. Every sharing
  mechanism is already rejected; duplication is the design the machinery wants.
- **Indirection is the bug class we keep paying for.** Two places asserting
  where one piece of content lives drift the moment a human forgets the tooling.
- **Git absorbs the cost.** A year's tree is single-digit megabytes and
  identical blobs cost near-zero in the pack.

The honest counter-argument, recorded once: for a course whose content barely
changes, evergreen modules shared by reference are cheaper, and the yearly fork
is real work. That was weighed against one obvious shape for every repo and
immutable cohort history, and the fork won.

**Policy for a typo that exists in three cohorts:**

- Fix the **current cohort**. That is the only place content PRs are normally
  accepted.
- Past cohorts are frozen archives; the drift *is the record of what was taught*.
  Backport only factual or breaking errors (a wrong command, a dead dataset
  URL), by a maintainer, per cohort, explicitly.
- Backporting is mechanical because the trees are congruent: the same file lives
  at the same cohort-relative path, so `grep -rl` finds every affected year and
  the fix is the same hunk in each.

Say all of this in the repo's own `cohorts/README.md` so contributors do not
have to guess.

---

## 7. Who is the authority

Two enforcers, one of them final:

- **The website's ingestion parser is the authority.** It parses a pushed
  commit, rejects anything malformed with a typed diagnostic, and leaves the
  previously imported content serving. It never guesses: no fallback title, no
  tolerated stray key. A repo that this document and the parser disagree about
  is a repo the parser wins.
- **[`scripts/check-zoomcamp`](scripts/check-zoomcamp/) is the earlier,
  friendlier gate.** It lives here, next to the convention text it enforces, so
  a rule change and its check land in one commit. It runs locally and on every
  pull request, minutes after a push, instead of hours later on a rejected
  import.

The checker is not a replacement and must not grow rules the convention does not
state. Every rule it can emit is listed in §8; if it fires on something this
file does not say, that is a bug in the checker.

Run it locally:

```bash
uv run https://raw.githubusercontent.com/DataTalksClub/zoomcamp-template/main/scripts/check-zoomcamp/check_zoomcamp.py .
```

Wire it into a course repo by copying
[`templates/workflows/curriculum-check.yml`](templates/workflows/curriculum-check.yml)
to `.github/workflows/curriculum-check.yml`. It calls this repo's reusable
workflow at a pinned SHA; the checker version and the convention version are the
same version.

**Migration phases.** `--phase` decides how strict the checker is, and the
default lives in the repo's `.zoomcamp-check.yaml`:

| Phase | What is an error | What is a warning |
|-------|------------------|-------------------|
| 1 — layout | layout and manifest rules (`L*`, `M001`–`M006`, `U001`) | unit shape (`U002`–`U009`, `M012`), retired knobs |
| 2 — unit shape | the above plus unit shape | retired knobs |
| 3 — derived contract | everything, including retired knobs | advisories only |

Phase 3 rules describe the end state and **will fail against the deployed parser
until it catches up** — it still requires `cohort.yaml` identity fields, the
`units` list, `instructions_path` and `description_path`. That is why they are
warnings first. Do not delete a knob because the checker mentioned it; delete it
when [`docs/curriculum-contract.md`](docs/curriculum-contract.md) says the
parser has stopped requiring it.

**Grandfathered paths** go in `.zoomcamp-check.yaml` at the repo root:

```yaml
phase: 1
allow:
  - rule: L007
    path: cohorts/2026/08-deep-learning/install.md
    reason: "frozen slug: published as /modules/08-deep-learning/install"
```

Every entry needs a reason, and an entry that stops matching anything is
reported (`C002`) so the list decays instead of accumulating.

One thing to know before reading a report: units in a **non-conforming location**
(a root-level module, a `lessons/` subdirectory) are reported for placement but
their content is not checked. Fix `L002`/`L007` first, then re-run for the
content findings.

---

## 8. Rule index

Run `uv run check_zoomcamp.py --rules` for the same list from the checker.

| Rule | Spec | What it means |
|------|------|---------------|
| `L001` | §1.1 | `course.yaml` exists at the repository root |
| `L002` | §1.1 | `module.yaml` only at `cohorts/<year>/<NN-module>/module.yaml` |
| `L003` | §1.1 | `cohort.yaml`, `homework.yaml` and `course.yaml` sit at their fixed depths |
| `L004` | §1.1 | no numbered module directories at the repository root |
| `L005` | §1.2 | module directory name is `NN-kebab-case` |
| `L006` | §1.3 | a module directory holds only units, `README.md`, `homework.*`, `images/`, `code/` |
| `L007` | §1.3 | unit files are `NN-kebab.md` siblings of `module.yaml`, with unique prefixes |
| `L008` | §1.5 | `homework.md` and `homework.yaml` are co-located |
| `L009` | §1.7, §3 | every module directory has a `README.md` index |
| `L010` | §1.8 | `SITE.md` exists at the repository root |
| `L011` | §4, §6 | `cohorts/README.md` names the live cohort and the freeze policy |
| `L012` | §3 | relative links in a module README resolve |
| `M001` | contract | manifest YAML parses, no duplicate keys, no unknown keys, no missing keys |
| `M002` | contract | every `content_id` is a canonical UUID, unique across the repository |
| `M003` | contract | `schema_version` is `1` |
| `M004` | §1.2 | `cohort.yaml` restates identity the path already carries (retired) |
| `M005` | §1.5, §1.6 | flow entries resolve, stay in their cohort, and pair co-located files |
| `M006` | §1.3 | `module.yaml` units resolve and match the unit files on disk |
| `M007` | §1.2 | declared `slug` keys only restate the path (retired) |
| `M008` | §1.5 | `instructions_path` only restates `homework.md` (retired) |
| `M009` | §1.8 | the course description comes from `SITE.md` (retired `description_path`) |
| `M010` | §1.1 | new-cohort homework slugs are `hwNN`; existing slugs are frozen |
| `M011` | §5 U10 | `module.yaml` declares a `units` list (derived from Phase 3 on) |
| `M012` | §5 U2 | a declared unit title agrees with the unit file's H1 |
| `U001` | §5 U1, U7 | unit frontmatter carries only allowed keys with valid values |
| `U002` | §5 U2 | a unit opens with exactly one unnumbered `# Title` |
| `U003` | §5 U3 | a unit body has no second H1 |
| `U004` | §5 U4 | images resolve inside the module directory |
| `U005` | §5 U5 | relative links resolve and stay inside the cohort |
| `U006` | §5 U6 | videos live in frontmatter `video_url`, never in the body |
| `U008` | §5 U8 | no hand-maintained navigation furniture |
| `U009` | §5 U9 | `homework.md` opens with a single H1 |
| `U010` | §5 U10 | the unit's `content_id` lives in its frontmatter (Phase 3) |
| `C001` | §7 | `.zoomcamp-check.yaml` is well formed |
| `C002` | §7 | every declared allowance is still needed |

There is no `U007` rule ID: "declare the files you teach from" is authoring
guidance no script can verify. Its checkable half — a declared `code` path must
resolve — is `U001`.

---

## Conventions summary

See [`docs/conventions.md`](docs/conventions.md) for prose and presentation
rules. The headline ones:

- Banner order: image → `<h1>` title → one-line tagline → Airtable signup
  button → inline `•`-separated link row → status badges.
- No emoji in `##` headings. (Emoji are fine inside the Quick Links table.)
- No bold formatting anywhere; rely on headings and lists.
- Standard heading names — "How to Take the Course" (not "Join"/"Enroll"),
  "Community & Support", "About DataTalks.Club".
- Title pattern: `<Course> Zoomcamp: A Free <N>-Week Course on <topic>`.
- Let GitHub auto-generate the table of contents — don't hand-maintain one.
