# Bootstrap or archive a Zoomcamp cohort

`bootstrap_cohort.py` is a local, filesystem-only helper for the v2 shared
curriculum layout. It never calls Git/GitHub, the website, or the course
management platform; it never commits, pushes, deletes root material, or
rewrites code. It is read-only unless the explicit `--apply` flag is present.

The command is read-only unless the explicit `--apply` flag is present. Every
requested destination is checked before the first write. A destination that
already contains different bytes is a refusal; an exact previous result is a
no-op, so a successful operation can be safely replayed.

Use `uv` to run it:

```bash
uv run scripts/bootstrap-cohort/bootstrap_cohort.py bootstrap \
  /path/to/llm-zoomcamp --cohort 2027 --delivery live \
  --request /path/to/bootstrap-2027.yaml
```

Review the complete plan, then apply that same command only after reviewing
it:

```bash
uv run scripts/bootstrap-cohort/bootstrap_cohort.py bootstrap \
  /path/to/llm-zoomcamp --cohort 2027 --delivery live \
  --request /path/to/bootstrap-2027.yaml --apply
```

The command also accepts `--repo-root PATH` in place of the positional
repository path. `bootstrap` may be omitted; a command beginning with a repo
path or an option is treated as a read-only bootstrap plan. `plan` is an
explicit alias for that default. `--json` emits only paths, actions, checks
and counts, never Markdown, YAML bodies, prompts, answer material, tokens or
personal data.

The exact command forms are:

```text
bootstrap REPO --cohort ID --delivery live|self-paced
  [--request REQUEST.yaml] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
  [--apply] [--json]
archive REPO --cohort ID [--archive-id ID] [--archive-manifest FILE]
  [--delivery live|self-paced] [--module NN-module ...] [--apply] [--json]
```

## Bootstrap request

The request is YAML with schema version `2`:

```yaml
schema_version: 2
cohort:
  id: "2027"
  delivery: live                 # live | self-paced (emits self_paced)
  title: LLM Zoomcamp 2027
  description: A live delivery of the current curriculum.
  start_date: 2027-06-07        # optional; never inferred or copied
  end_date: 2027-10-11           # optional; never inferred or copied
  readme: |                      # optional replacement for generated README
    # LLM Zoomcamp 2027

modules:
  - slug: 01-agentic-rag
    homework:
      slug: homework-01
      title: "Homework 1: Agentic RAG"
      instructions: |
        # Homework 1: Agentic RAG

        Write the reviewed assignment instructions here.
      # Do not provide content_id; the tool mints a new deterministic ID.
      due_at: 2027-07-01T21:59:00Z
      initial_state: open
      form:
        homework_url: true
        time_spent_lectures: true
        time_spent_homework: true
        faq_contribution: true
        learning_in_public_cap: 7
      questions:
        - id: q1
          type: free_form_long
          prompt: What did you learn?
          answer_type: any
          points: 0
  - slug: 02-vector-search
    # No `homework` means this delivery has no assignment for this module.
```

Self-paced bootstrap is currently practice-only and always emits
`homework: []`; authored graded homework is refused until its policy is
defined. For live assignments, every new homework manifest must author a real
`due_at`, `initial_state`, all five `form` fields, and at least one question.
Non-`any` questions also require the website's complete encrypted answer
envelope; plaintext answer-key fields are rejected. There is no source-cohort
option and no inherited deadlines, grading, points, questions or answers.
Custom `graded`/`points` assignment keys are not emitted.

For one-module requests, a top-level `homework:` mapping is also accepted. A
multi-module request may use a mapping keyed by module slug or a list whose
entries include `module` and the assignment fields. The explicit per-module
form above is preferred because omission is visibly “no assignment”.

If `modules` is omitted, the tool discovers all direct root directories named
`NN-kebab-name`. Each must contain a `module.yaml` and at least one numbered
lesson file named `NN-kebab-name.md`. The tool reads module IDs and titles only
to create references; it never copies or edits those files. In a request,
`modules` lists only modules whose homework is authored; the current root graph
is always referenced in full. The bootstrap `--module` option is intentionally
rejected; use request mappings for assignment authoring.

Bootstrap writes only:

```text
cohorts/<id>/cohort.yaml
cohorts/<id>/README.md
cohorts/<id>/homework/<module>/homework.md
cohorts/<id>/homework/<module>/homework.yaml
```

The last two files are written only for assignments explicitly present in the
request. The website discovers the shared root module manifests; the cohort
manifest carries no duplicated current module list. No lesson, image, notebook
or code file appears under the new cohort. The new cohort and assignment IDs are fresh UUIDs derived
from the course ID and their stable request identity. This makes planning and
replay deterministic while still refusing a collision with any existing ID.

The root `course.yaml` must already be schema v2. A v1 checkout is refused with
`migration_required`; this script does not migrate it. The tool refuses a
non-archived `cohorts/*/*/module.yaml` before inspecting or writing a bootstrap
destination. Each selected root module must be `NN-kebab/module.yaml` with
schema v2 and at least one numbered lesson sibling.

The v2 cohort manifest has `identifier` equal to its directory, `course` equal
to `course.yaml:slug`, `curriculum: current`, `published: false`, explicit
`start_date`/`end_date` (null is allowed), and a homework list whose only keys
are `module` and full repository-relative `source` paths. Root module and
lesson IDs are preserved and shared files are referenced, never copied.

## Archive an outgoing curriculum

Archiving is a separate operation. Run it before replacing the root modules:

```bash
uv run scripts/bootstrap-cohort/bootstrap_cohort.py archive \
  /path/to/llm-zoomcamp --cohort 2026

uv run scripts/bootstrap-cohort/bootstrap_cohort.py archive \
  /path/to/llm-zoomcamp --cohort 2026 --apply
```

By default every numbered root module is selected. Use `--module` repeatedly,
or an archive request (`--archive-manifest PATH`), to select modules explicitly.
The optional `--delivery` value is used only when creating a new archive
manifest; an existing v2 cohort's delivery is retained:

```yaml
schema_version: 2
modules:
  - 01-agentic-rag
  - 02-vector-search
```

The archive is additive and lands at:

```text
cohorts/<id>/cohort.yaml       # curriculum: github_archive
cohorts/<id>/README.md         # archive notice with local links
cohorts/<id>/archive.yaml      # checksum/provenance evidence
cohorts/<id>/<NN-module>/...   # full module tree, byte-for-byte
```

`cohort.yaml` is created or narrowly switched to `curriculum: github_archive`,
retaining an existing v2 cohort's delivery, dates, publication and homework
fields. Its archive metadata is exactly
`archive: {notice_path: cohorts/<id>/README.md}`; it does not invent a future
commit or URL. The website can derive an immutable archive URL from the
incoming source commit. A v1 cohort manifest is a migration prerequisite.

`archive.yaml` records the selected module list and SHA-256 checksums for each
copied file. Images, notebooks, code and other local assets are included. An
existing authored README is preserved and receives one managed archive notice
section; existing homework and other delivery files remain untouched. No
generic regex rewrite is performed. Markdown and HTML links are checked before
any write:

- same-module links must resolve to files in that module;
- links to another selected root module are preserved because the relative
  module layout is unchanged;
- links to an unselected module, repository root, external local tree, missing
  file, unsafe path or same-repository moving GitHub/raw URL are refused.

Symlinks, special files, traversal, absolute paths, URL-encoded separators and
conflicting destination files are rejected. The root curriculum is never
deleted or changed; no code or Markdown is rewritten. Unknown files inside a
selected archived module are a conflict rather than an implicit overwrite.

Exit codes are `0` for a valid plan/no-op/apply, `1` for a safety or schema
refusal, and `2` when required command arguments or the repository root are
missing.

## Tests

Fixtures are created in a temporary directory by the test itself; no real
course checkout is modified. Run:

```bash
mkdir -p .tmp
uv run --with pytest --with pyyaml pytest \
  --basetemp=.tmp/bootstrap-cohort-test -q \
  scripts/bootstrap-cohort/test_bootstrap_cohort.py
```

The tests cover read-only planning, exact replay, fresh IDs and references,
v1 migration refusal, symlink/traversal/overwrite safety, complete asset and
cross-module archive closure, unsafe dependency refusal, archive classification,
encrypted-answer validation, and the guarantee that root curriculum files
survive an archive unchanged.
