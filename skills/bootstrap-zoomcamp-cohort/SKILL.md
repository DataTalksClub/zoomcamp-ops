---
name: bootstrap-zoomcamp-cohort
description: Bootstrap a live or self-paced Zoomcamp cohort that references the current numbered root curriculum, or archive an outgoing curriculum in its cohort folder before replacement. Use for cohort setup and curriculum archival, not for writing lessons or grading homework.
---

# Bootstrap a Zoomcamp cohort

Use the deterministic command in `zoomcamp-ops/scripts/bootstrap-cohort/`.
Locate the zoomcamp-ops checkout first; do not confuse it with the target course
repository. When this skill is read in its source repository, the command folder
is `../../scripts/bootstrap-cohort/` relative to this file's directory. If the
skill was installed separately, locate the ops checkout and read the command's
README there. Do not download and execute a moving remote script.

Read the command README before invoking it. It owns the exact CLI, supported
source schema, and refusal codes. The website consumer must support the emitted
schema before generated changes are published to a course repository. A successful
local bootstrap is not proof of website import readiness.

## Choose the operation

- New live or self-paced delivery using the same teaching material: bootstrap a
  cohort reference. Do not archive or copy lessons just because the year changes.
- Replacing the teaching material: archive the outgoing curriculum for its named
  cohort before editing current lessons. Keep the current root files until the
  archive has been checked. Archival is a separate operation from cohort creation.
- Existing cohort-owned source layout: report the migration prerequisite. Do not
  treat creating a cohort as permission to move an existing repository's modules.

Preserve numbered root modules such as `01-agentic-rag/` and numbered lesson
files. Current website lesson paths have the form
`/courses/llm-zoomcamp/01-agentic-rag/01-introduction`; historical lessons are
read on GitHub under `cohorts/<identifier>/`. Cohort homework and learner
operations stay cohort-specific.

## Run the workflow

1. Inspect the target repository's instructions, Git status, `course.yaml`,
   current root modules and destination cohort. Establish the exact target
   identifier and live/self-paced mode from the request. Do not infer the cohort
   from the current calendar year. Ask only for missing inputs required by the
   chosen operation.
2. Run the command's default preview with `uv`. Inspect its full action list and
   diagnostics. Refusals are a reason to fix the named input, not to bypass the
   command with ad hoc file copies.
3. Apply only the requested operation using the documented explicit apply flag.
   Existing authorization to create/archive that cohort covers local apply;
   do not ask for the same permission again. Keep previews and test artifacts in
   the target project's `.tmp/`.
4. Inspect the resulting diff and run the command's documented validation. Check
   that a new delivery references the root modules without copying them, uses a
   new cohort identity, and remains unpublished. Shared module and lesson IDs
   remain unchanged. Do not invent assignment questions, deadlines, registration
   windows, grading policy, or certificate eligibility.
5. For an archive, follow local Markdown and image links, cross-module links and
   companion-code links in the archived tree. The old homework must continue to
   lead to compatible material. Unsupported dependencies must be resolved before
   replacing the current curriculum; an archive containing only Markdown is not
   sufficient.
6. Report created/updated paths, checks, and any remaining website/schema or
   editorial prerequisites. Commit, push, production import and deployment are
   separate actions and require authorization in the active task.

Never put learner registrations, submissions, credentials or plaintext answer
keys into the cohort tree or reports. Bootstrap must not copy enrollment,
scoring, peer-review or certificate state. Self-paced delivery must not inherit
live deadlines or claim grading/certificates that have not been configured.
