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


def findings(path: Path, phase: int = 1) -> list:
    repo = check.Repo(root=path, files=check.collect_files(path))
    checker = check.Checker(repo=repo, phase=phase)
    checker.run()
    return [(checker.severity(f), f.rule) for f in checker.findings]


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
        ("warning", "M012"): 1,  # declared title disagrees with the H1
        ("warning", "U002"): 1,  # H2-as-title, with its own numbering
        ("warning", "U003"): 1,  # second H1 in the body
        ("warning", "U004"): 1,  # images%2F URL-encoded separator
        ("warning", "U005"): 4,  # escapes the cohort, and three dead links
        ("warning", "U006"): 1,  # YouTube URL in the body
        ("warning", "U008"): 1,  # navigation furniture
        ("warning", "U009"): 1,  # homework.md opens with an H2
    },
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
