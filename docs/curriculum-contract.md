# The Curriculum Contract

What the website's ingestion pipeline requires of a course repository, field by
field. Until now this contract existed only as parser code and as the handful of
repos that happened to satisfy it, so the only way to discover a rule was to have
an import rejected. This page is that contract written down.

[`STRUCTURE.md`](../STRUCTURE.md) owns where files live and what units look like.
This page owns the four YAML manifests and the failure modes.

**The parser is the authority.** It lives in the website repository
(`content_sync/course_repository.py`, with the projection in
`courses/services/curriculum_import.py`). If this page and the parser disagree,
the parser is right and this page has a bug worth reporting. The PR checker
([`scripts/check-zoomcamp`](../scripts/check-zoomcamp/)) is a friendlier
restatement of the same rules, not a second authority.

---

## 1. How ingestion works, in six sentences

A push to the course repository fires a webhook. The website downloads a tarball
of that exact commit, turns it into an immutable snapshot of paths and bytes, and
parses it whole. Parsing is strict and total: an unknown key anywhere, a missing
file anywhere, a duplicate `content_id` anywhere rejects the entire commit. A
rejected import records a diagnostic and **leaves the previous successful import
serving**, so a bad push produces stale content and a red run, never a broken
site. A successful parse is projected in one transaction, reconciled by
`content_id` rather than by path — which is why moving a file preserves its
identity, its read-state and its submissions. Slugs, and therefore URLs, come
from names on disk, which is why renaming a file is a published-URL change and
[`STRUCTURE.md` §1.1](../STRUCTURE.md#11-slugs-are-frozen-conventions-bind-forward)
freezes them.

---

## 2. Universal rules

These hold for every manifest:

- **Strict keys.** Unknown keys are rejected (`unknown_key`), missing required
  keys are rejected. There is no "extra metadata for later" — add the field to
  the contract or leave it out.
- **No duplicate keys** within a mapping.
- **`schema_version` is the integer `1`.** Not `"1"`.
- **`content_id` is a canonical lowercase UUID string** (`uuidgen | tr 'A-Z' 'a-z'`),
  unique across the *whole repository* — courses, cohorts, modules, units,
  homeworks and questions share one namespace. Copying a unit file as a template
  and forgetting to change its `content_id` is the most common way to break an
  import (`duplicate_content_id`).
- **`content_id` is minted once and never reused, never re-pointed.** It is the
  identity the importer reconciles on. A new cohort's modules and units get
  *new* ids: a 2027 module is a new row, not the 2026 row rebound.
- **Paths are repository-relative POSIX paths.** No leading `/`, no `..`
  segments, no backslashes, no URL schemes, no symlinks. Referenced files must
  exist in the commit.
- **Slugs match `[a-z0-9]+(-[a-z0-9]+)*`** — lowercase, single hyphens, no
  underscores, no trailing hyphen.
- **Dates are `YYYY-MM-DD`; timestamps carry a timezone** (`2026-01-19T21:59:00Z`).
- **Limits**: 5,000 files, 100 MB total, 8 MB per file, 512 KB per YAML file.

Manifest placement is fixed, and a manifest anywhere else rejects the commit
(`manifest_path_invalid`):

| File | Only valid location |
|------|---------------------|
| `course.yaml` | repository root |
| `cohort.yaml` | `cohorts/<identifier>/cohort.yaml` |
| `module.yaml` | `cohorts/<identifier>/<module>/module.yaml` |
| `homework.yaml` | `cohorts/<identifier>/<module>/homework.yaml` |

> The deployed parser also still accepts `module.yaml` at `<module>/module.yaml`
> at the repository root. That is the abolished layout, kept only so repositories
> can migrate in one commit each; it is a `L002` error in the checker and the
> parser will stop accepting it at Phase 3.

---

## 3. `course.yaml`

One per repository, at the root.

```yaml
schema_version: 1
content_id: 7736c1e6-5d66-4286-8180-b1eef3f83a84
slug: llm-zoomcamp
title: LLM Zoomcamp
description_path: SITE.md
outcome: Build, evaluate, and monitor production-style LLM applications.
repository_url: https://github.com/DataTalksClub/llm-zoomcamp
docs_url: https://datatalks.club/docs/courses/llm-zoomcamp/
faq_url: https://datatalks.club/faq/llm-zoomcamp.html
hashtag: llmzoomcamp
published: true
```

| Field | Required | Notes |
|---|---|---|
| `schema_version` | yes | `1` |
| `content_id` | yes | minted once, never changed |
| `slug` | yes | the published course family segment. **Not derivable** from the repository name: the repo is `machine-learning-zoomcamp` but the family is `ml-zoomcamp`. Changing it moves every URL of the course. |
| `title` | yes | per-course prose |
| `outcome` | yes | one sentence the site renders |
| `repository_url` | yes | https. Cross-checked against the webhook's repository identity — a deliberate tripwire that catches forks and renamed repos pushing into the wrong family. |
| `docs_url`, `faq_url` | yes | https. Kept declared because they are not uniformly derivable (ml-zoomcamp's FAQ path uses the *repo* name while its slug is `ml-zoomcamp`). |
| `hashtag` | yes | letters, digits and underscores; no leading `#` |
| `published` | yes | boolean |
| `description_path` | **transitional** | must be `SITE.md`. See below. |
| `description` | **retired** | inline description text. Move it to `SITE.md`. |

**The description, and the one live inconsistency.** The convention is: `SITE.md`
at the repository root is the course description, by fixed name, with no pointer
field — the same shape as `homework.md`. The deployed parser has not caught up:
it requires *exactly one* of `description` or `description_path`, so today a repo
writes `description_path: SITE.md` and keeps the file. The checker therefore
accepts `description_path: SITE.md`, rejects it pointing anywhere else, and warns
that the key is retiring (`M009`).

Never point `description_path` at `README.md`. It has been done, and it published
banner markup and badges as three courses' descriptions, overwriting curated
copy. The root README is a GitHub landing page; `SITE.md` is the website's copy.

---

## 4. `cohort.yaml`

One per cohort directory. The directory name is the cohort identifier.

```yaml
schema_version: 1
content_id: 88444444-4444-4444-8444-444444444444
format: modules
published: true
start_date: 2026-06-08
end_date: 2026-10-12
```

| Field | Required | Notes |
|---|---|---|
| `schema_version`, `content_id` | yes | |
| `format` | yes | `modules` or `legacy`. `legacy` cohorts carry no curriculum: the site keeps whatever it already has for them, and a `flow` is rejected. |
| `published` | yes | boolean |
| `start_date`, `end_date` | yes | `YYYY-MM-DD`; end must not precede start |
| `course` | **retired** | restates `course.yaml:slug`; can only be redundant or wrong |
| `identifier` | **retired** | restates the directory name. The parser already refuses an identifier that disagrees with the directory — which proves the directory is authoritative, so the field has no job. |
| `year` | **retired** | derived as `int(identifier)` |
| `legacy_slug` | **retired** | derived as `<course-slug>-<identifier>`; all three repos declare exactly the derivable value |
| `title`, `description` | **retired** | derived as `"<course title> <identifier>"` and composed by the site |
| `flow` | **transitional** | see below |

The deployed parser still *requires* every field marked retired. They are listed
as retired so nobody adds a new one and so the Phase 3 cleanup is already
written down; the checker warns (`M004`) and only errors at `--phase 3`.

### Flow

`flow` declares the module order and pairs each module with its homework:

```yaml
flow:
  - module:
      source: cohorts/2026/01-agentic-rag/module.yaml
      homework: cohorts/2026/01-agentic-rag/homework.yaml
  - project: capstone
```

Rules the parser enforces: every referenced file must exist and be a real
manifest; a module and its homework must belong to *this* cohort
(`module_cohort_mismatch`, `homework_cohort_mismatch`); no module or homework may
appear twice; at least one module entry is required; every `homework.yaml` in the
repository must be referenced by some flow (`unreferenced_homework_manifest`);
homework slugs must be unique within a cohort.

Rules the *convention* adds on top (`M005`): a module and its homework are
co-located in the same directory, and the flow order matches the directory
prefixes. The knob that let one repo bind module `01-ai-native-workflow` to
homework directory `01-overview` is a mismatch to fix, not a feature.

From Phase 3, `flow` becomes optional and is derived by default: the cohort's
modules are the `NN-*/` directories containing `module.yaml`, ordered by prefix,
each paired with its own `homework.yaml`. A declared `flow` survives only for
what cannot be derived — interleaving a project, or a genuine reordering — and
its entries shrink to directory names.

---

## 5. `module.yaml`

One per module directory. The directory name is the module slug.

```yaml
schema_version: 1
content_id: 2a309b04-3047-4864-a32e-a8c101603b29
title: Agentic RAG
units:
  - content_id: 856087c5-2a56-41ad-b43b-36e6ab335414
    title: Introduction
    path: 01-intro.md
```

| Field | Required | Notes |
|---|---|---|
| `schema_version`, `content_id` | yes | |
| `title` | yes | per-module prose. Stays declared: deriving it from the README H1 would couple site metadata to a GitHub marketing heading. |
| `slug` | **retired** | must equal the directory name or the import fails; it can only restate or be wrong |
| `units` | **transitional** | ordered list; see below |
| `units[].content_id` | yes | unique repository-wide |
| `units[].title` | **retired** | must equal the unit file's H1 (`M012`). Two statements of one title is exactly the drift that put duplicate headings on published pages. |
| `units[].path` | yes | module-relative, `.md`, must exist. No `..`. |
| `units[].slug` | **retired** | must equal the file stem |

**Where the derived-units rule applies — forward, not backward.** A `module.yaml`
**with** a `units` list is authoritative as declared; that is the shape every
frozen cohort keeps, and it is what lets ml-zoomcamp go on publishing
`install.md` and `updates.md` as units. From Phase 3, a `module.yaml`
**without** a `units` list derives them from the `NN-*.md` siblings in prefix
order, each carrying its own `content_id` in frontmatter. New cohorts use the
list-less form, where new slugs are legitimate because the cohort's URLs do not
exist yet. `units` survives only as a frozen-cohort affordance, never as a choice
for new content.

**Where ordering comes from.** Today: the `flow` list index for modules, the
`units` list index for units. In the convention: the `NN-` prefix, in both cases.
Verified across all three repos, the declared order and the prefix order agree
everywhere today — so making the prefix authoritative changes no published
ordering, it removes the second way of stating it. Prefix gaps are legal; two
units with the same prefix are not.

---

## 6. Unit frontmatter

Optional, and strictly bounded. The parser rejects any key outside the
allowlist, so this is not a place to stash metadata.

```yaml
---
video_url: https://www.youtube.com/watch?v=Crm_5n4mvmg
code:
  - label: Notebook
    path: code/notebook.ipynb
---
```

| Key | Notes |
|---|---|
| `video_url` | `https`, and the host must be `youtube.com`, `www.youtube.com`, `m.youtube.com` or `youtu.be`. The site renders a player from it. |
| `code` | list of `{label, path}`. The path is resolved relative to the unit file and must exist in the commit; the snapshot builder ships those files so the site can offer them. |
| `content_id` | **Phase 3 only.** Adding it today is rejected by the deployed parser. |

Everything below the closing `---` is the unit body, and
[`STRUCTURE.md` §5](../STRUCTURE.md#5-the-unit-page) governs its shape.

---

## 7. `homework.yaml`

Beside the `homework.md` it describes.

```yaml
schema_version: 1
content_id: 85555555-5555-4555-8555-555555555555
slug: hw01
title: "Homework 1: Agentic RAG"
instructions_path: homework.md
due_at: 2026-08-31T21:59:00Z
initial_state: open
form:
  homework_url: true
  time_spent_lectures: true
  time_spent_homework: true
  faq_contribution: true
  learning_in_public_cap: 7
questions:
  - content_id: 86666666-6666-4666-8666-666666666666
    id: lesson-page-count
    type: multiple_choice
    prompt: How many lesson pages are in the dataset?
    options:
      - id: pages-24
        label: "24"
      - id: pages-72
        label: "72"
    points: 1
```

| Field | Required | Notes |
|---|---|---|
| `schema_version`, `content_id` | yes | |
| `slug` | yes | a published URL segment. The repos disagree today (`hw01` in two, `homework-01` in one) and both are frozen. New cohorts use the derived `hwNN`, where `NN` is the module prefix (`M010`). |
| `title` | yes | prose |
| `due_at` | yes | timezone-aware timestamp |
| `initial_state` | yes | the state the homework is imported in |
| `form` | yes | all five keys required: `homework_url`, `time_spent_lectures`, `time_spent_homework`, `faq_contribution`, `learning_in_public_cap` |
| `questions` | yes | at least one |
| `instructions_path` | **retired** | it is `homework.md` beside the YAML in every repo already. A fixed name, like `SITE.md`. |

Question fields: `content_id`, `id` (slug, unique within the homework), `type`
(`multiple_choice`, `checkboxes`, `free_form`, `free_form_long`), `prompt`,
`points`, and either `options` (at least two `{id, label}` pairs, for the choice
types) or `answer_type` (for the free-form types). An optional `answer` carries
an **encrypted** envelope.

**Never commit a plaintext answer.** The parser refuses a manifest containing
`answer_key`, `answer_value`, `correct_answer`, `plaintext_answer` or `solution`,
precisely so a well-meaning contributor cannot publish the answer key in a public
repository.

---

## 8. Diagnostics you are likely to meet

Every rejection names a code, the file and a JSON-pointer-ish location. The ones
worth recognising:

| Code | What happened |
|---|---|
| `course_manifest_missing` | no `course.yaml` at the root |
| `manifest_path_invalid` | a manifest is at the wrong depth or in the wrong directory |
| `unknown_key` | a key not in the contract — usually a typo or a field from another camp |
| `unsupported_schema_version` | `schema_version` is not the integer `1` |
| `duplicate_content_id` | a `content_id` appears twice; usually a copied template |
| `invalid_content_id` | not a canonical lowercase UUID |
| `source_path_missing` | a manifest points at a file that is not in the commit — the classic half-done move |
| `invalid_repository_path` | a path with `..`, a leading `/`, a backslash or a URL scheme |
| `cohort_identifier_path_mismatch` | `identifier` disagrees with the directory name |
| `cohort_course_mismatch` | `cohort.yaml:course` disagrees with `course.yaml:slug` |
| `module_cohort_mismatch` / `homework_cohort_mismatch` | a cohort's flow reaches into another cohort |
| `module_slug_path_mismatch` / `unit_slug_path_mismatch` | a declared slug disagrees with the path |
| `unreferenced_homework_manifest` | a `homework.yaml` no flow points at |
| `duplicate_homework_slug` | two homeworks share a slug inside one cohort |
| `lesson_frontmatter_unclosed` | a `---` block that never closes |
| `lesson_video_url_invalid` | `video_url` is not an https YouTube URL |
| `course_description_source_required` | neither or both of `description` / `description_path` |
| `invalid_hashtag` | a leading `#` or a character outside `[A-Za-z0-9_]` |

A rejected import is safe: the previous import keeps serving. The cost is stale
content and a red run, so the way to avoid it is to run the checker before
pushing.
