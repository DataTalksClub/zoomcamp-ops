# Shared curriculum rollout

Status: implementation in progress for local operations tooling. Website work
is tracked in [DataTalksClub/website#320](https://github.com/DataTalksClub/website/issues/320).
This document is a delivery plan, not evidence that a proposed website feature
already exists. The website's `_docs/PROCESS.md` still governs each code slice.

## Accepted product decisions

- Keep current modules at repository root, with required numeric prefixes:
  `01-agentic-rag/01-retrieval-augmented-generation.md`.
- Use the corresponding website hierarchy:
  `/courses/llm-zoomcamp/01-agentic-rag/01-retrieval-augmented-generation`.
- Keep live and self-paced delivery operations beneath explicit cohort routes,
  such as `/courses/llm-zoomcamp/cohorts/2026/homework/homework-01`.
- Create a cohort by referencing shared current content, not copying it.
- Preserve materially different outgoing teaching material in GitHub under
  `cohorts/<identifier>/`, including code, notebooks, images and internal links.
  The website links to that archive and keeps historical cohort operations; it
  does not serve another versioned lesson site.
- Keep assignment identities, submissions, grading, enrollment and certificate
  history attached to the cohort that owns them. Do not infer assignment
  bindings from matching numeric prefixes.
- Preserve the full declared LLM course slug. Other courses retain their
  reviewed published slugs; this project is not permission to rename every
  course to its repository name.
- Reading stays public. Selecting a cohort changes browsing context, not
  authorization or the shared lesson body.

The initial self-paced scope is reading, persistent lesson progress and
practice. Graded self-paced submissions, rolling deadlines, certificates and
peer review require a separate product policy. Do not fabricate dates to make
existing live-cohort models accept a self-paced delivery.

## Repository ownership and order

| Repository | Owns | Must not do |
| --- | --- | --- |
| `DataTalksClub/zoomcamp-ops` | Bootstrap/archive command, skill, authoring contract, checker, templates, this rollout plan | Write the website database or silently publish a course |
| `DataTalksClub/website` (local `dtc-website`) | Source admission, database projection, cohort operations, public routes, context, SEO and redirects | Read public content from repository files at request time |
| Each Zoomcamp repository | Current teaching material, cohort-specific public assignments, GitHub archives | Convert to v2 before consumer/checker compatibility passes |

The remote formerly named `DataTalksClub/zoomcamp-template` was renamed to
`DataTalksClub/zoomcamp-ops` during this work. Reusable workflow references must
use the new name and a reviewed commit pin. Keep old links readable through the
GitHub rename redirect; do not assume reusable workflow callers are fixed by a
web redirect.

## Producer/consumer contract decisions

Schema v2 is an explicit opt-in. A v1 root manifest continues through the v1
parser and checker without silently acquiring v2 semantics. Current root module
and cohort manifests use v2 together. The bootstrap command refuses a v1 input
instead of promoting old cohort-owned modules automatically.

A cohort declares a string identifier, course slug, delivery (`live` or
`self_paced`), curriculum (`current` or `github_archive`), publication state,
dates, and an explicit homework list. Empty homework lists are valid for new
drafts and self-paced practice. New homework paths are repository-relative
`cohorts/<id>/homework/<module>/homework.yaml`; existing archive homework may
retain its old location through an explicit mapping. The assignment's stable
identity belongs in its manifest, not in a duplicate mapping field.

An archive declares a `notice_path` in its cohort tree. The website derives
its immutable GitHub destination from the validated source repository and the
incoming source commit. Do not require a newly created archive manifest to name
the future commit that will contain that manifest.

Archived module/lesson manifests may preserve original IDs. Classify archives
before registering the active teaching graph so those IDs are not interpreted
as new current lessons. Explicitly mapped historical homework/questions remain
operational and participate in normal identity validation. Archive exclusion
does not exempt files from transport path, symlink or size admission.

The full field contract and conformance examples belong in
`docs/shared-curriculum-v2.md`. CLI/request details belong in
`scripts/bootstrap-cohort/README.md`; do not maintain a second command reference
inside this plan or the skill.

## Execution protocol for every implementation agent

1. Read the owning issue, its acceptance criteria, the current contract, and
   the exact files assigned to you. Check Git status and preserve other work.
2. Confirm that prerequisite task evidence exists. A draft plan or generated
   fixture is not evidence that its website consumer is implemented.
3. Make only the assigned change. If an interface needs to change, coordinate
   with its owner before updating fixtures or producers to match an invention.
4. Run the named focused checks and the repository-required verification plan.
   Use `uv` for Python and project-local `.tmp/` for scratch data.
5. Report modified paths, exact commands/results, interface changes and remaining
   failures. Do not claim a proposed acceptance criterion as implemented.
6. Freeze the candidate for independent testing. In the website repository,
   tester and PM acceptance precede commits/merge/push; on-call owns CI watching.

No agent may move real course material merely to make a local checker pass.
Rehearse source changes in a disposable clone and a synthetic/content-only test
database first. Never read or copy production learner data for these tests.

## Local tooling acceptance

Bootstrap must preview without writing, create only the requested unpublished
cohort and explicitly authored assignments, retain shared lesson IDs and bytes,
and replay an identical request without generating another identity. Invalid
schema, duplicate IDs, traversal, symlinks and conflicting destinations refuse
before writes. A failed apply restores all changed files.

Archive must preserve complete selected module trees and verify supported local
link dependencies, including cross-module navigation. It must refuse unsupported
dependencies with an actionable diagnostic rather than claim a complete archive.
It preserves authored cohort prose and existing homework, provides a usable
archive index, changes the cohort's curriculum classification explicitly, and
leaves the root teaching material in place until replacement is reviewed.

Run the v1 checker assertions, v2 positive/negative checks, bootstrap suite and
a generated-bootstrap-output-to-checker integration test. Forward-test the skill
with a fresh agent using only the skill and a disposable course fixture. Confirm
that the agent uses preview/apply correctly, does not copy lessons for a new
cohort, and identifies the v1 migration prerequisite.

## Source replacement and deployment gates

Before replacing a current curriculum, enumerate every current-linked delivery,
including self-paced. Explicitly decide which are still compatible with the
replacement and which require an archive. Do not leave a self-paced enrollment
pointing to incompatible new assignment prerequisites because only the live
cohort was considered.

The safe order is contract fixtures, dual consumer/checker support, shared
database projection and UI/route tests, rehearsal, then one real source migration
at a time. Source publication must not precede the consumer that understands it.
Preserve a last-good import and a tested route/source rollback. Keep v1 support
until all registered sources and compatibility consumers have been inventoried
and the retirement is separately approved through its owning issue.

## Website implementation tickets

The [detailed website implementation plan](website-shared-curriculum-implementation.md)
contains the concrete model/service interfaces, W0-W10 task files, acceptance
criteria, commands, browser scenarios and dependency graph. Read it before
selecting a website implementation slice. Code and command paths introduced by
a ticket are deliverables of that ticket, not tools that already exist.

The first website slice is W0: resolve the currently conflicting specifications
and freeze the route/compatibility contract. W1 then adds the dual parser and
the known-output consumer fixture. Neither source movement nor publishing the
new operations producer is a substitute for those consumer tasks.

Review corrections applied while integrating the PM plan:

- The bootstrap script writes source files only; the importer writes website
  rows. There is no direct script-to-production-database path.
- Old mutation endpoints keep direct compatibility adapters during client
  migration. Moving an HTML page must not turn an existing homework POST into
  a 405 or redirect its body.
- Shared read-state reconciliation retains the earliest known read timestamp,
  matching the existing first-read behavior.
- Database uniqueness/check constraints and service-level cross-FK ownership
  validation are separate checks; Django constraints cannot silently perform
  cross-table joins.
- Initial v2 project operations remain cohort-owned; a new interleaved project
  flow requires an explicit source-contract extension rather than guessed order.
- Initial sitemap entries are course/current module/current lesson pages.
  Context variants use private/no-store; these are settled initial defaults.

## Website rehearsal of the schema-2 move (2026-09-08)

A scratch copy of `llm-zoomcamp` (HEAD `c16eb587…`) was transformed to the v2
layout and checker-gated at commit `a7227d6aba0a77ddd1b2152007144838074ab5b3`
(never pushed): the v2 checker passes with 0 findings and the website's
release gate plus database import both accept it. The first pass surfaced 41
findings; the real move must apply five mechanical fix classes: drop
`description_path`/`overview_path` manifest keys, quote homework `due_at`
values, relocate `07-project-example/content-processing-summary.md` to
`docs/`, strip trailing slashes on in-module directory links, and rewrite
module-escaping links (archive cross-links, `../../../project.md`,
`homework.md`) to their GitHub main-branch URLs. Existing content IDs carry
over verbatim; the three new cohorts use deterministic UUIDv5 IDs recorded in
the website rehearsal notes.

## Website rehearsal of the schema-2 move (2026-09-08)

A scratch copy of `llm-zoomcamp` (HEAD `c16eb587…`) was transformed to the v2
layout and checker-gated at commit `a7227d6aba0a77ddd1b2152007144838074ab5b3`
(never pushed): the v2 checker passes with 0 findings and the website's
release gate plus database import both accept it. The first pass surfaced 41
findings; the real move must apply five mechanical fix classes: drop
`description_path`/`overview_path` manifest keys, quote homework `due_at`
values, relocate `07-project-example/content-processing-summary.md` to
`docs/`, strip trailing slashes on in-module directory links, and rewrite
module-escaping links (archive cross-links, `../../../project.md`,
`homework.md`) to their GitHub main-branch URLs. Existing content IDs carry
over verbatim; the three new cohorts use deterministic UUIDv5 IDs recorded in
the website rehearsal notes.
