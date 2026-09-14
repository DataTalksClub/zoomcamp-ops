"""Exercise the producer and checker together on a disposable v2 repository."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


OPS_ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = OPS_ROOT / "scripts/bootstrap-cohort/bootstrap_cohort.py"
CHECKER = OPS_ROOT / "scripts/check-zoomcamp/check_zoomcamp.py"
FIXTURE = OPS_ROOT / "scripts/check-zoomcamp/fixtures/shared-current-v2"


def run_command(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        cwd=OPS_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def assert_success(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, result.stdout + result.stderr


def tree_digest(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_bootstrap_and_archive_output_passes_shared_checker(tmp_path: Path) -> None:
    repository = tmp_path / "course"
    shutil.copytree(FIXTURE, repository)
    assert_success(run_command(CHECKER, str(repository)))
    original = tree_digest(repository)

    live_args = ("bootstrap", str(repository), "--cohort", "2028", "--delivery", "live")
    assert_success(run_command(BOOTSTRAP, *live_args, "--json"))
    assert tree_digest(repository) == original
    assert_success(run_command(BOOTSTRAP, *live_args, "--apply"))
    live = yaml.safe_load((repository / "cohorts/2028/cohort.yaml").read_text())
    assert live["identifier"] == "2028"
    assert live["delivery"] == "live"
    assert live["curriculum"] == "current"
    assert live["published"] is False
    assert live["homework"] == []
    assert not list((repository / "cohorts/2028").rglob("module.yaml"))
    assert_success(run_command(CHECKER, str(repository)))

    after_live = tree_digest(repository)
    assert_success(run_command(BOOTSTRAP, *live_args, "--apply"))
    assert tree_digest(repository) == after_live

    self_paced_args = (
        "bootstrap", str(repository), "--cohort", "self-paced-new",
        "--delivery", "self-paced",
    )
    assert_success(run_command(BOOTSTRAP, *self_paced_args, "--apply"))
    self_paced = yaml.safe_load(
        (repository / "cohorts/self-paced-new/cohort.yaml").read_text()
    )
    assert self_paced["delivery"] == "self_paced"
    assert self_paced["curriculum"] == "current"
    assert self_paced["homework"] == []
    assert self_paced.get("start_date") is None
    assert self_paced.get("end_date") is None
    assert self_paced["content_id"] != live["content_id"]
    assert_success(run_command(CHECKER, str(repository)))

    before_archive = tree_digest(repository)
    archive_args = ("archive", str(repository), "--cohort", "2028")
    assert_success(run_command(BOOTSTRAP, *archive_args, "--json"))
    assert tree_digest(repository) == before_archive
    assert_success(run_command(BOOTSTRAP, *archive_args, "--apply"))
    archived = yaml.safe_load((repository / "cohorts/2028/cohort.yaml").read_text())
    assert archived["content_id"] == live["content_id"]
    assert archived["curriculum"] == "github_archive"
    assert archived["homework"] == []
    assert (repository / archived["archive"]["notice_path"]).is_file()
    assert list((repository / "cohorts/2028").rglob("module.yaml"))
    assert_success(run_command(CHECKER, str(repository)))
    after_archive = tree_digest(repository)
    for path, digest in original.items():
        assert after_archive[path] == digest

    assert_success(run_command(BOOTSTRAP, *archive_args, "--apply"))
    assert tree_digest(repository) == after_archive
