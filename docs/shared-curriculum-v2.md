# Shared curriculum contract (schema v2)

Schema v2 makes the repository root the single source for the current teaching
graph. It is an opt-in contract; a repository whose root `course.yaml` says
`schema_version: 1` remains on the v1 parser/checker until its migration is
reviewed.

## Source layout

```text
course.yaml
NN-module/module.yaml
NN-module/NN-lesson.md
cohorts/README.md
cohorts/<id>/cohort.yaml
cohorts/<id>/README.md
cohorts/<id>/homework/NN-module/homework.yaml
cohorts/<id>/homework/NN-module/homework.md
```

`NN-module` and `NN-lesson.md` are numbered kebab-case names. Lesson files are
siblings of `module.yaml`; `README.md` is a GitHub index and `images/` and
`code/` are module-local assets. A module manifest keeps the v1-compatible
`units: [{content_id, title, path}]` representation in the first v2 slice.
The module and every unit have a canonical, quoted UUID `content_id` which is
never reused or silently rebound.

**Modules are discovered, never listed.** `course.yaml` does not enumerate
its modules. The current module set is every `NN-kebab-name/` directory at
the repository root that contains a `module.yaml`, ordered by its numeric
prefix; a root directory without one (a draft, or content not yet wired in,
like ml-zoomcamp's `11-kserve` today) is simply not part of the curriculum
yet. This is deliberate, not an omission: a declared list in `course.yaml`
would duplicate what the filesystem already states unambiguously and could
drift from it the moment someone adds a module directory and forgets to
update the list, with nothing to catch the mismatch. It is the same reasoning
that retires `cohort.yaml`'s old `flow` list, `slug`/`title` restatement on
units, and `SITE.md`'s pointer — one fact, one place.

## File placement and website treatment

What each file becomes once it is pushed, not just where it sits:

- **A lesson `NN-lesson.md`** is the only file that becomes rendered content.
  Its frontmatter (`video_url`, `code`) is parsed and stripped; the remaining
  body becomes the unit's page. The filename stem is the unit's URL slug,
  never a declared `slug` field.
- **`images/` is never imported.** A unit's `![alt](images/foo.png)` reference
  is resolved at render time to
  `raw.githubusercontent.com/<org>/<repo>/<commit-sha>/<module>/images/foo.png`
  — no image bytes are copied into the website's database or storage. The
  same holds for `code:` frontmatter entries pointing into a module's
  `code/`/`notebooks/` directory.
- **`README.md` is GitHub-facing decoration, with one exception.** The root
  `README.md`, every module `README.md`, and a *current* cohort's
  `README.md` are never read by the website's importer — they exist only for
  someone browsing the repository on GitHub. The **one** exception is an
  archived cohort's `README.md`, which the website does read, but only as an
  address: `cohort.yaml`'s `archive.notice_path` points at it so the site can
  render a "view the original material on GitHub" link. It is never parsed
  for content.
- **The course description lives inline in `course.yaml:description`**,
  not in a separate file. v1's `SITE.md` + `description_path` pointer is
  retired in v2: one course-identity fact belongs in the one manifest that
  already carries the rest of the course's identity, not split across a
  manifest and a fixed-name file. Never point a description at `README.md`.
- **Homework stays paired but separate from curriculum.** `homework.yaml` and
  its sibling `homework.md` live under `cohorts/<id>/homework/<module>/`,
  one pair per module with an assignment — never folded into `cohort.yaml`
  (homework is authored and reviewed per module, so a shared file would be a
  standing merge-conflict hotspot) and never sitting inside the shared root
  module directory (homework is per-delivery, the module content is not).

## Course and cohort manifests

The v2 course manifest keeps the existing course identity fields and adds one:

```yaml
schema_version: 2
content_id: "7736c1e6-5d66-4286-8180-b1eef3f83a84"
slug: llm-zoomcamp
title: LLM Zoomcamp
current_cohort: "2027"
description: |
  LLM Zoomcamp is a free, hands-on course on building and operating
  production-style LLM applications.

  Across its modules you work through retrieval, agentic workflows,
  evaluation, and monitoring, then deploy what you build.
outcome: Build and operate production-style LLM applications.
urls:
  repository: https://github.com/DataTalksClub/llm-zoomcamp
  docs: https://datatalks.club/docs/courses/llm-zoomcamp/
  faq: https://datatalks.club/faq/llm-zoomcamp.html
hashtag: llmzoomcamp
published: true
```

`urls` groups the three external links (`repository_url`, `docs_url`, `faq_url`
in v1) under one mapping instead of three separately-suffixed top-level keys —
they are one kind of fact (where to find things about this course), so they
sit together. Same three required sub-keys as before: `repository`, `docs`,
`faq`.

`current_cohort` is new in v2: it names which cohort directory the root
curriculum currently belongs to — the answer to "who is this content live
for right now" that used to be implicit in editing `cohorts/<year>/` directly.
It must equal the `identifier` of the one cohort whose `cohort.yaml` declares
`curriculum: current`; exactly one such cohort exists at a time. Bootstrapping
a new cohort and archiving the outgoing one (§ the bootstrap-cohort tool)
updates this field as part of the same change that switches which cohort is
current.

Every cohort manifest has an explicit delivery and curriculum discriminator:

```yaml
schema_version: 2
content_id: "94444444-4444-4444-8444-444444444444"
identifier: "2027"                 # native YAML string; equals the directory
course: llm-zoomcamp
delivery: live                     # live | self_paced
published: false
start_date: "2027-06-07"            # optional/null for an unpublished draft
end_date: "2027-10-11"
curriculum: current                # current | github_archive
homework:
  - module: 01-agentic-rag
    source: cohorts/2027/homework/01-agentic-rag/homework.yaml
```

`curriculum` is a scalar discriminator. `current` means every numbered root
module is discovered and shared; `github_archive` opts the cohort out of
website lesson ingestion. Live and self-paced cohorts therefore share one
module and lesson graph. `homework` is a required explicit list of
`{module, source}` mappings; `[]` is valid for a draft and for a cohort
without assignments. Self-paced phase one requires exactly `homework: []`;
a nonempty list is rejected (`self_paced_homework_rejected`), matching the
bootstrap producer's refusal to author self-paced assignments. New v2
homework uses the full
repository-relative path shown above. The checker validates that the YAML and
Markdown pair exists under the declaring cohort; it never discovers arbitrary
homework manifests by walking the tree. Existing archive homework may retain
the v1 direct path `cohorts/<id>/NN-module/homework.yaml` while it is being
converted. No mapping carries a second `content_id`: identity belongs to the
homework manifest itself.

Published live cohorts must have quoted ISO dates. Unpublished live drafts may
leave either date null. Self-paced practice has no generated deadline or
`due_at: null` grading convention in this first slice. If a live assignment is
mapped, its child homework manifest has a real `due_at`.

## GitHub-only historical archives

A materially different curriculum is kept complete for GitHub readers under
its cohort directory, but it is not a website lesson source:

```yaml
schema_version: 2
content_id: "95555555-5555-4555-8555-555555555555"
identifier: "2025"
course: llm-zoomcamp
delivery: live
published: true
start_date: "2025-05-05"
end_date: "2025-07-14"
curriculum: github_archive
archive:
  notice_path: cohorts/2025/README.md
homework:
  - module: null
    source: cohorts/2025/01-old-module/homework.yaml
```

`archive.notice_path` is the only archive metadata in the source manifest. It
must point to an existing Markdown notice inside that cohort. The website
derives the immutable GitHub URL from the validated source repository, the
incoming commit SHA and this path during import; a manifest cannot name its own
future commit. All archive descendants, including duplicate module/unit IDs,
are opaque and never become current module or lesson rows. Explicit `module: null`
homework mappings are still parsed and can remain operational for historical
submissions. An archive with no operational homework uses `homework: []`.

## Safety and checker

Run the checker with the same `uv`-backed command used in CI:

```bash
uv run --with pyyaml scripts/check-zoomcamp/check_zoomcamp.py PATH
```

The checker dispatches on the root schema before discovery. V2 rejects
duplicate YAML keys, implicit numeric identifiers, unknown fields, unbounded
values, traversal/absolute/URL-encoded paths, symlinks, missing module or
lesson pairs, duplicate numeric prefixes, missing archive notices, mixed
current/archive sources, and unreferenced current homework. Archive module
files are deliberately not loaded or ID-registered; only an explicitly mapped
archive homework manifest is admitted. Diagnostics contain repository paths and
YAML pointers, not lesson prose, answer material, tokens, registration data or
email addresses.

The existing v1 checker and manifests remain unchanged. A v2 failure is
atomic at import time: the website keeps the last successful projection and
does not fall back to another cohort, a README projection, or the newest
curriculum. Consumer projection and shared routes must be deployed and tested
before source repositories opt into schema v2.
