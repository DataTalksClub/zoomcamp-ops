#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0", "pytest>=8.0"]
# ///
"""Safety and repeatability tests for bootstrap_cohort.py.

Every repository below is built under pytest's temporary directory.  Nothing
in a real course checkout is ever used as a test fixture or modified by the
test suite.
"""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest
import yaml


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("bootstrap_cohort", HERE / "bootstrap_cohort.py")
assert SPEC and SPEC.loader
bootstrap = importlib.util.module_from_spec(SPEC)
sys.modules["bootstrap_cohort"] = bootstrap
SPEC.loader.exec_module(bootstrap)


def write(path: Path, text: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, str):
        path.write_text(text, encoding="utf-8")
    else:
        path.write_bytes(text)


def make_repo(tmp_path: Path, *, old_layout: bool = False, links: bool = True) -> Path:
    root = tmp_path / "course"
    root.mkdir(parents=True)
    write(
        root / "course.yaml",
        "schema_version: 2\n"
        "content_id: 11111111-1111-4111-8111-111111111111\n"
        "slug: fixture-zoomcamp\n",
    )
    write(root / "cohorts" / "README.md", "# Cohorts\n")
    if old_layout:
        write(
            root / "cohorts" / "2026" / "01-agentic-rag" / "module.yaml",
            "schema_version: 1\n"
            "content_id: 22222222-2222-4222-8222-222222222222\n"
            "title: Old\n"
            "units: []\n",
        )
        return root
    module_specs = (
        (
            "01-agentic-rag",
            "22222222-2222-4222-8222-222222222222",
            "Agentic RAG",
            "01-introduction.md",
        ),
        (
            "02-vector-search",
            "33333333-3333-4333-8333-333333333333",
            "Vector Search",
            "01-indexing.md",
        ),
    )
    for slug, content_id, title, lesson in module_specs:
        module = root / slug
        write(
            module / "module.yaml",
            f"schema_version: 2\ncontent_id: {content_id}\ntitle: {title}\n",
        )
        target = "../02-vector-search/01-indexing.md" if links and slug == "01-agentic-rag" else "images/diagram.png"
        write(
            module / lesson,
            f"# {title}\n\n[related material]({target})\n\n![diagram](images/diagram.png)\n",
        )
        write(module / "README.md", f"# {title}\n")
        write(module / "images" / "diagram.png", b"fixture image\n")
        write(module / "code" / "example.py", "print('fixture')\n")
    return root


def request_file(tmp_path: Path, *, with_homework: bool = True) -> Path:
    request = {
        "schema_version": 2,
        "cohort": {
            "id": "2027",
            "delivery": "live",
            "title": "Fixture Zoomcamp 2027",
            "start_date": "2027-06-07",
            "end_date": "2027-10-11",
        },
        "modules": [
            {
                "slug": "01-agentic-rag",
                **(
                    {
                        "homework": {
                            "slug": "homework-01",
                            "title": "Homework 1: Agentic RAG",
                            "instructions": "# Homework 1\n\nBuild the exercise.\n",
                            "due_at": "2027-07-01T21:59:00Z",
                            "initial_state": "open",
                            "form": {
                                "homework_url": True,
                                "time_spent_lectures": True,
                                "time_spent_homework": True,
                                "faq_contribution": True,
                                "learning_in_public_cap": 7,
                            },
                            "questions": [
                                {
                                    "id": "q1",
                                    "type": "free_form_long",
                                    "prompt": "What did you learn?",
                                    "answer_type": "any",
                                    "points": 0,
                                }
                            ],
                        }
                    }
                    if with_homework
                    else {}
                ),
            },
            {"slug": "02-vector-search"},
        ],
    }
    path = tmp_path / "bootstrap.yaml"
    write(path, yaml.safe_dump(request, sort_keys=False))
    return path


def snapshot(root: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            result[path.relative_to(root).as_posix()] = path.read_bytes()
    return result


def test_bootstrap_plan_is_read_only_and_references_shared_modules(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    before = snapshot(root)
    plan = bootstrap.build_bootstrap_plan(root, request_path=request)
    assert plan.changed
    assert all(action.path.startswith("cohorts/2027/") for action in plan.writes)
    assert any("cohort.yaml" in action.path for action in plan.writes)
    assert snapshot(root) == before
    assert not (root / "cohorts" / "2027").exists()
    assert plan.metadata["modules"] == ["01-agentic-rag", "02-vector-search"]


def test_bootstrap_apply_and_exact_replay_are_idempotent(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    first = bootstrap.build_bootstrap_plan(root, request_path=request)
    bootstrap.apply_plan(first)
    after = snapshot(root)
    second = bootstrap.build_bootstrap_plan(root, request_path=request)
    assert not second.changed
    assert snapshot(root) == after
    manifest = yaml.safe_load((root / "cohorts" / "2027" / "cohort.yaml").read_text())
    assert manifest["course"] == "fixture-zoomcamp"
    assert manifest["curriculum"] == "current"
    assert manifest["identifier"] == "2027"
    assert manifest["homework"][0] == {
        "module": "01-agentic-rag",
        "source": "cohorts/2027/homework/01-agentic-rag/homework.yaml",
    }
    assert not (root / "cohorts" / "2027" / "01-agentic-rag").exists()
    assert (root / "01-agentic-rag" / "01-introduction.md").exists()
    homework = yaml.safe_load(
        (root / "cohorts" / "2027" / "homework" / "01-agentic-rag" / "homework.yaml").read_text()
    )
    assert homework["content_id"] not in {
        "11111111-1111-4111-8111-111111111111",
        "22222222-2222-4222-8222-222222222222",
        "33333333-3333-4333-8333-333333333333",
    }
    assert homework["initial_state"] == "open"
    assert homework["due_at"] == "2027-07-01T21:59:00Z"
    assert homework["questions"][0]["content_id"] not in {
        "11111111-1111-4111-8111-111111111111",
        "22222222-2222-4222-8222-222222222222",
        "33333333-3333-4333-8333-333333333333",
    }


def test_bootstrap_does_not_carry_homework_or_dates_without_explicit_request(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path, with_homework=False)
    # Change the request to a self-paced delivery with no dates.  The fixture
    # has no source cohort at all; this assertion also guards against future
    # implementations that look for one and silently copy it.
    values = yaml.safe_load(request.read_text())
    values["cohort"]["delivery"] = "self-paced"
    values["cohort"].pop("start_date")
    values["cohort"].pop("end_date")
    request.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
    plan = bootstrap.build_bootstrap_plan(root, request_path=request)
    bootstrap.apply_plan(plan)
    cohort = yaml.safe_load((root / "cohorts" / "2027" / "cohort.yaml").read_text())
    assert cohort["delivery"] == "self_paced"
    assert cohort["start_date"] is None and cohort["end_date"] is None
    assert cohort["homework"] == []
    assert not (root / "cohorts" / "2027" / "homework").exists()


def test_bootstrap_request_modules_only_select_homework_and_never_shrinks_shared_graph(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    values = yaml.safe_load(request.read_text())
    values["modules"] = [values["modules"][0]]
    request.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
    bootstrap.apply_plan(bootstrap.build_bootstrap_plan(root, request_path=request))
    cohort = yaml.safe_load((root / "cohorts" / "2027" / "cohort.yaml").read_text())
    assert cohort["curriculum"] == "current"
    assert cohort["homework"][0]["module"] == "01-agentic-rag"
    readme = (root / "cohorts" / "2027" / "README.md").read_text()
    assert "02-vector-search" in readme


def test_bootstrap_rejects_cli_module_subset(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    with pytest.raises(bootstrap.BootstrapError, match="module_subset_unsupported"):
        bootstrap.build_bootstrap_plan(root, cohort_id="2027", delivery="live", module_slugs=["01-agentic-rag"])


def test_bootstrap_rejects_authored_self_paced_homework_policy(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    values = yaml.safe_load(request.read_text())
    values["cohort"]["delivery"] = "self-paced"
    values["cohort"].pop("start_date")
    values["cohort"].pop("end_date")
    request.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
    with pytest.raises(bootstrap.BootstrapError, match="self_paced_homework_unsupported"):
        bootstrap.build_bootstrap_plan(root, request_path=request)


def test_bootstrap_accepts_only_a_valid_encrypted_answer_envelope(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    values = yaml.safe_load(request.read_text())
    question = values["modules"][0]["homework"]["questions"][0]
    question["answer_type"] = "integer"
    question["answer"] = {
        "version": 1,
        "algorithm": "A256GCM",
        "kdf": "HKDF-SHA256",
        "key_id": "fixture-key",
        "salt": base64.urlsafe_b64encode(b"s" * 32).decode().rstrip("="),
        "nonce": base64.urlsafe_b64encode(b"n" * 12).decode().rstrip("="),
        "ciphertext": base64.urlsafe_b64encode(b"c" * 16).decode().rstrip("="),
        "context_sha256": hashlib.sha256(
            b"dtc-homework-answer:v1\0fixture-zoomcamp\0homework-01\0q1"
        ).hexdigest(),
    }
    request.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
    plan = bootstrap.build_bootstrap_plan(root, request_path=request)
    bootstrap.apply_plan(plan)
    homework = yaml.safe_load(
        (root / "cohorts" / "2027" / "homework" / "01-agentic-rag" / "homework.yaml").read_text()
    )
    assert homework["questions"][0]["answer"]["algorithm"] == "A256GCM"

    values["modules"][0]["homework"]["questions"][0]["answer"]["context_sha256"] = "0" * 64
    request.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
    with pytest.raises(bootstrap.BootstrapError, match="answer_context_mismatch"):
        bootstrap.build_bootstrap_plan(root, request_path=request, cohort_id="2028")


def test_bootstrap_mints_assignment_and_question_ids_instead_of_reusing_input_ids(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    values = yaml.safe_load(request.read_text())
    values["modules"][0]["homework"]["content_id"] = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
    with pytest.raises(bootstrap.BootstrapError, match="content_id_forbidden"):
        request.write_text(yaml.safe_dump(values, sort_keys=False), encoding="utf-8")
        bootstrap.build_bootstrap_plan(root, request_path=request)


def test_bootstrap_refuses_old_cohort_owned_layout_before_writes(tmp_path: Path) -> None:
    root = make_repo(tmp_path, old_layout=True)
    request = request_file(tmp_path)
    before = snapshot(root)
    with pytest.raises(bootstrap.BootstrapError, match="migration_required"):
        bootstrap.build_bootstrap_plan(root, request_path=request)
    assert snapshot(root) == before


def test_bootstrap_refuses_traversal_and_conflicting_overwrite(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    original = request.read_text()
    request.write_text(original.replace("01-agentic-rag", "../escape", 1), encoding="utf-8")
    with pytest.raises(bootstrap.BootstrapError, match="invalid_module"):
        bootstrap.build_bootstrap_plan(root, request_path=request)

    request.write_text(original, encoding="utf-8")
    target = root / "cohorts" / "2027" / "README.md"
    write(target, "a conflicting file\n")
    with pytest.raises(bootstrap.BootstrapError, match="overwrite_refused"):
        bootstrap.build_bootstrap_plan(root, request_path=request)
    assert target.read_text() == "a conflicting file\n"


def test_bootstrap_rejects_symlinked_root_module(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "01-agentic-rag").rename(root / "01-agentic-rag-real")
    os.symlink(outside, root / "01-agentic-rag")
    with pytest.raises(bootstrap.BootstrapError, match="symlink_rejected"):
        bootstrap.build_bootstrap_plan(root, cohort_id="2027", delivery="live")


def test_archive_preserves_complete_tree_and_cross_module_links(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    before_modules = {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.glob("0[12]-*")
        for path in path.rglob("*")
        if path.is_file()
    }
    plan = bootstrap.build_archive_plan(root, cohort_id="2026")
    assert plan.changed
    assert any(action.path == "cohorts/2026/archive.yaml" for action in plan.writes)
    bootstrap.apply_plan(plan)
    for relative, data in before_modules.items():
        archived = root / "cohorts" / "2026" / relative
        assert archived.read_bytes() == data
    assert snapshot(root / "01-agentic-rag") == {
        key.removeprefix("01-agentic-rag/"): value
        for key, value in snapshot(root).items()
        if key.startswith("01-agentic-rag/")
    }
    manifest = yaml.safe_load((root / "cohorts" / "2026" / "archive.yaml").read_text())
    assert manifest["kind"] == "curriculum_archive"
    assert [module["slug"] for module in manifest["modules"]] == [
        "01-agentic-rag",
        "02-vector-search",
    ]
    cohort = yaml.safe_load((root / "cohorts" / "2026" / "cohort.yaml").read_text())
    assert cohort["curriculum"] == "github_archive"
    assert cohort["archive"] == {"notice_path": "cohorts/2026/README.md"}
    assert "01-agentic-rag/" in (root / "cohorts" / "2026" / "README.md").read_text()
    replay = bootstrap.build_archive_plan(root, cohort_id="2026")
    assert not replay.changed


def test_archive_allows_existing_cohort_delivery_files(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    write(root / "cohorts" / "2026" / "README.md", "old delivery notes\n")
    write(root / "cohorts" / "2026" / "homework" / "01.md", "assignment\n")
    plan = bootstrap.build_archive_plan(root, cohort_id="2026")
    bootstrap.apply_plan(plan)
    readme = (root / "cohorts" / "2026" / "README.md").read_text()
    assert readme.startswith("old delivery notes\n")
    assert "Archived curriculum: 2026" in readme
    assert (root / "cohorts" / "2026" / "homework" / "01.md").exists()


def test_archive_refuses_unselected_cross_module_dependency_before_writes(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    request = tmp_path / "archive.yaml"
    write(request, "schema_version: 2\nmodules:\n  - 01-agentic-rag\n")
    before = snapshot(root)
    with pytest.raises(bootstrap.BootstrapError, match="external_root_dependency"):
        bootstrap.build_archive_plan(root, cohort_id="2026", manifest_path=request)
    assert snapshot(root) == before


def test_archive_refuses_root_dependency_and_missing_link(tmp_path: Path) -> None:
    root = make_repo(tmp_path, links=False)
    write(root / "01-agentic-rag" / "01-introduction.md", "# Intro\n\n[bad](../README.md)\n")
    before = snapshot(root)
    with pytest.raises(bootstrap.BootstrapError, match="external_root_dependency"):
        bootstrap.build_archive_plan(root, cohort_id="2026")
    assert snapshot(root) == before


def test_archive_refuses_symlink_and_plaintext_answer_key(tmp_path: Path) -> None:
    root = make_repo(tmp_path, links=False)
    os.symlink(root / "02-vector-search" / "code", root / "01-agentic-rag" / "linked-code")
    with pytest.raises(bootstrap.BootstrapError, match="symlink_rejected"):
        bootstrap.build_archive_plan(root, cohort_id="2026")

    root = make_repo(tmp_path / "answer", links=False)
    write(
        root / "01-agentic-rag" / "metadata.yaml",
        "answer_key: pages-24\n",
    )
    with pytest.raises(bootstrap.BootstrapError, match="plaintext_answer_key"):
        bootstrap.build_archive_plan(root, cohort_id="2026")


def test_archive_refuses_conflicting_existing_bytes(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    existing = root / "cohorts" / "2026" / "01-agentic-rag" / "README.md"
    write(existing, "different archive\n")
    with pytest.raises(bootstrap.BootstrapError, match="overwrite_refused"):
        bootstrap.build_archive_plan(root, cohort_id="2026")


def test_archive_switches_existing_v2_cohort_and_preserves_delivery_fields(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    write(
        root / "cohorts" / "2026" / "cohort.yaml",
        yaml.safe_dump(
            {
                "schema_version": 2,
                "content_id": "44444444-4444-4444-8444-444444444444",
                "identifier": "2026",
                "course": "fixture-zoomcamp",
                "delivery": "self_paced",
                "curriculum": "current",
                "published": True,
                "start_date": None,
                "end_date": None,
                "homework": [
                    {"module": "01-agentic-rag", "source": "cohorts/2026/homework/01/homework.yaml"}
                ],
            },
            sort_keys=False,
        ),
    )
    write(root / "cohorts" / "2026" / "homework" / "01" / "homework.yaml", "historical: true\n")
    write(root / "cohorts" / "2026" / "homework" / "01" / "homework.md", "# Historical Homework\n")
    plan = bootstrap.build_archive_plan(root, cohort_id="2026")
    manifest_action = next(action for action in plan.writes if action.path.endswith("/cohort.yaml"))
    assert manifest_action.replace
    bootstrap.apply_plan(plan)
    manifest = yaml.safe_load((root / "cohorts" / "2026" / "cohort.yaml").read_text())
    assert manifest["delivery"] == "self_paced"
    assert manifest["published"] is True
    assert manifest["homework"] == [
        {"module": None, "source": "cohorts/2026/homework/01/homework.yaml"}
    ]
    assert manifest["curriculum"] == "github_archive"
    assert manifest["archive"] == {"notice_path": "cohorts/2026/README.md"}
    assert (root / "cohorts" / "2026" / "homework" / "01" / "homework.yaml").read_text() == "historical: true\n"
    assert not bootstrap.build_archive_plan(root, cohort_id="2026").changed


def test_archive_refuses_v1_course_before_any_writes(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    write(root / "course.yaml", "schema_version: 1\nslug: fixture-zoomcamp\n")
    before = snapshot(root)
    with pytest.raises(bootstrap.BootstrapError, match="migration_required"):
        bootstrap.build_archive_plan(root, cohort_id="2026")
    assert snapshot(root) == before


def test_archive_apply_rolls_back_tree_when_controlled_metadata_changed(tmp_path: Path) -> None:
    root = make_repo(tmp_path)
    metadata = root / "cohorts" / "2026" / "cohort.yaml"
    write(
        metadata,
        yaml.safe_dump(
            {
                "schema_version": 2,
                "content_id": "44444444-4444-4444-8444-444444444444",
                "identifier": "2026",
                "course": "fixture-zoomcamp",
                "delivery": "live",
                "curriculum": "current",
                "published": False,
                "start_date": None,
                "end_date": None,
                "homework": [],
            },
            sort_keys=False,
        ),
    )
    plan = bootstrap.build_archive_plan(root, cohort_id="2026")
    original_metadata = metadata.read_bytes()
    metadata.write_bytes(original_metadata + b"# changed after planning\n")
    with pytest.raises(bootstrap.BootstrapError, match="concurrent_change"):
        bootstrap.apply_plan(plan)
    assert metadata.read_bytes() == original_metadata + b"# changed after planning\n"
    assert not (root / "cohorts" / "2026" / "01-agentic-rag").exists()
    assert not (root / "cohorts" / "2026" / "archive.yaml").exists()


def test_archive_checks_reference_links_and_moving_repository_urls(tmp_path: Path) -> None:
    root = make_repo(tmp_path, links=False)
    write(
        root / "01-agentic-rag" / "01-introduction.md",
        "# Intro\n\n![diagram][asset] and [asset][]\n\n[asset]: images/diagram.png\n",
    )
    assert bootstrap.build_archive_plan(root, cohort_id="2026").changed
    write(
        root / "course.yaml",
        "schema_version: 2\n"
        "content_id: 11111111-1111-4111-8111-111111111111\n"
        "slug: fixture-zoomcamp\n"
        "repository_url: https://github.com/DataTalksClub/fixture-zoomcamp\n",
    )
    write(
        root / "01-agentic-rag" / "01-introduction.md",
        "# Intro\n\n[current](https://github.com/DataTalksClub/fixture-zoomcamp/blob/main/README.md)\n",
    )
    with pytest.raises(bootstrap.BootstrapError, match="moving_repository_dependency"):
        bootstrap.build_archive_plan(root, cohort_id="2026")


def test_json_plan_does_not_include_content_bodies(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = make_repo(tmp_path)
    request = request_file(tmp_path)
    plan = bootstrap.build_bootstrap_plan(root, request_path=request)
    bootstrap._print_plan(plan, as_json=True)
    parsed = json.loads(capsys.readouterr().out)
    rendered = json.dumps(parsed)
    assert "Build the exercise" not in rendered
    assert "print('fixture')" not in rendered
    assert "cohorts/2027/cohort.yaml" in rendered
