#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Safely create a cohort reference or archive the current curriculum.

The command is deliberately a small, local filesystem tool.  It does not call
Git, GitHub, the website, or a course-management API.  The default operation
is a read-only plan; ``--apply`` is required before a file can be created.

There are two separate operations:

``bootstrap``
    Creates a cohort manifest and explicitly requested homework under
    ``cohorts/<identifier>/``.  Numbered modules at the repository root are
    referenced by path and are never copied.

``archive``
    Copies selected numbered root modules into ``cohorts/<identifier>/`` with
    their complete local trees.  Markdown links are checked before any write;
    links to selected sibling modules remain valid after the copy, while links
    outside the selected curriculum are refused.

The source repositories currently found in the wild use the older
cohort-owned layout.  Seeing a non-archived ``cohorts/*/*/module.yaml`` is a
hard migration prerequisite, not a reason to move files implicitly.  An
explicit v2 ``curriculum: github_archive`` cohort classifier (or the local
checksum ``archive.yaml`` evidence) is required before archived module trees
are ignored by this gate.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import posixpath
import re
import sys
import tempfile
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator, Mapping, Sequence
from urllib.parse import unquote, urlsplit

import yaml


SCRIPT_VERSION = "2"
SCHEMA_VERSION = 2
DEFAULT_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
MODULE_RE = re.compile(r"^\d{2,}-[a-z0-9]+(?:-[a-z0-9]+)*$")
LESSON_RE = re.compile(r"^\d{2,}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
UUID_RE = re.compile(
    r"(?<![0-9a-fA-F])([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12})(?![0-9a-fA-F])"
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
MD_LINK_RE = re.compile(
    r"(!?)\[(?:[^\]\\]|\\.)*\]\(\s*(<[^>]*>|[^()\s]*(?:\([^()]*\)[^()\s]*)*)"
)
MD_REFERENCE_DEFINITION_RE = re.compile(
    r"^\s{0,3}\[([^\]]+)\]:\s*(<[^>]*>|\S+)"
)
MD_REFERENCE_USE_RE = re.compile(
    r"!?\[([^\]\\]*(?:\\.[^\]\\]*)*)\]\s*\[([^\]]*)\]"
)
MD_SHORTCUT_REFERENCE_RE = re.compile(r"!?\[([^\]\\]+)\](?!\s*[\[(])")
HTML_LINK_RE = re.compile(
    r"<(?:a|img)\b[^>]*?\b(?:href|src)\s*=\s*['\"]([^'\"]+)['\"]",
    re.IGNORECASE,
)
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")

PLAINTEXT_ANSWER_KEYS = frozenset(
    {
        "answer_key",
        "answer_value",
        "correct_answer",
        "plaintext_answer",
        "solution",
    }
)
BASE64URL_RE = re.compile(r"^[A-Za-z0-9_-]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class DuplicateKeyLoader(yaml.SafeLoader):
    """PyYAML loader that fails closed on duplicate mapping keys."""


def _construct_unique_mapping(
    loader: DuplicateKeyLoader,
    node: yaml.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    mapping: dict[object, object] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.YAMLError(f"duplicate mapping key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


DuplicateKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


class BootstrapError(ValueError):
    """A bounded, user-actionable refusal.

    ``detail`` contains paths and rule names only.  We never include file
    bodies, homework prompts, answer material, or environment values in a
    diagnostic because command output is routinely pasted into issues.
    """

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class WriteAction:
    path: str
    reason: str
    data: bytes
    mode: int = 0o644
    # Replacement is reserved for the archive metadata/notice transition.
    # All ordinary bootstrap and archive-tree writes remain create-only.
    replace: bool = False
    expected_sha256: str | None = None


@dataclass(frozen=True)
class Plan:
    operation: str
    repo_root: Path
    writes: tuple[WriteAction, ...]
    skips: tuple[str, ...] = ()
    checks: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def changed(self) -> bool:
        return bool(self.writes)

    def as_dict(self) -> dict[str, Any]:
        return {
            "operation": self.operation,
            "repo_root": str(self.repo_root),
            "changed": self.changed,
            "actions": [
                {
                    "action": "update" if item.replace else "create",
                    "path": item.path,
                    "reason": item.reason,
                }
                for item in self.writes
            ]
            + [{"action": "skip", "path": path, "reason": "already matches"} for path in self.skips],
            "checks": list(self.checks),
            "metadata": dict(self.metadata),
        }

    def render(self) -> str:
        lines = [f"{self.operation}: {'changes required' if self.changed else 'no changes'}"]
        for item in self.writes:
            verb = "update" if item.replace else "create"
            lines.append(f"  {verb:<6} {item.path}  ({item.reason})")
        for path in self.skips:
            lines.append(f"  skip   {path}  (already matches)")
        for check in self.checks:
            lines.append(f"  check  {check}")
        return "\n".join(lines)


@dataclass(frozen=True)
class ModuleInfo:
    slug: str
    path: str
    manifest_path: str
    content_id: str | None
    title: str | None
    files: tuple[str, ...] = ()


@dataclass(frozen=True)
class HomeworkInfo:
    module: str
    slug: str
    title: str
    instructions: str
    content_id: str
    due_at: str | None
    values: Mapping[str, Any]


def _error(code: str, detail: str) -> BootstrapError:
    return BootstrapError(code, detail)


def _safe_path_string(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise _error("unsafe_path", f"{label} must be a non-empty relative path")
    if value != value.strip() or "\x00" in value or "\\" in value:
        raise _error("unsafe_path", f"{label} is not a normalized POSIX path")
    if value.startswith("/") or SCHEME_RE.match(value) or value.startswith("//"):
        raise _error("unsafe_path", f"{label} must not be absolute or a URL")
    pure = PurePosixPath(value)
    if pure.as_posix() != value or any(part in {"", ".", ".."} for part in pure.parts):
        raise _error("unsafe_path", f"{label} contains a traversal or non-canonical segment")
    return value


def _safe_slug(value: object, *, label: str, maximum: int = 100) -> str:
    if not isinstance(value, str) or len(value) > maximum or SLUG_RE.fullmatch(value) is None:
        raise _error("invalid_identifier", f"{label} must be lowercase kebab-case")
    return value


def _safe_module_slug(value: object, *, label: str = "module") -> str:
    if not isinstance(value, str) or MODULE_RE.fullmatch(value) is None:
        raise _error("invalid_module", f"{label} must be NN-kebab-case")
    return value


def _module_sort_key(slug: str) -> tuple[int, str]:
    """Sort numbered modules/lessons by their numeric prefix, not text."""

    prefix = slug.split("-", 1)[0]
    return int(prefix), slug


def _canonical_uuid(value: object, *, label: str) -> str:
    if not isinstance(value, str):
        raise _error("invalid_content_id", f"{label} must be a UUID string")
    try:
        parsed = uuid.UUID(value)
    except ValueError as exc:
        raise _error("invalid_content_id", f"{label} is not a UUID") from exc
    if str(parsed) != value:
        raise _error("invalid_content_id", f"{label} must be canonical lowercase UUID form")
    return value


def _yaml_load(path: Path, *, label: str) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise _error("invalid_utf8", f"{label} is not UTF-8") from exc
    try:
        return yaml.load(text, Loader=DuplicateKeyLoader)
    except yaml.YAMLError as exc:
        raise _error("invalid_yaml", f"{label} is not valid YAML") from exc


def _mapping(value: object, *, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise _error("invalid_schema", f"{label} must be a YAML mapping")
    return value


def _strict_keys(mapping: Mapping[str, Any], allowed: set[str], *, label: str) -> None:
    unknown = sorted(set(mapping) - allowed)
    if unknown:
        raise _error("unknown_key", f"{label} contains unsupported key {unknown[0]!r}")


def _text(value: object, *, label: str, required: bool = True) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str) or (required and not value.strip()):
        raise _error("invalid_schema", f"{label} must be non-empty text")
    return value


def _boolean(value: object, *, label: str, default: bool = False) -> bool:
    if value is None:
        return default
    if type(value) is not bool:
        raise _error("invalid_schema", f"{label} must be boolean")
    return value


def _date_string(value: object, *, label: str, required: bool = False) -> str | None:
    if value is None and not required:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        result = value.isoformat()
    elif isinstance(value, str):
        result = value
    else:
        raise _error("invalid_date", f"{label} must be YYYY-MM-DD")
    if DATE_RE.fullmatch(result) is None:
        raise _error("invalid_date", f"{label} must be YYYY-MM-DD")
    try:
        date.fromisoformat(result)
    except ValueError as exc:
        raise _error("invalid_date", f"{label} is not a calendar date") from exc
    return result


def _timestamp_string(value: object, *, label: str) -> str:
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise _error("invalid_timestamp", f"{label} must carry a timezone")
        return value.isoformat()
    if not isinstance(value, str) or not value.strip():
        raise _error("invalid_timestamp", f"{label} must be an explicit timezone-aware timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise _error("invalid_timestamp", f"{label} is not an ISO timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise _error("invalid_timestamp", f"{label} must carry a timezone")
    return value


def _normalise_scalar(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, tuple):
        return [_normalise_scalar(item) for item in value]
    if isinstance(value, list):
        return [_normalise_scalar(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _normalise_scalar(item) for key, item in value.items()}
    return value


def _yaml_dump(mapping: Mapping[str, Any]) -> bytes:
    text = yaml.safe_dump(
        _normalise_scalar(dict(mapping)),
        sort_keys=False,
        allow_unicode=False,
        default_flow_style=False,
    )
    return text.encode("utf-8")


def _repo_root(value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = Path.cwd() / path
    try:
        stat = path.lstat()
    except FileNotFoundError as exc:
        raise _error("repo_unavailable", "repository root does not exist") from exc
    if not path.is_dir() or os.path.islink(path) or path.resolve() != path.absolute():
        raise _error("repo_root_unsafe", "repository root must be a real directory")
    if not stat:
        raise _error("repo_unavailable", "repository root cannot be inspected")
    return path.absolute()


def _relative_to_root(path: Path, root: Path, *, label: str) -> str:
    try:
        relative = path.absolute().relative_to(root.absolute()).as_posix()
    except ValueError as exc:
        raise _error("unsafe_path", f"{label} leaves the repository root") from exc
    return _safe_path_string(relative, label=label)


def _assert_no_symlink_components(root: Path, relative: str, *, label: str, allow_missing: bool) -> None:
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            if allow_missing:
                return
            raise _error("missing_path", f"{label} does not exist")
        if os.path.islink(current):
            raise _error("symlink_rejected", f"{label} contains a symlink")
        if current != root / PurePosixPath(relative) and not os.path.isdir(current):
            # A non-directory parent means the target cannot be a safe path.
            if current != root / PurePosixPath(relative):
                raise _error("unsafe_path", f"{label} has a non-directory parent")
        if not info:
            raise _error("unsafe_path", f"{label} cannot be inspected")


def _assert_regular_file(path: Path, *, label: str) -> None:
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise _error("missing_path", f"{label} does not exist") from exc
    if os.path.islink(path):
        raise _error("symlink_rejected", f"{label} is a symlink")
    if not os.path.isfile(path):
        raise _error("unsupported_file", f"{label} is not a regular file")
    if not info:
        raise _error("unsupported_file", f"{label} cannot be inspected")


def _walk_files(root: Path, *, label: str) -> tuple[Path, ...]:
    """Return a sorted regular-file tree and reject symlinks/special files."""

    _assert_no_symlink_components(root.parent, root.name, label=label, allow_missing=False)
    result: list[Path] = []

    def visit(directory: Path) -> None:
        try:
            entries = sorted(directory.iterdir(), key=lambda item: item.name)
        except OSError as exc:
            raise _error("read_failed", f"cannot inspect {label}") from exc
        for entry in entries:
            if entry.is_symlink():
                raise _error("symlink_rejected", f"{label} contains a symlink")
            if entry.is_dir():
                visit(entry)
            elif entry.is_file():
                result.append(entry)
            else:
                raise _error("unsupported_file", f"{label} contains a special file")

    visit(root)
    return tuple(result)


def _read_course_namespace(root: Path) -> uuid.UUID:
    course_path = root / "course.yaml"
    if not course_path.exists() or course_path.is_symlink():
        return DEFAULT_NAMESPACE
    mapping = _mapping(_yaml_load(course_path, label="course.yaml"), label="course.yaml")
    value = mapping.get("content_id")
    if isinstance(value, str):
        try:
            return uuid.UUID(value)
        except ValueError:
            pass
    return DEFAULT_NAMESPACE


def _course_identity(root: Path) -> tuple[str, int]:
    """Return the course slug and schema version without modifying course.yaml."""

    course_path = root / "course.yaml"
    _assert_regular_file(course_path, label="course.yaml")
    mapping = _mapping(_yaml_load(course_path, label="course.yaml"), label="course.yaml")
    version = mapping.get("schema_version")
    if type(version) is not int:
        raise _error("migration_required", "course.yaml must declare schema_version: 2 before bootstrapping")
    slug = _safe_slug(mapping.get("slug"), label="course.yaml slug")
    if version != SCHEMA_VERSION:
        raise _error(
            "migration_required",
            "course.yaml uses v1; migrate the repository manifest to schema_version: 2 first",
        )
    return slug, version


def _existing_content_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    # This is intentionally a lexical scan.  A malformed old manifest is
    # still a reason not to mint an ID that appears in it.
    ignored = {".git", ".venv", "venv", ".tmp", "__pycache__", "node_modules"}
    paths: list[Path] = []
    for entry in sorted(root.iterdir(), key=lambda item: item.name):
        if entry.name in ignored:
            continue
        if entry.is_symlink():
            # Ignored operational directories are the only paths skipped in
            # this repository-wide ID scan.  Curriculum source trees are
            # walked separately and reject every symlink.
            continue
        if entry.is_dir():
            paths.extend(_walk_files(entry, label="repository"))
        elif entry.is_file():
            paths.append(entry)
        else:
            raise _error("unsupported_file", "repository contains a special file")
    for path in paths:
        if path.suffix.lower() not in {".yaml", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        ids.update(match.group(1).lower() for match in UUID_RE.finditer(text))
    return ids


def _fresh_deterministic_id(root: Path, label: str, existing: set[str]) -> str:
    namespace = _read_course_namespace(root)
    candidate = str(uuid.uuid5(namespace, label))
    counter = 0
    while candidate in existing:
        counter += 1
        candidate = str(uuid.uuid5(namespace, f"{label}:{counter}"))
    existing.add(candidate)
    return candidate


def _find_v1_modules(root: Path) -> list[str]:
    cohorts = root / "cohorts"
    if not cohorts.exists():
        return []
    if cohorts.is_symlink():
        raise _error("symlink_rejected", "cohorts is a symlink")
    found: list[str] = []
    for path in _walk_files(cohorts, label="cohorts"):
        if path.name != "module.yaml":
            continue
        relative = _relative_to_root(path, root, label="module manifest")
        parts = PurePosixPath(relative).parts
        # An archived tree is explicitly marked and is allowed to contain
        # copies of module.yaml.  A cohort-owned manifest without that marker
        # is the old v1 layout and must be migrated by a human/tool designed
        # for that migration.
        if len(parts) >= 2:
            cohort_dir = root / "cohorts" / parts[1]
            if (cohort_dir / "archive.yaml").exists():
                continue
            cohort_manifest = cohort_dir / "cohort.yaml"
            if cohort_manifest.exists() and not cohort_manifest.is_symlink():
                try:
                    cohort_mapping = _mapping(
                        _yaml_load(cohort_manifest, label="archive cohort manifest"),
                        label="archive cohort manifest",
                    )
                except BootstrapError:
                    cohort_mapping = {}
                if cohort_mapping.get("curriculum") == "github_archive":
                    continue
        found.append(relative)
    return found


def _require_new_layout(root: Path) -> None:
    _course_identity(root)
    old = _find_v1_modules(root)
    if old:
        raise _error(
            "migration_required",
            "cohort-owned module manifests found; migrate v1 curriculum to root numbered modules first",
        )


def _root_module_slugs(root: Path) -> tuple[str, ...]:
    result: list[str] = []
    entries = sorted(
        root.iterdir(),
        key=lambda item: _module_sort_key(item.name)
        if MODULE_RE.fullmatch(item.name)
        else (10**9, item.name),
    )
    for entry in entries:
        if entry.is_symlink():
            if MODULE_RE.fullmatch(entry.name):
                raise _error("symlink_rejected", f"root module {entry.name} is a symlink")
            continue
        if not entry.is_dir() or MODULE_RE.fullmatch(entry.name) is None:
            continue
        result.append(entry.name)
    prefixes = [slug.split("-", 1)[0] for slug in result]
    if len(prefixes) != len(set(prefixes)):
        raise _error("duplicate_module_number", "root modules repeat a numeric prefix")
    return tuple(result)


def _module_info(root: Path, slug: str, *, require_manifest: bool = True) -> ModuleInfo:
    module_dir = root / slug
    _safe_module_slug(slug)
    _assert_no_symlink_components(root, slug, label=f"module {slug}", allow_missing=False)
    manifest = module_dir / "module.yaml"
    if require_manifest:
        _assert_regular_file(manifest, label=f"module {slug}/module.yaml")
    mapping: dict[str, Any] = {}
    if manifest.exists():
        loaded = _mapping(_yaml_load(manifest, label=f"{slug}/module.yaml"), label=f"{slug}/module.yaml")
        mapping = loaded
        version = mapping.get("schema_version")
        if type(version) is not int or version != SCHEMA_VERSION:
            raise _error(
                "migration_required",
                f"{slug}/module.yaml must use schema_version: 2 before this operation",
            )
        if "content_id" not in mapping:
            raise _error("invalid_schema", f"{slug}/module.yaml content_id is required")
        _canonical_uuid(mapping["content_id"], label=f"{slug}/module.yaml content_id")
        if not isinstance(mapping.get("title"), str) or not mapping["title"].strip():
            raise _error("invalid_schema", f"{slug}/module.yaml title is required")
    elif not require_manifest:
        raise _error("missing_path", f"module {slug}/module.yaml does not exist")
    # A current tree is copied/linked as a complete, regular-file tree.  Do
    # this before creating any destination action so symlinked lesson/assets
    # fail during preflight rather than halfway through an apply.
    _walk_files(module_dir, label=f"module {slug}")
    for entry in module_dir.iterdir():
        if entry.is_symlink() and LESSON_RE.fullmatch(entry.name):
            raise _error("symlink_rejected", f"module {slug} lesson {entry.name} is a symlink")
    lesson_files = tuple(
        sorted(
            (
                entry.name
                for entry in module_dir.iterdir()
                if not entry.is_symlink() and entry.is_file() and LESSON_RE.fullmatch(entry.name)
            ),
            key=_module_sort_key,
        )
    )
    if not lesson_files:
        lessons_dir = module_dir / "lessons"
        if lessons_dir.exists():
            raise _error(
                "migration_required",
                f"module {slug} still stores lessons/; flatten numbered lessons before bootstrapping",
            )
        raise _error("module_empty", f"module {slug} has no numbered lesson files")
    lesson_numbers = [name.split("-", 1)[0] for name in lesson_files]
    if len(lesson_numbers) != len(set(lesson_numbers)):
        raise _error("duplicate_lesson_number", f"module {slug} repeats a numbered lesson prefix")
    title = mapping.get("title")
    if title is not None and not isinstance(title, str):
        raise _error("invalid_schema", f"{slug}/module.yaml title must be text")
    return ModuleInfo(
        slug=slug,
        path=f"{slug}",
        manifest_path=f"{slug}/module.yaml",
        content_id=mapping.get("content_id"),
        title=title,
        files=lesson_files,
    )


def _extract_cohort_mapping(raw: Mapping[str, Any]) -> dict[str, Any]:
    candidate = raw.get("cohort")
    if candidate is None:
        return dict(raw)
    if isinstance(candidate, str):
        merged = dict(raw)
        merged.pop("cohort", None)
        merged["id"] = candidate
        return merged
    cohort = _mapping(candidate, label="cohort")
    merged = dict(raw)
    merged.pop("cohort", None)
    merged.update({key: value for key, value in cohort.items()})
    return merged


def _load_request(path: Path | None, *, operation: str) -> dict[str, Any]:
    if path is None:
        return {"schema_version": SCHEMA_VERSION}
    _assert_regular_file(path, label="request manifest")
    loaded = _mapping(_yaml_load(path, label="request manifest"), label="request manifest")
    version = loaded.get("schema_version", SCHEMA_VERSION)
    if type(version) is not int or version != SCHEMA_VERSION:
        raise _error("unsupported_schema", "request schema_version must be integer 2")
    declared = loaded.get("operation")
    if declared is not None and declared != operation:
        raise _error("operation_mismatch", "request operation does not match the command")
    return _extract_cohort_mapping(loaded)


def _cohort_fields(
    raw: Mapping[str, Any],
    *,
    cohort_id: str | None,
    delivery: str | None,
    start_date: str | None,
    end_date: str | None,
) -> tuple[str, str, str | None, str | None, str | None, str | None, str | None]:
    allowed = {
        "schema_version",
        "operation",
        "cohort",
        "id",
        "identifier",
        "delivery",
        "mode",
        "kind",
        "title",
        "description",
        "start_date",
        "end_date",
        "published",
        "readme",
        "modules",
        "homework",
    }
    _strict_keys(raw, allowed, label="bootstrap request")
    resolved_id = cohort_id or raw.get("id") or raw.get("identifier")
    if resolved_id is None:
        raise _error("cohort_required", "provide --cohort or cohort.id")
    if not isinstance(resolved_id, str):
        raise _error("invalid_identifier", "cohort identifier must be a quoted string")
    resolved_id = _safe_slug(resolved_id, label="cohort identifier", maximum=80)
    resolved_delivery = delivery or raw.get("delivery") or raw.get("mode") or raw.get("kind")
    if resolved_delivery is None:
        raise _error("delivery_required", "provide --delivery live or self-paced")
    if resolved_delivery == "self-paced":
        resolved_delivery = "self_paced"
    if resolved_delivery not in {"live", "self_paced"}:
        raise _error("invalid_delivery", "delivery must be live or self-paced")
    if "published" in raw and raw["published"] is not False:
        raise _error("publish_requires_review", "bootstrap always creates an unpublished cohort")
    resolved_start = _date_string(start_date if start_date is not None else raw.get("start_date"), label="start_date")
    resolved_end = _date_string(end_date if end_date is not None else raw.get("end_date"), label="end_date")
    if resolved_start and resolved_end and resolved_end < resolved_start:
        raise _error("invalid_date_range", "end_date must not precede start_date")
    title = _text(raw.get("title"), label="title", required=False)
    description = _text(raw.get("description"), label="description", required=False)
    readme = _text(raw.get("readme"), label="readme", required=False)
    return resolved_id, resolved_delivery, resolved_start, resolved_end, title, description, readme


def _module_request_entries(raw: Mapping[str, Any], root: Path) -> list[tuple[str, Mapping[str, Any] | None]]:
    value = raw.get("modules")
    if value is None:
        slugs = _root_module_slugs(root)
        if not slugs:
            raise _error("root_curriculum_missing", "no numbered root modules were found")
        return [(slug, None) for slug in slugs]
    if not isinstance(value, list) or not value:
        raise _error("invalid_schema", "modules must be a non-empty list")
    entries: list[tuple[str, Mapping[str, Any] | None]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        assignment: Mapping[str, Any] | None = None
        if isinstance(item, str):
            slug = item
        else:
            mapping = _mapping(item, label=f"modules[{index}]")
            _strict_keys(
                mapping,
                {"slug", "module", "path", "homework", "assignment"},
                label=f"modules[{index}]",
            )
            slug_value = mapping.get("slug") or mapping.get("module") or mapping.get("path")
            slug = str(slug_value) if slug_value is not None else ""
            assignment_value = mapping.get("homework", mapping.get("assignment"))
            if assignment_value is not None:
                assignment = _mapping(assignment_value, label=f"modules[{index}].homework")
        slug = _safe_module_slug(slug, label=f"modules[{index}]")
        if slug in seen:
            raise _error("duplicate_module", f"module {slug} is listed more than once")
        seen.add(slug)
        entries.append((slug, assignment))
    entries.sort(key=lambda item: _module_sort_key(item[0]))
    return entries


def _homework_mapping_for(raw: Mapping[str, Any], slug: str) -> Mapping[str, Any] | None:
    value = raw.get("homework")
    if value is None:
        return None
    if isinstance(value, dict):
        # A mapping with assignment fields is for the sole module; a mapping
        # keyed by module slug is the compact multi-module form.
        assignment_keys = {
            "slug",
            "title",
            "instructions",
            "instructions_file",
            "content_id",
            "due_at",
            "initial_state",
            "questions",
            "form",
        }
        if set(value) & assignment_keys:
            requested_modules = raw.get("modules")
            if requested_modules is None:
                raise _error(
                    "ambiguous_homework",
                    "top-level homework assignment fields require exactly one listed module",
                )
            if not isinstance(requested_modules, list) or len(requested_modules) != 1:
                raise _error(
                    "ambiguous_homework",
                    "top-level homework assignment fields require exactly one listed module",
                )
            return value
        candidate = value.get(slug)
        if candidate is None:
            return None
        return _mapping(candidate, label=f"homework.{slug}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            mapping = _mapping(item, label=f"homework[{index}]")
            module = mapping.get("module") or mapping.get("module_slug")
            if module == slug:
                result = dict(mapping)
                result.pop("module", None)
                result.pop("module_slug", None)
                return result
        return None
    raise _error("invalid_schema", "homework must be a mapping or list")


def _reject_plaintext_answers(value: object, *, label: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).casefold() in PLAINTEXT_ANSWER_KEYS:
                raise _error("plaintext_answer_key", f"{label} contains a plaintext answer-key field")
            _reject_plaintext_answers(item, label=f"{label}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_plaintext_answers(item, label=f"{label}[{index}]")


def _validate_answer_envelope(
    value: object,
    *,
    course_slug: str,
    homework_slug: str,
    question_id: str,
    label: str,
) -> dict[str, Any]:
    """Validate the website's opaque A256GCM answer envelope without decrypting it."""

    answer = _mapping(value, label=label)
    required = {
        "version",
        "algorithm",
        "kdf",
        "key_id",
        "salt",
        "nonce",
        "ciphertext",
        "context_sha256",
    }
    if set(answer) != required:
        raise _error("invalid_answer_envelope", f"{label} must contain the encrypted answer fields")
    if type(answer["version"]) is not int or answer["version"] != 1 or answer["algorithm"] != "A256GCM" or answer["kdf"] != "HKDF-SHA256":
        raise _error("invalid_answer_envelope", f"{label} has an unsupported encryption envelope")
    _safe_slug(answer["key_id"], label=f"{label}.key_id", maximum=100)
    for key, size in (("salt", 32), ("nonce", 12)):
        encoded = answer[key]
        if not isinstance(encoded, str) or BASE64URL_RE.fullmatch(encoded) is None:
            raise _error("invalid_answer_envelope", f"{label}.{key} is not base64url")
        try:
            decoded = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4))
        except (ValueError, binascii.Error) as exc:
            raise _error("invalid_answer_envelope", f"{label}.{key} is not base64url") from exc
        if len(decoded) != size:
            raise _error("invalid_answer_envelope", f"{label}.{key} has the wrong length")
    ciphertext = answer["ciphertext"]
    if not isinstance(ciphertext, str) or BASE64URL_RE.fullmatch(ciphertext) is None:
        raise _error("invalid_answer_envelope", f"{label}.ciphertext is not base64url")
    try:
        ciphertext_bytes = base64.urlsafe_b64decode(ciphertext + "=" * (-len(ciphertext) % 4))
    except (ValueError, binascii.Error) as exc:
        raise _error("invalid_answer_envelope", f"{label}.ciphertext is not base64url") from exc
    if len(ciphertext_bytes) < 16:
        raise _error("invalid_answer_envelope", f"{label}.ciphertext is too short")
    context = f"dtc-homework-answer:v1\0{course_slug}\0{homework_slug}\0{question_id}".encode()
    expected_context = hashlib.sha256(context).hexdigest()
    if not isinstance(answer["context_sha256"], str) or SHA256_RE.fullmatch(answer["context_sha256"]) is None:
        raise _error("invalid_answer_envelope", f"{label}.context_sha256 is invalid")
    if answer["context_sha256"] != expected_context:
        raise _error("answer_context_mismatch", f"{label}.context_sha256 does not match its assignment")
    return dict(answer)


def _homework_info(
    root: Path,
    course_slug: str,
    cohort_id: str,
    module: str,
    raw: Mapping[str, Any],
    existing_ids: set[str],
) -> HomeworkInfo:
    allowed = {
        "slug",
        "title",
        "instructions",
        "instructions_file",
        "content_id",
        "due_at",
        "initial_state",
        "form",
        "questions",
    }
    _strict_keys(raw, allowed, label=f"homework for {module}")
    slug = _safe_slug(raw.get("slug", f"homework-{module.split('-', 1)[0]}"), label=f"homework {module} slug")
    title = _text(raw.get("title"), label=f"homework {module} title")
    if title is None:  # pragma: no cover - _text(required=True) raises
        raise _error("invalid_schema", f"homework {module} title is required")
    instructions = raw.get("instructions")
    instructions_file = raw.get("instructions_file")
    if instructions is not None and instructions_file is not None:
        raise _error("ambiguous_instructions", f"homework {module} provides both instructions and instructions_file")
    if instructions is not None:
        instructions_text = _text(instructions, label=f"homework {module} instructions")
    elif instructions_file is not None:
        if not isinstance(instructions_file, str):
            raise _error("unsafe_path", f"homework {module} instructions_file must be repository-relative")
        source_rel = _safe_path_string(instructions_file, label=f"homework {module} instructions_file")
        source = root / PurePosixPath(source_rel)
        _assert_no_symlink_components(root, source_rel, label=f"homework {module} instructions_file", allow_missing=False)
        _assert_regular_file(source, label=f"homework {module} instructions_file")
        try:
            instructions_text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise _error("invalid_utf8", f"homework {module} instructions_file is not UTF-8") from exc
    else:
        raise _error("instructions_required", f"homework {module} needs explicit instructions or instructions_file")
    if instructions_text is None or not instructions_text.strip():
        raise _error("instructions_required", f"homework {module} instructions cannot be empty")
    supplied_id = raw.get("content_id")
    if supplied_id is not None:
        raise _error("content_id_forbidden", f"homework {module} content_id is minted by bootstrap")
    content_id = _fresh_deterministic_id(root, f"cohort:{cohort_id}:homework:{module}", existing_ids)
    due_at = None
    if "due_at" not in raw:
        raise _error("due_at_required", f"homework {module} must explicitly set due_at")
    if raw["due_at"] is not None:
        due_at = _timestamp_string(raw["due_at"], label=f"homework {module} due_at")
    if "initial_state" not in raw:
        raise _error("initial_state_required", f"homework {module} must explicitly set initial_state")
    initial_state = raw["initial_state"]
    if initial_state not in {"closed", "open", "scored"}:
        raise _error("invalid_homework_state", f"homework {module} initial_state must be closed, open or scored")
    if "form" not in raw:
        raise _error("form_required", f"homework {module} must provide the complete form mapping")
    form = _mapping(raw["form"], label=f"homework {module} form")
    required_form = {
        "homework_url",
        "time_spent_lectures",
        "time_spent_homework",
        "faq_contribution",
        "learning_in_public_cap",
    }
    if set(form) != required_form:
        raise _error("invalid_form", f"homework {module} form must name the five supported fields")
    for key in required_form - {"learning_in_public_cap"}:
        if type(form[key]) is not bool:
            raise _error("invalid_form", f"homework {module} form.{key} must be boolean")
    if type(form["learning_in_public_cap"]) is not int or not 0 <= form["learning_in_public_cap"] <= 100:
        raise _error("invalid_form", f"homework {module} form.learning_in_public_cap must be 0..100")
    if "questions" not in raw or not isinstance(raw["questions"], list) or not raw["questions"]:
        raise _error("questions_required", f"homework {module} must provide at least one question")
    normalised_questions: list[dict[str, Any]] = []
    question_ids: set[str] = set()
    for index, question_value in enumerate(raw["questions"]):
        question = _mapping(question_value, label=f"homework {module} questions[{index}]")
        allowed_question = {
            "content_id",
            "id",
            "type",
            "prompt",
            "options",
            "points",
            "answer_type",
            "answer",
        }
        _strict_keys(question, allowed_question, label=f"homework {module} questions[{index}]")
        for key in {"id", "type", "prompt", "points"}:
            if key not in question:
                raise _error("question_field_required", f"homework {module} questions[{index}] needs {key}")
        question_id = _safe_slug(question["id"], label=f"homework {module} question id")
        if question_id in question_ids:
            raise _error("duplicate_question_id", f"homework {module} repeats question {question_id}")
        question_ids.add(question_id)
        if not isinstance(question["type"], str) or question["type"] not in {
            "multiple_choice",
            "checkboxes",
            "free_form",
            "free_form_long",
        }:
            raise _error("invalid_question_type", f"homework {module} questions[{index}] has unsupported type")
        if not isinstance(question["prompt"], str) or not question["prompt"].strip():
            raise _error("invalid_question", f"homework {module} questions[{index}] prompt is required")
        if type(question["points"]) is not int or not 0 <= question["points"] <= 1000:
            raise _error("invalid_question", f"homework {module} questions[{index}] points must be 0..1000")
        answer_envelope: dict[str, Any] | None = None
        if question["type"] in {"multiple_choice", "checkboxes"}:
            if "answer_type" in question:
                raise _error("invalid_question", f"homework {module} questions[{index}] cannot have answer_type")
            if not isinstance(question.get("options"), list) or len(question["options"]) < 2:
                raise _error("invalid_question", f"homework {module} questions[{index}] needs two options")
            option_ids: set[str] = set()
            for option_index, option_value in enumerate(question["options"]):
                option = _mapping(
                    option_value,
                    label=f"homework {module} questions[{index}] options[{option_index}]",
                )
                if set(option) != {"id", "label"}:
                    raise _error("invalid_option", f"homework {module} questions[{index}] options need id and label")
                option_id = _safe_slug(option["id"], label=f"homework {module} option id")
                if option_id in option_ids:
                    raise _error("duplicate_option_id", f"homework {module} repeats option {option_id}")
                option_ids.add(option_id)
                if not isinstance(option["label"], str) or not option["label"].strip():
                    raise _error("invalid_option", f"homework {module} option label is required")
            if "answer" not in question:
                raise _error("answer_required", f"homework {module} questions[{index}] needs an encrypted answer")
            answer_envelope = _validate_answer_envelope(
                question["answer"],
                course_slug=course_slug,
                homework_slug=slug,
                question_id=question_id,
                label=f"homework {module} questions[{index}].answer",
            )
        elif question.get("options") is not None:
            raise _error("invalid_question", f"homework {module} questions[{index}] cannot have options")
        else:
            answer_type = question.get("answer_type")
            if answer_type not in {"any", "float", "integer", "exact_string", "contains_string"}:
                raise _error("invalid_answer_type", f"homework {module} questions[{index}] needs a valid answer_type")
            if answer_type == "any" and "answer" in question:
                raise _error("answer_not_allowed", f"homework {module} questions[{index}] answer is not allowed for any")
            if answer_type != "any" and "answer" not in question:
                raise _error("answer_required", f"homework {module} questions[{index}] needs an encrypted answer")
            if answer_type != "any":
                answer_envelope = _validate_answer_envelope(
                    question["answer"],
                    course_slug=course_slug,
                    homework_slug=slug,
                    question_id=question_id,
                    label=f"homework {module} questions[{index}].answer",
                )
        if "content_id" in question:
            raise _error("content_id_forbidden", f"homework {module} question content_id is minted by bootstrap")
        question_content_id = _fresh_deterministic_id(
            root,
            f"cohort:{cohort_id}:homework:{module}:question:{question_id}",
            existing_ids,
        )
        normalised = dict(question)
        normalised["content_id"] = question_content_id
        if answer_envelope is not None:
            normalised["answer"] = answer_envelope
        normalised_questions.append(normalised)
    _reject_plaintext_answers(raw, label=f"homework {module}")
    values: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "content_id": content_id,
        "slug": slug,
        "title": title,
        "instructions_path": "homework.md",
        "due_at": due_at,
        "initial_state": initial_state,
        "form": form,
        "questions": normalised_questions,
    }
    return HomeworkInfo(
        module=module,
        slug=slug,
        title=title,
        instructions=instructions_text,
        content_id=content_id,
        due_at=due_at,
        values=values,
    )


def _request_homework(raw: Mapping[str, Any], module: str, module_assignment: Mapping[str, Any] | None) -> Mapping[str, Any] | None:
    if module_assignment is not None:
        return module_assignment
    return _homework_mapping_for(raw, module)


def _target_status(root: Path, action: WriteAction) -> tuple[bool, str | None]:
    target = root / PurePosixPath(action.path)
    _assert_no_symlink_components(root, action.path, label=action.path, allow_missing=True)
    if target.exists() or target.is_symlink():
        if target.is_symlink():
            raise _error("symlink_rejected", f"target {action.path} is a symlink")
        if not target.is_file():
            raise _error("overwrite_refused", f"target {action.path} is not a regular file")
        try:
            existing = target.read_bytes()
        except OSError as exc:
            raise _error("read_failed", f"cannot inspect target {action.path}") from exc
        if existing == action.data:
            return False, action.path
        if not action.replace:
            raise _error("overwrite_refused", f"target {action.path} already contains different content")
        if action.expected_sha256 and hashlib.sha256(existing).hexdigest() != action.expected_sha256:
            raise _error("concurrent_change", f"target {action.path} changed during archive planning")
        return True, None
    return True, None


def _prepare_actions(root: Path, actions: Iterable[WriteAction]) -> tuple[tuple[WriteAction, ...], tuple[str, ...]]:
    writes: list[WriteAction] = []
    skips: list[str] = []
    seen: set[str] = set()
    for action in sorted(actions, key=lambda item: item.path):
        _safe_path_string(action.path, label="write target")
        if action.path in seen:
            raise _error("duplicate_target", f"planned target {action.path} appears more than once")
        seen.add(action.path)
        changed, skipped = _target_status(root, action)
        if changed:
            writes.append(action)
        elif skipped:
            skips.append(skipped)
    return tuple(writes), tuple(skips)


def _module_paths(root: Path, modules: Sequence[ModuleInfo]) -> set[str]:
    paths: set[str] = set()
    for module in modules:
        for path in _walk_files(root / module.slug, label=f"module {module.slug}"):
            paths.add(_relative_to_root(path, root, label=f"module {module.slug} file"))
    return paths


def _iter_prose_targets(text: str) -> Iterator[str]:
    # Parse definitions before uses so reference-style links are checked even
    # when the definition appears later in the document.  Fenced code is not
    # prose and must never turn an example URL/path into a dependency.
    fence: str | None = None
    prose_lines: list[str] = []
    for line in text.splitlines():
        fence_match = FENCE_RE.match(line)
        if fence is None and fence_match:
            fence = fence_match.group(1)[0] * 3
            continue
        if fence is not None:
            if fence_match and fence_match.group(1)[0] * 3 == fence:
                fence = None
            continue
        prose_lines.append(line)

    definitions: dict[str, str] = {}
    for line in prose_lines:
        match = MD_REFERENCE_DEFINITION_RE.match(line)
        if not match:
            continue
        label = re.sub(r"\s+", " ", match.group(1).strip()).casefold()
        target = match.group(2).strip()
        if target.startswith("<") and ">" in target:
            target = target[1 : target.index(">")].strip()
        else:
            target = target.split()[0]
        if label in definitions and definitions[label] != target:
            raise _error("ambiguous_link_reference", "Markdown reference label has conflicting definitions")
        definitions[label] = target

    for line in prose_lines:
        for match in MD_LINK_RE.finditer(line):
            target = match.group(2).strip()
            if target.startswith("<") and ">" in target:
                target = target[1 : target.index(">")].strip()
            else:
                target = target.split()[0]
            if target:
                yield target
        for match in HTML_LINK_RE.finditer(line):
            yield match.group(1).strip()
        for match in MD_REFERENCE_USE_RE.finditer(line):
            # `[]` is the collapsed form: use the text label from the first
            # bracket.  Keep the label normalization identical to definition
            # parsing so case and line wrapping remain harmless.
            label = (match.group(2) or match.group(1)).strip()
            target = definitions.get(re.sub(r"\s+", " ", label).casefold())
            if target:
                yield target
        for match in MD_SHORTCUT_REFERENCE_RE.finditer(line):
            target = definitions.get(re.sub(r"\s+", " ", match.group(1)).casefold())
            if target:
                yield target


def _repository_key_from_url(value: object) -> tuple[str, str] | None:
    if not isinstance(value, str) or not value.strip():
        return None
    parsed = urlsplit(value.strip())
    host = (parsed.hostname or "").casefold()
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    if parts[1].endswith(".git"):
        parts[1] = parts[1][:-4]
    if not host or not parts[0] or not parts[1]:
        return None
    return host, f"{parts[0].casefold()}/{parts[1].casefold()}"


def _moving_repository_url(root: Path, target: str) -> bool:
    """Return whether an absolute URL points at this checkout's moving tree."""

    parsed = urlsplit(target)
    host = (parsed.hostname or "").casefold()
    if not parsed.scheme and not parsed.netloc:
        return False
    # GitHub's HTML and raw hosts both encode owner/repository in the first
    # two path components.  A missing repository declaration is handled
    # conservatively: refuse GitHub links rather than claim they are frozen.
    github_host = host in {"github.com", "www.github.com", "raw.githubusercontent.com"}
    candidate = _repository_key_from_url(target)
    if candidate is None:
        return False
    course_path = root / "course.yaml"
    configured: tuple[str, str] | None = None
    if course_path.exists() and not course_path.is_symlink():
        mapping = _mapping(_yaml_load(course_path, label="course.yaml"), label="course.yaml")
        configured = _repository_key_from_url(mapping.get("repository_url"))
    if github_host and configured is None:
        return True
    if configured is None:
        return False
    configured_host, configured_repo = configured
    candidate_host, candidate_repo = candidate
    if candidate_repo != configured_repo:
        return False
    # A GitHub raw URL has a different host from the configured HTML URL, but
    # both are the same moving repository.  For custom hosts require host
    # equality so an unrelated project with the same path is not rejected.
    return github_host or candidate_host == configured_host


def _resolved_local_target(root: Path, source: Path, target: str) -> str | None:
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        if parsed.scheme.casefold() == "file":
            raise _error("unsafe_link", f"file URL in {_relative_to_root(source, root, label='source link')}")
        if _moving_repository_url(root, target):
            source_rel = _relative_to_root(source, root, label="source link")
            raise _error(
                "moving_repository_dependency",
                f"{source_rel} links to the moving repository URL; use a relative local asset or review the archive",
            )
        return None
    raw_path = parsed.path
    if not raw_path or raw_path.startswith("#"):
        return None
    if "%2f" in raw_path.casefold() or "%5c" in raw_path.casefold():
        raise _error("unsafe_link", f"encoded path separator in {source.name}")
    decoded = unquote(raw_path)
    if decoded.startswith("/") or "\\" in decoded:
        raise _error("unsafe_link", f"absolute or backslash link in {source.name}")
    source_rel = _relative_to_root(source, root, label="source link")
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_rel), decoded))
    if resolved == "." or resolved == ".." or resolved.startswith("../"):
        raise _error("external_root_dependency", f"link from {source_rel} leaves selected root modules")
    return resolved


def _check_module_links(root: Path, modules: Sequence[ModuleInfo]) -> tuple[str, ...]:
    selected = {module.slug for module in modules}
    checks: list[str] = []
    selected_paths = _module_paths(root, modules)
    for module in modules:
        for path in _walk_files(root / module.slug, label=f"module {module.slug}"):
            if path.suffix.casefold() not in {".md", ".markdown", ".html", ".htm"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                raise _error("invalid_utf8", f"Markdown file {_relative_to_root(path, root, label='link source')} is not UTF-8") from exc
            source_rel = _relative_to_root(path, root, label="link source")
            for target in _iter_prose_targets(text):
                resolved = _resolved_local_target(root, path, target)
                if resolved is None:
                    continue
                first = PurePosixPath(resolved).parts[0]
                if MODULE_RE.fullmatch(first) and first not in selected:
                    raise _error("external_root_dependency", f"{source_rel} links to unselected module {first}")
                if first not in selected:
                    raise _error("external_root_dependency", f"{source_rel} links outside the selected root modules")
                target_path = root / PurePosixPath(resolved)
                if target_path.is_dir() and not target_path.is_symlink():
                    target_path = target_path / "README.md"
                    resolved = f"{resolved}/README.md"
                if resolved not in selected_paths:
                    raise _error("missing_dependency", f"{source_rel} links to unavailable local path")
                _assert_regular_file(target_path, label=f"link target {resolved}")
            checks.append(source_rel)
    return tuple(sorted(checks))


def _cohort_yaml(
    root: Path,
    course_slug: str,
    cohort_id: str,
    delivery: str,
    start_date: str | None,
    end_date: str | None,
    title: str | None,
    description: str | None,
    modules: Sequence[ModuleInfo],
    homework: Sequence[HomeworkInfo],
    cohort_content_id: str,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "content_id": cohort_content_id,
        "identifier": cohort_id,
        "course": course_slug,
        "delivery": delivery,
        "curriculum": "current",
        "published": False,
        "start_date": start_date,
        "end_date": end_date,
    }
    if title is not None:
        result["title"] = title
    if description is not None:
        result["description"] = description
    result["homework"] = [
        {
            "module": item.module,
            "source": f"cohorts/{cohort_id}/homework/{item.module}/homework.yaml",
        }
        for item in homework
    ]
    return result


def _cohort_readme(
    cohort_id: str,
    delivery: str,
    title: str | None,
    description: str | None,
    modules: Sequence[ModuleInfo],
    homework: Sequence[HomeworkInfo],
    custom: str | None,
) -> str:
    if custom is not None:
        return custom if custom.endswith("\n") else custom + "\n"
    heading = title or f"Zoomcamp {cohort_id}"
    lines = [f"# {heading}", "", f"Delivery: {delivery}", ""]
    if description:
        lines.extend([description, ""])
    lines.extend(["## Curriculum", ""])
    homework_by_module = {item.module: item for item in homework}
    for module in modules:
        line = f"- [{module.title or module.slug}](../../{module.slug}/)"
        assignment = homework_by_module.get(module.slug)
        if assignment:
            line += f" · [homework](homework/{module.slug}/homework.md)"
        lines.append(line)
    lines.extend(
        [
            "",
            "The lessons are shared current curriculum. This cohort directory contains delivery-specific instructions and homework only.",
            "",
        ]
    )
    return "\n".join(lines)


def build_bootstrap_plan(
    repo_root: str | Path,
    *,
    request_path: str | Path | None = None,
    cohort_id: str | None = None,
    delivery: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    module_slugs: Sequence[str] | None = None,
) -> Plan:
    root = _repo_root(repo_root)
    _require_new_layout(root)
    course_slug, _course_version = _course_identity(root)
    request = _load_request(Path(request_path) if request_path else None, operation="bootstrap")
    if module_slugs:
        raise _error(
            "module_subset_unsupported",
            "bootstrap always references the complete root curriculum; use request.modules for homework authoring",
        )
    resolved = _cohort_fields(
        request,
        cohort_id=cohort_id,
        delivery=delivery,
        start_date=start_date,
        end_date=end_date,
    )
    identifier, mode, begin, finish, title, description, readme = resolved
    entries = _module_request_entries(request, root)
    # A current cohort points at the one shared root graph.  `modules` in a
    # request therefore selects only which modules receive explicitly authored
    # homework; it can never create a partial current curriculum reference.
    all_root_slugs = _root_module_slugs(root)
    modules = [_module_info(root, slug) for slug in all_root_slugs]
    entry_by_slug = {slug: assignment for slug, assignment in entries}
    unknown_requested = sorted(set(entry_by_slug) - set(all_root_slugs), key=_module_sort_key)
    if unknown_requested:
        raise _error("missing_path", f"requested module {unknown_requested[0]} is not a root module")
    entries = [(slug, entry_by_slug.get(slug)) for slug in all_root_slugs if slug in entry_by_slug]
    module_ids = [module.content_id for module in modules if module.content_id]
    if len(module_ids) != len(set(module_ids)):
        raise _error("duplicate_content_id", "root module content IDs are not unique")
    existing_ids = _existing_content_ids(root)
    # A replay must retain the IDs minted by the first apply.  They are still
    # present in the repository-wide scan, but belong to this exact target and
    # therefore are not a reuse collision.  A conflicting target is caught by
    # the byte-for-byte preflight below.
    reusable_ids: set[str] = set()
    cohort_target = root / "cohorts" / identifier
    candidate_paths = [cohort_target / "cohort.yaml"]
    for slug, assignment in entries:
        if _request_homework(request, slug, assignment) is not None:
            candidate_paths.append(cohort_target / "homework" / slug / "homework.yaml")
    for candidate_path in candidate_paths:
        if not candidate_path.exists() or candidate_path.is_symlink() or not candidate_path.is_file():
            continue
        try:
            _mapping(
                _yaml_load(candidate_path, label="existing bootstrap target"),
                label="existing bootstrap target",
            )
        except BootstrapError:
            continue
        # Reusing IDs from this exact target is what makes an exact replay
        # deterministic.  Include nested question IDs as well as the
        # manifest ID; a lexical scan is enough and avoids exposing bodies.
        try:
            reusable_ids.update(match.group(1).lower() for match in UUID_RE.finditer(candidate_path.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            continue
    existing_ids.difference_update(reusable_ids)
    cohort_content_id = _fresh_deterministic_id(root, f"cohort:{identifier}", existing_ids)
    homework: list[HomeworkInfo] = []
    for slug, assignment in entries:
        raw_assignment = _request_homework(request, slug, assignment)
        if raw_assignment is None:
            continue
        if mode == "self_paced":
            raise _error(
                "self_paced_homework_unsupported",
                "self-paced bootstrap currently creates practice access with homework: []; author graded homework separately",
            )
        homework.append(_homework_info(root, course_slug, identifier, slug, raw_assignment, existing_ids))
    actions: list[WriteAction] = []
    cohort_dir = f"cohorts/{identifier}"
    manifest = _cohort_yaml(
        root,
        course_slug,
        identifier,
        mode,
        begin,
        finish,
        title,
        description,
        modules,
        homework,
        cohort_content_id,
    )
    actions.append(
        WriteAction(
            path=f"{cohort_dir}/cohort.yaml",
            reason="new cohort manifest referencing root modules",
            data=_yaml_dump(manifest),
        )
    )
    actions.append(
        WriteAction(
            path=f"{cohort_dir}/README.md",
            reason="cohort delivery index",
            data=_cohort_readme(identifier, mode, title, description, modules, homework, readme).encode("utf-8"),
        )
    )
    for item in homework:
        base = f"{cohort_dir}/homework/{item.module}"
        actions.append(
            WriteAction(
                path=f"{base}/homework.md",
                reason=f"explicit instructions for {item.module}",
                data=(item.instructions if item.instructions.endswith("\n") else item.instructions + "\n").encode("utf-8"),
            )
        )
        actions.append(
            WriteAction(
                path=f"{base}/homework.yaml",
                reason=f"new assignment metadata for {item.module}",
                data=_yaml_dump(item.values),
            )
        )
    writes, skips = _prepare_actions(root, actions)
    checks = [
        "root numbered modules inspected",
        "shared lesson and module files are referenced, never copied",
        "no cohort-owned v1 module manifests found",
        "new cohort and assignment IDs are fresh and deterministic",
        "dates, grading fields and answer material are request-only",
    ]
    return Plan(
        operation="bootstrap",
        repo_root=root,
        writes=writes,
        skips=skips,
        checks=tuple(checks),
        metadata={
            "cohort": identifier,
            "delivery": mode,
            "modules": [module.slug for module in modules],
            "homework": [item.module for item in homework],
            "cohort_content_id": cohort_content_id,
        },
    )


def _archive_modules(raw: Mapping[str, Any], root: Path, cli_modules: Sequence[str] | None) -> tuple[str, ...]:
    selected: list[str] = []
    value = raw.get("modules")
    if cli_modules:
        value = list(cli_modules)
    if value is None:
        selected = list(_root_module_slugs(root))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, str):
                slug = item
            else:
                mapping = _mapping(item, label=f"archive modules[{index}]")
                _strict_keys(mapping, {"slug", "module", "path"}, label=f"archive modules[{index}]")
                slug_value = mapping.get("slug") or mapping.get("module") or mapping.get("path")
                slug = str(slug_value) if slug_value is not None else ""
            selected.append(_safe_module_slug(slug, label=f"archive modules[{index}]"))
    else:
        raise _error("invalid_schema", "archive modules must be a list")
    deduped = sorted(set(selected), key=_module_sort_key)
    if not deduped:
        raise _error("root_curriculum_missing", "no numbered root modules were found")
    return tuple(deduped)


def _archive_manifest(
    identifier: str,
    modules: Sequence[ModuleInfo],
    root: Path,
) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for module in modules:
        files: list[dict[str, str]] = []
        for path in _walk_files(root / module.slug, label=f"module {module.slug}"):
            rel = path.relative_to(root / module.slug).as_posix()
            data = path.read_bytes()
            files.append({"path": rel, "sha256": hashlib.sha256(data).hexdigest()})
        entries.append({"slug": module.slug, "files": files})
    return {
        "schema_version": SCHEMA_VERSION,
        "kind": "curriculum_archive",
        "identifier": identifier,
        "modules": entries,
    }


def _archive_manifest_request(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"schema_version": SCHEMA_VERSION}
    _assert_regular_file(path, label="archive manifest")
    loaded = _mapping(_yaml_load(path, label="archive manifest"), label="archive manifest")
    version = loaded.get("schema_version", SCHEMA_VERSION)
    if type(version) is not int or version != SCHEMA_VERSION:
        raise _error("unsupported_schema", "archive schema_version must be integer 2")
    if loaded.get("operation") not in {None, "archive"}:
        raise _error("operation_mismatch", "archive manifest operation is not archive")
    _strict_keys(loaded, {"schema_version", "operation", "modules", "delivery"}, label="archive manifest")
    if "delivery" in loaded:
        value = loaded["delivery"]
        if value == "self-paced":
            value = "self_paced"
        if value not in {"live", "self_paced"}:
            raise _error("invalid_delivery", "archive delivery must be live or self-paced")
        loaded["delivery"] = value
    return loaded


ARCHIVE_NOTICE_PREFIX = "<!-- zoomcamp-archive-notice:v2:"


def _archive_notice_marker(identifier: str) -> str:
    return f"{ARCHIVE_NOTICE_PREFIX}{identifier} -->"


def _archive_notice(identifier: str, modules: Sequence[ModuleInfo]) -> str:
    lines = [
        _archive_notice_marker(identifier),
        f"## Archived curriculum: {identifier}",
        "",
        "This cohort preserves the complete local curriculum tree used for this delivery. "
        "It is an archive and is not imported as the current website curriculum.",
        "",
        "### Archived modules",
        "",
    ]
    lines.extend(f"- [{module.title or module.slug}]({module.slug}/)" for module in modules)
    lines.extend(["", "The root numbered modules remain the editable current curriculum.", ""])
    return "\n".join(lines)


def _archive_notice_bytes(
    root: Path,
    identifier: str,
    modules: Sequence[ModuleInfo],
) -> tuple[bytes, bool]:
    """Return notice bytes and whether an existing README may be replaced."""

    readme = root / "cohorts" / identifier / "README.md"
    notice = _archive_notice(identifier, modules)
    if not readme.exists():
        return notice.encode("utf-8"), False
    _assert_regular_file(readme, label=f"archive {identifier}/README.md")
    try:
        existing = readme.read_bytes()
    except OSError as exc:
        raise _error("read_failed", f"cannot inspect archive {identifier}/README.md") from exc
    try:
        text = existing.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _error("invalid_utf8", f"archive {identifier}/README.md is not UTF-8") from exc
    marker = _archive_notice_marker(identifier)
    if marker in text:
        # A prior archive operation owns the marker.  Preserve all authored
        # prose and avoid attempting a broad Markdown rewrite on replay.
        return existing, False
    if ARCHIVE_NOTICE_PREFIX in text:
        raise _error("archive_notice_conflict", "archive README has a notice for another cohort")
    separator = "" if not text or text.endswith("\n") else "\n"
    updated = text + separator + "\n" + notice
    return updated.encode("utf-8"), True


def _validate_existing_archive_homework(root: Path, identifier: str, value: object) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        raise _error("invalid_schema", f"cohorts/{identifier}/cohort.yaml homework must be a list")
    prefix = f"cohorts/{identifier}/"
    for index, item in enumerate(value):
        if not isinstance(item, dict) or set(item) != {"module", "source"}:
            raise _error(
                "invalid_schema",
                f"cohorts/{identifier}/cohort.yaml homework[{index}] needs module and source",
            )
        source = _safe_path_string(item["source"], label=f"cohort homework[{index}] source")
        if not source.startswith(prefix) or not source.endswith("/homework.yaml"):
            raise _error("unsafe_path", f"cohort homework[{index}] source must stay inside its cohort")
        _assert_no_symlink_components(root, source, label=f"cohort homework[{index}] source", allow_missing=False)
        _assert_regular_file(root / PurePosixPath(source), label=f"cohort homework[{index}] source")
        instructions = f"{posixpath.dirname(source)}/homework.md"
        _assert_no_symlink_components(root, instructions, label=f"cohort homework[{index}] instructions", allow_missing=False)
        _assert_regular_file(root / PurePosixPath(instructions), label=f"cohort homework[{index}] instructions")
        loaded = _yaml_load(root / PurePosixPath(source), label=f"cohort homework[{index}] source")
        _reject_plaintext_answers(loaded, label=f"cohort homework[{index}] source")


def _archive_cohort_manifest(
    root: Path,
    course_slug: str,
    identifier: str,
    *,
    delivery: str | None,
    notice_path: str,
    existing_ids: set[str],
) -> tuple[dict[str, Any], bool, str | None]:
    """Build the v2 archive classifier, preserving existing delivery data."""

    path = root / "cohorts" / identifier / "cohort.yaml"
    if path.exists() or path.is_symlink():
        _assert_regular_file(path, label=f"archive {identifier}/cohort.yaml")
        mapping = _mapping(_yaml_load(path, label=f"archive {identifier}/cohort.yaml"), label="archive cohort manifest")
        if mapping.get("schema_version") != SCHEMA_VERSION:
            raise _error(
                "migration_required",
                f"cohorts/{identifier}/cohort.yaml is not v2; migrate it before archiving",
            )
        if not isinstance(mapping.get("identifier"), str) or mapping["identifier"] != identifier:
            raise _error("invalid_schema", f"cohorts/{identifier}/cohort.yaml identifier must match its path")
        if mapping.get("course") != course_slug:
            raise _error("invalid_schema", f"cohorts/{identifier}/cohort.yaml course does not match course.yaml")
        _canonical_uuid(mapping.get("content_id"), label=f"cohorts/{identifier}/cohort.yaml content_id")
        if mapping.get("delivery") not in {"live", "self_paced"}:
            raise _error("invalid_delivery", f"cohorts/{identifier}/cohort.yaml delivery is invalid")
        if mapping.get("curriculum") not in {"current", "github_archive"}:
            raise _error("invalid_schema", f"cohorts/{identifier}/cohort.yaml curriculum is invalid")
        if "published" in mapping and type(mapping["published"]) is not bool:
            raise _error("invalid_schema", f"cohorts/{identifier}/cohort.yaml published must be boolean")
        _validate_existing_archive_homework(root, identifier, mapping.get("homework"))
        updated = dict(mapping)
        updated["curriculum"] = "github_archive"
        if "homework" in mapping:
            homework = mapping["homework"]
            archived_homework: list[dict[str, Any]] = []
            for index, item in enumerate(homework):
                if not isinstance(item, dict) or set(item) != {"module", "source"}:
                    raise _error(
                        "invalid_schema",
                        f"cohorts/{identifier}/cohort.yaml homework[{index}] needs module and source",
                    )
                archived_item = dict(item)
                # Archive homework remains operational, but no historical
                # module row exists for its binding.  The homework manifest
                # and its due date stay untouched; only the binding changes.
                archived_item["module"] = None
                archived_homework.append(archived_item)
            updated["homework"] = archived_homework
        # Do not retain a mutable branch/commit claim from an older tool.  The
        # importer derives the immutable source URL from its incoming commit.
        updated["archive"] = {"notice_path": notice_path}
        return updated, True, hashlib.sha256(path.read_bytes()).hexdigest()

    resolved_delivery = delivery or "live"
    if resolved_delivery == "self-paced":
        resolved_delivery = "self_paced"
    if resolved_delivery not in {"live", "self_paced"}:
        raise _error("invalid_delivery", "archive delivery must be live or self-paced")
    content_id = _fresh_deterministic_id(root, f"cohort:{identifier}", existing_ids)
    return (
        {
            "schema_version": SCHEMA_VERSION,
            "content_id": content_id,
            "identifier": identifier,
            "course": course_slug,
            "delivery": resolved_delivery,
            "curriculum": "github_archive",
            "published": False,
            "start_date": None,
            "end_date": None,
            "archive": {"notice_path": notice_path},
            "homework": [],
        },
        False,
        None,
    )


def build_archive_plan(
    repo_root: str | Path,
    *,
    cohort_id: str,
    archive_id: str | None = None,
    manifest_path: str | Path | None = None,
    module_slugs: Sequence[str] | None = None,
    delivery: str | None = None,
) -> Plan:
    root = _repo_root(repo_root)
    _require_new_layout(root)
    course_slug, _course_version = _course_identity(root)
    identifier = _safe_slug(archive_id or cohort_id, label="archive identifier", maximum=80)
    request = _archive_manifest_request(Path(manifest_path) if manifest_path else None)
    if delivery is not None:
        if delivery == "self-paced":
            delivery = "self_paced"
        if delivery not in {"live", "self_paced"}:
            raise _error("invalid_delivery", "archive delivery must be live or self-paced")
    requested_delivery = delivery or request.get("delivery")
    selected_slugs = _archive_modules(request, root, module_slugs)
    modules = [_module_info(root, slug) for slug in selected_slugs]
    module_ids = [module.content_id for module in modules]
    if len(module_ids) != len(set(module_ids)):
        raise _error("duplicate_content_id", "selected root module content IDs are not unique")
    selected_paths = _module_paths(root, modules)
    _check_module_links(root, modules)
    # A root curriculum should never carry answer keys.  We inspect YAML
    # values for known answer-key field names but do not regex-rewrite code.
    for module in modules:
        for path in _walk_files(root / module.slug, label=f"module {module.slug}"):
            if path.suffix.lower() not in {".yaml", ".yml"}:
                continue
            loaded = _yaml_load(path, label=_relative_to_root(path, root, label="archive source"))
            _reject_plaintext_answers(loaded, label=_relative_to_root(path, root, label="archive source"))
    actions: list[WriteAction] = []
    destination_root = f"cohorts/{identifier}"
    notice_path = f"{destination_root}/README.md"
    existing_ids = _existing_content_ids(root)
    cohort_manifest, replacing_manifest, expected_manifest_hash = _archive_cohort_manifest(
        root,
        course_slug,
        identifier,
        delivery=requested_delivery,
        notice_path=notice_path,
        existing_ids=existing_ids,
    )
    for module in modules:
        source_dir = root / module.slug
        for path in _walk_files(source_dir, label=f"module {module.slug}"):
            relative = path.relative_to(source_dir).as_posix()
            destination = f"{destination_root}/{module.slug}/{relative}"
            data = path.read_bytes()
            mode = path.stat().st_mode & 0o777
            actions.append(
                WriteAction(
                    path=destination,
                    reason=f"complete archived tree for {module.slug}",
                    data=data,
                    mode=mode,
                )
            )
    archive_manifest = _archive_manifest(identifier, modules, root)
    actions.append(
        WriteAction(
            path=f"{destination_root}/archive.yaml",
            reason="archive provenance and file checksums",
            data=_yaml_dump(archive_manifest),
        )
    )
    actions.append(
        WriteAction(
            path=f"{destination_root}/cohort.yaml",
            reason="v2 archive curriculum classifier",
            data=_yaml_dump(cohort_manifest),
            replace=replacing_manifest,
            expected_sha256=expected_manifest_hash,
        )
    )
    notice_data, replace_notice = _archive_notice_bytes(root, identifier, modules)
    notice_existing = root / PurePosixPath(notice_path)
    notice_hash = hashlib.sha256(notice_existing.read_bytes()).hexdigest() if replace_notice else None
    actions.append(
        WriteAction(
            path=notice_path,
            reason="archive notice with local module links",
            data=notice_data,
            replace=replace_notice,
            expected_sha256=notice_hash,
        )
    )
    writes, skips = _prepare_actions(root, actions)
    # If an archive directory already contains files not represented by this
    # operation, refuse rather than silently coexisting with an unknown copy.
    target_dir = root / destination_root
    if target_dir.exists() and not target_dir.is_symlink():
        # A cohort may already contain its delivery README, cohort manifest
        # and homework.  Only an extra file inside one of the selected module
        # trees is ambiguous and therefore a conflict.
        planned = {root / PurePosixPath(action.path) for action in actions}
        for module in modules:
            module_destination = target_dir / module.slug
            if not module_destination.exists():
                continue
            for existing in _walk_files(
                module_destination, label=f"archive destination {identifier}/{module.slug}"
            ):
                if existing not in planned:
                    raise _error(
                        "archive_destination_extra",
                        f"archive destination contains unplanned file in {module.slug}",
                    )
    return Plan(
        operation="archive",
        repo_root=root,
        writes=writes,
        skips=skips,
        checks=(
            "all selected root module files included",
            "selected module assets and companion code retained byte-for-byte",
            "local Markdown links resolve",
            "cross-module links target selected modules only",
            "no code or Markdown rewrite performed",
            "archive writes are additive; root curriculum is untouched",
        ),
        metadata={
            "cohort": identifier,
            "modules": list(selected_slugs),
            "file_count": len(selected_paths),
        },
    )


def apply_plan(plan: Plan) -> None:
    """Apply a fully preflighted plan and roll back every changed file on failure."""

    root = plan.repo_root
    created_files: list[Path] = []
    created_dirs: list[Path] = []
    replaced_files: list[tuple[Path, bytes, int]] = []
    try:
        for action in plan.writes:
            target = root / PurePosixPath(action.path)
            parent = target.parent
            # Create parents one at a time so every component can be checked
            # for symlink replacement immediately before use.
            missing: list[Path] = []
            cursor = parent
            while cursor != root and not cursor.exists():
                missing.append(cursor)
                cursor = cursor.parent
            if cursor != root:
                _assert_no_symlink_components(root, _relative_to_root(cursor, root, label="target parent"), label="target parent", allow_missing=False)
            for directory in reversed(missing):
                directory.mkdir(mode=0o755)
                created_dirs.append(directory)
            _assert_no_symlink_components(root, action.path, label=action.path, allow_missing=True)
            if action.replace:
                _assert_regular_file(target, label=action.path)
                old_data = target.read_bytes()
                if old_data == action.data:
                    continue
                if action.expected_sha256 and hashlib.sha256(old_data).hexdigest() != action.expected_sha256:
                    raise _error("concurrent_change", f"target {action.path} changed during archive planning")
                old_mode = target.stat().st_mode & 0o777
                temporary: Path | None = None
                try:
                    fd, temporary_name = tempfile.mkstemp(
                        prefix=f".{target.name}.bootstrap-",
                        dir=parent,
                    )
                    temporary = Path(temporary_name)
                    os.fchmod(fd, action.mode)
                    with os.fdopen(fd, "wb") as stream:
                        stream.write(action.data)
                        stream.flush()
                        os.fsync(stream.fileno())
                    _assert_no_symlink_components(root, action.path, label=action.path, allow_missing=False)
                    # The target was hashed immediately before this atomic
                    # replacement.  A concurrent mutation is refused rather
                    # than clobbered.
                    if hashlib.sha256(target.read_bytes()).hexdigest() != hashlib.sha256(old_data).hexdigest():
                        raise _error("concurrent_change", f"target {action.path} changed during archive apply")
                    os.replace(temporary, target)
                    temporary = None
                    replaced_files.append((target, old_data, old_mode))
                finally:
                    if temporary is not None:
                        try:
                            temporary.unlink()
                        except OSError:
                            pass
            else:
                try:
                    fd = os.open(
                        target,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                        action.mode,
                    )
                except FileExistsError as exc:
                    raise _error("overwrite_refused", f"target {action.path} appeared during apply") from exc
                try:
                    os.fchmod(fd, action.mode)
                    with os.fdopen(fd, "wb") as stream:
                        stream.write(action.data)
                        stream.flush()
                        os.fsync(stream.fileno())
                except Exception:
                    try:
                        target.unlink()
                    except OSError:
                        pass
                    raise
                created_files.append(target)
    except Exception:
        # Restore controlled archive metadata updates first, then remove newly
        # created files/directories.  Restoration itself is atomic and never
        # follows a symlinked target.
        for path, old_data, old_mode in reversed(replaced_files):
            temporary: Path | None = None
            try:
                _assert_no_symlink_components(root, _relative_to_root(path, root, label="rollback target"), label="rollback target", allow_missing=False)
                fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.bootstrap-rollback-", dir=path.parent)
                temporary = Path(temporary_name)
                os.fchmod(fd, old_mode)
                with os.fdopen(fd, "wb") as stream:
                    stream.write(old_data)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, path)
                temporary = None
            except OSError:
                # Keep the original exception as the actionable diagnostic;
                # callers still receive the preflight/apply failure.
                pass
            finally:
                if temporary is not None:
                    try:
                        temporary.unlink()
                    except OSError:
                        pass
        for path in reversed(created_files):
            try:
                path.unlink()
            except OSError:
                pass
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise


def _print_plan(plan: Plan, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(plan.as_dict(), sort_keys=True, indent=2))
    else:
        print(plan.render())


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan or safely apply a Zoomcamp cohort bootstrap/archive operation."
    )
    sub = parser.add_subparsers(dest="command")

    def common(command: argparse.ArgumentParser) -> None:
        command.add_argument("repo", nargs="?", help="course repository checkout")
        command.add_argument("--repo-root", dest="repo_root", help="course repository checkout")
        command.add_argument("--json", action="store_true", help="emit machine-readable plan")
        command.add_argument("--apply", action="store_true", help="apply after successful preflight")

    bootstrap = sub.add_parser("bootstrap", help="create a cohort reference and explicit homework")
    common(bootstrap)
    bootstrap.add_argument("--request", type=Path, help="bootstrap request YAML")
    bootstrap.add_argument("--cohort", help="new cohort identifier")
    bootstrap.add_argument("--delivery", choices=("live", "self-paced"))
    bootstrap.add_argument("--start-date")
    bootstrap.add_argument("--end-date")
    bootstrap.add_argument("--module", dest="modules", action="append", help="root module (repeatable)")

    plan = sub.add_parser("plan", help="read-only plan (bootstrap by default)")
    common(plan)
    plan.add_argument("--operation", choices=("bootstrap", "archive"), default="bootstrap")
    plan.add_argument("--request", type=Path, help="bootstrap or archive request YAML")
    plan.add_argument("--archive-manifest", type=Path)
    plan.add_argument("--cohort")
    plan.add_argument("--archive-id")
    plan.add_argument("--delivery", choices=("live", "self-paced"))
    plan.add_argument("--start-date")
    plan.add_argument("--end-date")
    plan.add_argument("--module", dest="modules", action="append")

    archive = sub.add_parser("archive", help="archive complete root module trees")
    common(archive)
    archive.add_argument("--cohort", required=True, help="outgoing cohort identifier")
    archive.add_argument("--archive-id")
    archive.add_argument("--archive-manifest", type=Path)
    archive.add_argument("--request", type=Path, dest="archive_manifest", help=argparse.SUPPRESS)
    archive.add_argument("--delivery", choices=("live", "self-paced"), help="delivery type to retain in a new archive manifest")
    archive.add_argument("--module", dest="modules", action="append", help="root module (repeatable)")
    return parser


def _normalise_argv(argv: Sequence[str]) -> list[str]:
    if argv and argv[0] not in {"bootstrap", "archive", "plan", "-h", "--help"}:
        return ["bootstrap", *argv]
    if not argv:
        return ["bootstrap"]
    return list(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(_normalise_argv(list(argv if argv is not None else sys.argv[1:])))
    command = args.command or "bootstrap"
    repo_value = getattr(args, "repo_root", None) or getattr(args, "repo", None)
    if repo_value is None:
        print("error[repo_required]: provide REPO or --repo-root", file=sys.stderr)
        return 2
    if command == "plan" and getattr(args, "apply", False):
        print("error[apply_requires_operation]: use bootstrap or archive with --apply", file=sys.stderr)
        return 2
    if (command == "archive" or (command == "plan" and args.operation == "archive")) and not args.cohort:
        print("error[cohort_required]: provide --cohort for an archive", file=sys.stderr)
        return 2
    try:
        if command == "archive" or (command == "plan" and args.operation == "archive"):
            if command == "archive":
                manifest = getattr(args, "archive_manifest", None)
            else:
                manifest = getattr(args, "archive_manifest", None) or getattr(args, "request", None)
            plan = build_archive_plan(
                repo_value,
                cohort_id=args.cohort,
                archive_id=getattr(args, "archive_id", None),
                manifest_path=manifest,
                module_slugs=getattr(args, "modules", None),
                delivery=getattr(args, "delivery", None),
            )
        else:
            plan = build_bootstrap_plan(
                repo_value,
                request_path=getattr(args, "request", None),
                cohort_id=getattr(args, "cohort", None),
                delivery=getattr(args, "delivery", None),
                start_date=getattr(args, "start_date", None),
                end_date=getattr(args, "end_date", None),
                module_slugs=getattr(args, "modules", None),
            )
        _print_plan(plan, as_json=bool(getattr(args, "json", False)))
        if getattr(args, "apply", False):
            apply_plan(plan)
            print("applied")
        return 0
    except BootstrapError as error:
        print(f"error[{error.code}]: {error.detail}", file=sys.stderr)
        return 1
    except OSError:
        print("error[io_failed]: filesystem operation failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
