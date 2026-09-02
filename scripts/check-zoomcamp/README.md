# check-zoomcamp

Conformance checker for course repositories. It reads a checkout and reports
every place the repo disagrees with [`STRUCTURE.md`](../../STRUCTURE.md) and
[`docs/curriculum-contract.md`](../../docs/curriculum-contract.md), with the
rule ID, the file and the line.

It is the early, friendly gate. **The website's ingestion parser is the
authority** — it fails loudly on push and leaves the previous import serving.
This script exists so that failure almost never happens: a contributor should
hear "your unit has no H1" on the pull request, minutes after pushing, not from
a rejected production import hours after merge. If the two disagree, the parser
is right and this script has a bug.

## Run it

```bash
# from a course repository checkout, without cloning this repo
uv run https://raw.githubusercontent.com/DataTalksClub/zoomcamp-template/main/scripts/check-zoomcamp/check_zoomcamp.py .

# or from a local clone of zoomcamp-template
uv run check_zoomcamp.py ~/git/llm-zoomcamp
```

`uv` handles the one dependency (PyYAML) through the script's inline metadata;
there is nothing to install and no lockfile to keep in sync.

Useful flags:

| Flag | Effect |
|------|--------|
| `--phase {1,2,3}` | how strict: 1 layout, 2 unit shape, 3 derived contract. Defaults to `phase:` in `.zoomcamp-check.yaml`, else 1. |
| `--warn-only` | report everything, exit 0. For the adoption window. |
| `--format github` | emit `::error file=…` annotations for GitHub Actions. |
| `--json` | machine-readable findings. |
| `--rules` | print the rule catalogue and exit. |

Exit codes: `0` no errors, `1` at least one error, `2` the checker could not run.

## In CI

Course repositories adopt it by reference, never by copy: copy
[`templates/workflows/curriculum-check.yml`](../../templates/workflows/curriculum-check.yml)
into `.github/workflows/` and pin the SHA. The reusable workflow takes the
checker from the same commit the caller pinned, so the rules and the workflow
are always the same version.

## Configuration

Optional `.zoomcamp-check.yaml` at the course repository root:

```yaml
phase: 1
allow:
  - rule: L007
    path: cohorts/2026/08-deep-learning/install.md
    reason: "frozen slug: published as /modules/08-deep-learning/install"
```

`allow` is the grandfather list. Conventions bind forward and published slugs
are frozen, so a repository will have a few files that are correct-because-live
and wrong-because-old. Recording them here — with a reason, in review — is how
the exception stays visible instead of being rediscovered by whoever "fixes" it
and breaks a public URL. An entry that stops matching anything is reported
(`C002`) so the list decays.

## Working on the checker

```bash
uv run test_check_zoomcamp.py
```

`fixtures/conformant/` is a repository that follows the convention;
`fixtures/violations/` breaks one rule at a time on purpose. The test asserts
the exact multiset of findings from each, at each phase, so a rule that starts
firing more or less than intended fails here rather than in a course repo's pull
request. It also asserts that every rule ID appears in `STRUCTURE.md`: a rule
the spec does not state is a rule that should not exist.

Adding a rule means, in one commit: the rule in `check_zoomcamp.py`, the
expectation in the fixture and test, and the sentence in `STRUCTURE.md` that
makes it a convention rather than a preference.

## Rules that must never fail a build

Some rules describe the convention's end state but depend on a website change
that has not shipped. `U006` (video to frontmatter) and `U009` (homework H1) are
in that state: acting on either today makes a published page worse. They are
class `pending`, they are warnings at every phase, the self-test asserts they can
never become errors, and their messages say what has to ship first.

`U011` (title ordinal prefixes) used to be the third. It left the class when the
owner settled the question — ordering lives in the filename prefix and titles
carry no ordinal — because what it was blocked on was a decision, not code. It is
class `content` now: warning at phase 1, error from phase 2. `U006` and `U009`
are still blocked on real code, and the self-test asserts the `pending` class is
exactly those two so neither is promoted by accident.

This class exists because the first version of this checker reported 205
findings against machine-learning-zoomcamp that were all of this kind, on a repo
that had just been carefully fixed. A checker whose loudest advice would break
production is one people learn to ignore. If you add a rule, ask what happens to
a contributor who does exactly what it says, today, and put it in `pending` if
the answer is "a worse page".

`U006`, the one bulk pending rule left, reports **once per cohort** with a count
and an example, not once per file, for the same reason: a hundred identical
warnings about one blocked migration teaches people to ignore the report. A rule
with an actionable per-file fix — `U011` now — reports per file, with the line,
so the annotation lands where the edit goes.

Note that `fixtures/conformant/` still produces *warnings* at phase 1. Those are
the retired knobs — `cohort.yaml` identity, `units`, `instructions_path`,
`description_path` — which the deployed parser still requires. That gap is real
and documented in `docs/curriculum-contract.md`; it closes when the parser
stops requiring them.
