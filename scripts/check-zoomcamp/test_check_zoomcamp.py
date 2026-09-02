#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Self-test for check-zoomcamp: the rules must not land broken.

Run it from this directory:

    uv run test_check_zoomcamp.py

It checks the two fixture repositories under `fixtures/` and asserts the exact
set of findings each one produces. A rule change that fires more or less than
intended fails here rather than in a course repository's pull request.
"""

from __future__ import annotations

import collections
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("check_zoomcamp", HERE / "check_zoomcamp.py")
assert spec and spec.loader
check = importlib.util.module_from_spec(spec)
sys.modules["check_zoomcamp"] = check
spec.loader.exec_module(check)


def raw_findings(path: Path, phase: int = 1) -> list:
    repo = check.Repo(root=path, files=check.collect_files(path))
    checker = check.Checker(repo=repo, phase=phase)
    checker.run()
    return [(checker.severity(f), f.rule, f.path) for f in checker.findings]


def findings(path: Path, phase: int = 1) -> list:
    return [(severity, rule) for severity, rule, _path in raw_findings(path, phase)]


def counts(path: Path, phase: int = 1) -> dict[tuple[str, str], int]:
    return dict(collections.Counter(findings(path, phase)))


FAILURES: list[str] = []


def expect(label: str, actual, wanted) -> None:
    if actual == wanted:
        print(f"ok   {label}")
    else:
        print(f"FAIL {label}\n     expected {wanted}\n     actual   {actual}")
        FAILURES.append(label)


# A repository that follows the convention has zero errors. It still carries
# warnings, because the deployed website parser REQUIRES the very keys the
# convention retires (cohort identity, instructions_path, description_path,
# the units list). Those warnings are the Phase 3 to-do list, not defects --
# see docs/curriculum-contract.md.
expect(
    "conformant fixture, phase 1",
    counts(HERE / "fixtures" / "conformant"),
    {
        ("warning", "M009"): 1,  # description_path -> fixed-name SITE.md
        ("warning", "M004"): 1,  # cohort identity restated in YAML
        ("warning", "M011"): 2,  # units list restates the files on disk
        ("warning", "M008"): 2,  # instructions_path restates homework.md
    },
)

expect(
    "violations fixture, phase 1",
    counts(HERE / "fixtures" / "violations"),
    {
        ("error", "L002"): 1,  # module.yaml at the repo root
        ("error", "L004"): 1,  # numbered directory at the repo root
        ("error", "L006"): 1,  # stray markdown in a module directory
        ("error", "L007"): 2,  # lessons/ subdirectory, and the unit inside it
        ("error", "L008"): 1,  # homework.yaml without homework.md
        ("error", "L009"): 1,  # module without a README index
        ("error", "L010"): 1,  # no SITE.md
        ("error", "M002"): 1,  # content_id reused across two manifests
        ("error", "M005"): 1,  # module with no flow entry
        ("error", "M006"): 1,  # markdown file missing from the units list
        ("error", "U001"): 2,  # unknown frontmatter key, non-YouTube video_url
        ("warning", "L011"): 1,  # no cohorts/README.md
        ("warning", "M004"): 1,
        ("warning", "M007"): 1,  # module slug restates the directory
        ("warning", "M008"): 2,  # bad instructions_path, and the retired key
        ("warning", "M009"): 1,  # inline description instead of SITE.md
        ("warning", "M010"): 1,  # homework-01 instead of the derived hw01
        ("warning", "M011"): 2,
        ("warning", "M012"): 2,  # title drift, and the ordinal-only drift
        ("warning", "U002"): 1,  # H2 instead of an H1 title
        ("warning", "U003"): 1,  # second H1 in the body
        ("warning", "U004"): 1,  # images%2F URL-encoded separator
        ("warning", "U005"): 4,  # escapes the cohort, and three dead links
        ("warning", "U006"): 1,  # one per cohort, not one per unit
        ("warning", "U008"): 1,  # navigation furniture
        ("warning", "U009"): 1,  # homework.md opens with an H2
        ("warning", "U011"): 1,  # 02-kept-ordinal.md: title still numbered
    },
)

# U011's fix edits two files, and doing half of it puts the title on the page
# twice. 02-kept-ordinal.md is the un-migrated unit (U011, both sides agree);
# 03-stripped-ordinal.md is the half-migrated one (M012, and NOT U011, because
# its H1 is already clean). Exactly one finding each, and the half-migrated
# state is the one that names the duplicate-title hazard.
expect(
    "un-migrated unit is U011, half-migrated unit is M012",
    sorted(
        (rule, path.rsplit("/", 1)[-1])
        for _severity, rule, path in raw_findings(HERE / "fixtures" / "violations")
        if rule in {"U011", "M012"}
    ),
    [
        ("M012", "01-drift.md"),
        ("M012", "03-stripped-ordinal.md"),
        ("U011", "02-kept-ordinal.md"),
    ],
)

# Rules that describe an end state the website cannot serve yet are never
# errors, at any phase. A checker that tells a contributor to move a video to
# frontmatter or promote a homework heading TODAY is telling them to break a
# published page -- see the PENDING note in check_zoomcamp.py. This assertion
# is the guard on that.
#
# Membership is asserted explicitly so a rule cannot drift into or out of the
# class by accident. U011 left it when the owner settled the ordinal question --
# what it was waiting on was a decision, not code. U006 and U009 are still
# blocked on website code that has not shipped (the importer drops frontmatter
# video_url; the homework page has no leading-heading strip), so they stay.
expect(
    "pending class is exactly the rules still blocked on the website",
    sorted(rule for rule, (rule_class, _) in check.RULES.items() if rule_class == check.PENDING),
    ["U006", "U009"],
)

for _phase in (1, 2, 3):
    expect(
        f"pending rules never become errors at phase {_phase}",
        sorted(
            {
                rule
                for (severity, rule) in counts(HERE / "fixtures" / "violations", phase=_phase)
                if severity == "error" and check.RULES[rule][0] == check.PENDING
            }
        ),
        [],
    )

# Phase 2 turns the unit-shape warnings into errors; phase 3 does the same for
# the retired knobs. The conformant fixture therefore fails at phase 3 until
# the website parser stops requiring them -- that is the intended signal.
conformant_phase3 = counts(HERE / "fixtures" / "conformant", phase=3)
expect(
    "conformant fixture, phase 3 turns knobs into errors",
    {rule for (severity, rule) in conformant_phase3 if severity == "error"},
    {"M004", "M008", "M009", "M011", "U010"},
)

expect(
    "violations fixture, phase 2 turns content warnings into errors",
    sum(n for (severity, _), n in counts(HERE / "fixtures" / "violations", phase=2).items()
        if severity == "error"),
    24,
)

# U011 is a real convention now, so the phase model gates it like any other unit
# shape rule: a warning at phase 1 while a repo is being normalized, an error
# once it declares phase 2. Stripping an ordinal is safe against the deployed
# site -- M012 is what keeps the two sides moving together.
expect(
    "U011 is a warning at phase 1 and an error from phase 2",
    [
        severity
        for phase in (1, 2, 3)
        for (severity, rule) in counts(HERE / "fixtures" / "violations", phase=phase)
        if rule == "U011"
    ],
    ["warning", "error", "error"],
)

# An allowance in .zoomcamp-check.yaml suppresses exactly one rule at exactly
# one path, and an allowance that matches nothing is reported so the list decays.
with tempfile.TemporaryDirectory() as raw:
    tmp = Path(raw) / "repo"
    shutil.copytree(HERE / "fixtures" / "violations", tmp)
    (tmp / ".zoomcamp-check.yaml").write_text(
        "phase: 1\n"
        "allow:\n"
        "  - rule: L007\n"
        "    path: cohorts/2026/01-intro/lessons/01-intro.md\n"
        '    reason: "frozen slug: the published URL is /modules/01-intro/01-intro"\n'
        "  - rule: L009\n"
        "    path: nothing/here/README.md\n"
        '    reason: "stale entry that should be reported"\n',
        encoding="utf-8",
    )
    allowed = counts(tmp)
    expect("allowance suppresses one L007", allowed.get(("error", "L007")), 1)
    expect("stale allowance is reported", allowed.get(("warning", "C002")), 1)

# Every rule the checker can emit must be in the catalogue, and every rule in
# the catalogue must be documented in STRUCTURE.md.
structure = (HERE.parent.parent / "STRUCTURE.md").read_text(encoding="utf-8")
undocumented = sorted(rule for rule in check.RULES if rule not in structure)
expect("every rule appears in STRUCTURE.md", undocumented, [])

print()
if FAILURES:
    print(f"{len(FAILURES)} check(s) failed")
    sys.exit(1)
print("all checks passed")
