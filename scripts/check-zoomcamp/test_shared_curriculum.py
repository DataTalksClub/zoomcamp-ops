#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0", "pytest>=8.0"]
# ///
"""Focused v2 checker tests.

The v1 self-test intentionally remains a separate executable with its exact
fixture expectations.  These tests exercise the new dispatch and archive
boundary without changing those fixtures.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("check_zoomcamp_v2", HERE / "check_zoomcamp.py")
assert SPEC and SPEC.loader
check = importlib.util.module_from_spec(SPEC)
sys.modules["check_zoomcamp_v2"] = check
SPEC.loader.exec_module(check)

FIXTURE = HERE / "fixtures" / "shared-current-v2"
CHECKER = HERE / "check_zoomcamp.py"


def run_checker(path: Path):
    repo = check.Repo(root=path, files=check.collect_files(path))
    checker = check.checker_for_repo(repo, phase=1)
    checker.run()
    return checker


def rules(checker) -> set[str]:
    return {finding.rule for finding in checker.findings}


def copy_fixture(tmp_path: Path) -> Path:
    target = tmp_path / "course"
    shutil.copytree(FIXTURE, target)
    return target


def test_valid_shared_current_fixture_excludes_archive_ids() -> None:
    checker = run_checker(FIXTURE)
    assert isinstance(checker, check.SharedCurriculumChecker)
    assert checker.findings == []
    assert "22222222-2222-4222-8222-222222222222" in checker.content_ids
    # The historical module intentionally repeats the current module and unit
    # IDs.  It must not be loaded or registered.
    assert checker.content_ids["22222222-2222-4222-8222-222222222222"] == "01-agentic-rag/module.yaml"
    assert checker.content_ids["33333333-3333-4333-8333-333333333333"] == (
        "01-agentic-rag/module.yaml"
    )


def test_archive_marker_requires_a_notice_path(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "cohorts" / "2027" / "cohort.yaml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("curriculum: current", "curriculum: github_archive", 1),
        encoding="utf-8",
    )
    assert "archive_notice_missing" in rules(run_checker(root))


def test_archive_homework_module_must_be_null(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "cohorts" / "2025" / "cohort.yaml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("module: null", "module: 01-agentic-rag", 1),
        encoding="utf-8",
    )
    assert "archive_module_reference" in rules(run_checker(root))


def test_homework_mapping_must_be_contained_by_declaring_cohort(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "cohorts" / "2027" / "cohort.yaml"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "source: cohorts/2027/homework/01-agentic-rag/homework.yaml",
            "source: cohorts/self-paced/homework/01-agentic-rag/homework.yaml",
            1,
        ),
        encoding="utf-8",
    )
    assert "homework_path_outside_cohort" in rules(run_checker(root))


def test_current_homework_must_be_explicitly_mapped(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    homework = root / "cohorts" / "2027" / "homework" / "02-agents"
    homework.mkdir(parents=True)
    (homework / "homework.yaml").write_text(
        "schema_version: 2\ncontent_id: aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaab\n", encoding="utf-8"
    )
    (homework / "homework.md").write_text("# Practice\n", encoding="utf-8")
    assert "homework_unreferenced" in rules(run_checker(root))


def test_self_paced_cohort_requires_empty_homework_list(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "cohorts" / "self-paced" / "cohort.yaml"
    written = path.write_text(
        path.read_text(encoding="utf-8").replace(
            "homework: []",
            (
                "homework:\n"
                "  - module: 01-agentic-rag\n"
                "    source: cohorts/self-paced/homework/01-agentic-rag/homework.yaml"
            ),
            1,
        ),
        encoding="utf-8",
    )
    assert written
    homework_dir = root / "cohorts" / "self-paced" / "homework" / "01-agentic-rag"
    homework_dir.mkdir(parents=True)
    (homework_dir / "homework.yaml").write_text(
        "schema_version: 2\n"
        "content_id: bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb\n"
        "slug: hw01\n"
        "title: Practice\n"
        "due_at: \"2027-06-14T23:59:00+00:00\"\n"
        "questions: []\n",
        encoding="utf-8",
    )
    (homework_dir / "homework.md").write_text("# Practice\n", encoding="utf-8")
    assert "self_paced_homework_rejected" in rules(run_checker(root))


def test_duplicate_yaml_keys_are_rejected(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "course.yaml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("title: LLM Zoomcamp\n", "title: LLM Zoomcamp\ntitle: Duplicate\n"),
        encoding="utf-8",
    )
    assert "v2_schema" in rules(run_checker(root))


def test_numeric_cohort_identifier_is_not_coerced_to_string(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "cohorts" / "2027" / "cohort.yaml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('identifier: "2027"', "identifier: 2027", 1),
        encoding="utf-8",
    )
    assert "v2_schema" in rules(run_checker(root))


def test_symlink_is_rejected_before_discovery(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("not curriculum", encoding="utf-8")
    os.symlink(outside, root / "01-agentic-rag" / "linked-asset.txt")
    assert "v2_path_unsafe" in rules(run_checker(root))


def test_duplicate_lesson_prefix_is_rejected(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    module = root / "01-agentic-rag"
    old = module / "02-function-calling.md"
    old.rename(module / "01-function-calling.md")
    manifest = module / "module.yaml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "path: 02-function-calling.md", "path: 01-function-calling.md", 1
        ),
        encoding="utf-8",
    )
    assert "duplicate_number_prefix" in rules(run_checker(root))


def test_unknown_lesson_frontmatter_key_is_rejected(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "01-agentic-rag" / "02-function-calling.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("prev_url:", "prev:", 1),
        encoding="utf-8",
    )
    findings = run_checker(root).findings
    assert "v2_schema" in {finding.rule for finding in findings}
    assert "lesson_navigation_mismatch" in {finding.rule for finding in findings}


def test_missing_lesson_navigation_key_is_rejected(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "01-agentic-rag" / "02-function-calling.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("next_url: ../02-agents/01-agent-loops.md\n", "", 1),
        encoding="utf-8",
    )
    findings = run_checker(root).findings
    assert "lesson_navigation_mismatch" in {finding.rule for finding in findings}
    assert any("missing next_url" in finding.message for finding in findings)


def test_wrong_lesson_navigation_target_is_rejected(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "02-agents" / "01-agent-loops.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "prev_url: ../01-agentic-rag/02-function-calling.md",
            "prev_url: ../01-agentic-rag/01-retrieval-augmented-generation.md",
            1,
        ),
        encoding="utf-8",
    )
    findings = run_checker(root).findings
    assert "lesson_navigation_mismatch" in {finding.rule for finding in findings}


def test_boundary_lesson_must_not_declare_navigation(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "01-agentic-rag" / "01-retrieval-augmented-generation.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "next_url: 02-function-calling.md",
            "prev_url: 02-function-calling.md\nnext_url: 02-function-calling.md",
            1,
        ),
        encoding="utf-8",
    )
    findings = run_checker(root).findings
    assert "lesson_navigation_mismatch" in {finding.rule for finding in findings}
    assert any("no previous current lesson" in finding.message for finding in findings)


def test_navigation_key_pointing_outside_the_current_graph_is_rejected(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "02-agents" / "01-agent-loops.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "prev_url: ../01-agentic-rag/02-function-calling.md",
            "prev_url: ../cohorts/2025/01-old-module/01-historical-retrieval.md",
            1,
        ),
        encoding="utf-8",
    )
    findings = run_checker(root).findings
    assert "v2_path_unsafe" in {finding.rule for finding in findings}


def test_navigation_key_to_a_non_lesson_file_is_rejected(tmp_path: Path) -> None:
    root = copy_fixture(tmp_path)
    path = root / "02-agents" / "01-agent-loops.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "prev_url: ../01-agentic-rag/02-function-calling.md",
            "prev_url: ../01-agentic-rag/README.md",
            1,
        ),
        encoding="utf-8",
    )
    findings = run_checker(root).findings
    assert "lesson_navigation_mismatch" in {finding.rule for finding in findings}
    assert any("declared current lesson" in finding.message for finding in findings)


def test_standalone_cli_accepts_v2_fixture_and_rejects_invalid_copy(tmp_path: Path) -> None:
    accepted = subprocess.run(
        [sys.executable, str(CHECKER), str(FIXTURE), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert accepted.returncode == 0, accepted.stdout + accepted.stderr
    broken = copy_fixture(tmp_path)
    cohort = broken / "cohorts" / "2027" / "cohort.yaml"
    cohort.write_text(
        cohort.read_text(encoding="utf-8").replace("delivery: live", "delivery: recorded", 1),
        encoding="utf-8",
    )
    rejected = subprocess.run(
        [sys.executable, str(CHECKER), str(broken), "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert rejected.returncode == 1
    assert '"invalid_delivery"' in rejected.stdout


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
