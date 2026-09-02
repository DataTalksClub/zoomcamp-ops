#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Conformance checker for DataTalks.Club zoomcamp course repositories.

This is the friendly, early gate for the curriculum conventions written down in
`STRUCTURE.md` and `docs/curriculum-contract.md`. It is NOT the authority: the
website's ingestion parser (`content_sync/course_repository.py` in the website
repo) is, and it fails loudly on push. This checker exists so that failure
almost never happens -- a contributor should hear "your unit has no H1" on the
pull request, minutes after pushing, not from a rejected production import.

Where the two disagree, the parser wins and this script has a bug: report it
against DataTalksClub/zoomcamp-template.

Usage:

    uv run check_zoomcamp.py                 # check the current directory
    uv run check_zoomcamp.py PATH            # check a course repo checkout
    uv run check_zoomcamp.py --phase 3       # enforce the end-state contract
    uv run check_zoomcamp.py --warn-only     # never exit non-zero (adoption)
    uv run check_zoomcamp.py --rules         # print the rule reference and exit

Run it straight from the template repo without cloning (pin the ref):

    uv run https://raw.githubusercontent.com/DataTalksClub/zoomcamp-template/<SHA>/scripts/check-zoomcamp/check_zoomcamp.py .

Exit codes: 0 = no errors, 1 = at least one error, 2 = the checker could not run.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Iterator
from uuid import UUID

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - environment guard
    sys.stderr.write(
        "check-zoomcamp needs PyYAML. Run it with uv so the dependency is handled:\n"
        "  uv run check_zoomcamp.py PATH\n"
    )
    raise SystemExit(2) from None


# --------------------------------------------------------------------------
# Rule catalogue
# --------------------------------------------------------------------------
#
# Rule classes decide how a phase maps to a severity (see PHASE_SEVERITY):
#
#   layout   -- where files live and what they are called. Always an error;
#               these are the rules the whole convention rests on.
#   content  -- unit page shape (U1-U9). Warning during Phase 1 while the
#               repos are still being normalized, error from Phase 2.
#   knob     -- configuration the convention deletes. Warning until Phase 3,
#               when the website parser starts rejecting it outright.
#   advisory -- always a warning; a human decision, never a gate.

LAYOUT = "layout"
CONTENT = "content"
KNOB = "knob"
ADVISORY = "advisory"

ERROR = "error"
WARNING = "warning"

PHASE_SEVERITY: dict[str, dict[int, str]] = {
    LAYOUT: {1: ERROR, 2: ERROR, 3: ERROR},
    CONTENT: {1: WARNING, 2: ERROR, 3: ERROR},
    KNOB: {1: WARNING, 2: WARNING, 3: ERROR},
    ADVISORY: {1: WARNING, 2: WARNING, 3: WARNING},
}

RULES: dict[str, tuple[str, str]] = {
    # id: (class, one-line description)
    "L001": (LAYOUT, "course.yaml must exist at the repository root"),
    "L002": (LAYOUT, "curriculum lives under cohorts/<year>/; no module.yaml elsewhere"),
    "L003": (LAYOUT, "cohort.yaml and homework.yaml sit at their fixed depths"),
    "L004": (LAYOUT, "no numbered module directories at the repository root"),
    "L005": (LAYOUT, "module directory name is NN-kebab-case"),
    "L006": (LAYOUT, "a module directory holds only units, README.md, homework.*, images/, code/"),
    "L007": (LAYOUT, "unit files are NN-kebab.md siblings of module.yaml"),
    "L008": (LAYOUT, "homework.md and homework.yaml are co-located in the module directory"),
    "L009": (LAYOUT, "every module directory has a README.md index"),
    "L010": (LAYOUT, "SITE.md exists at the repository root"),
    "L011": (ADVISORY, "cohorts/README.md explains the layout to contributors"),
    "L012": (CONTENT, "relative links in a module README resolve"),
    "M001": (LAYOUT, "manifest YAML parses, has no duplicate keys and no unknown keys"),
    "M002": (LAYOUT, "every content_id is a canonical UUID and unique in the repository"),
    "M003": (LAYOUT, "schema_version is 1"),
    "M004": (KNOB, "cohort.yaml restates identity the path already carries"),
    "M005": (LAYOUT, "flow entries resolve, stay in the cohort, and pair co-located files"),
    "M006": (LAYOUT, "module.yaml units resolve and agree with the unit files on disk"),
    "M007": (KNOB, "declared slug keys only restate the path"),
    "M008": (KNOB, "homework instructions_path only restates homework.md"),
    "M009": (KNOB, "course description comes from SITE.md"),
    "M010": (ADVISORY, "new-cohort homework slugs are hwNN (existing slugs are frozen)"),
    "M011": (KNOB, "module.yaml declares a units list (derived from Phase 3 on)"),
    "M012": (CONTENT, "a declared unit title agrees with the unit file's H1"),
    "U001": (LAYOUT, "unit frontmatter carries only the allowed keys with valid values"),
    "U002": (CONTENT, "a unit opens with exactly one unnumbered '# Title' H1"),
    "U003": (CONTENT, "a unit body has no second H1"),
    "U004": (CONTENT, "images resolve inside the module directory"),
    "U005": (CONTENT, "relative links resolve and stay inside the cohort"),
    "U006": (CONTENT, "videos live in frontmatter video_url, never in the body"),
    "U008": (CONTENT, "no hand-maintained navigation furniture"),
    "U009": (CONTENT, "homework.md opens with a single H1"),
    "U010": (KNOB, "unit content_id lives in the unit's frontmatter (Phase 3)"),
    "C001": (ADVISORY, ".zoomcamp-check.yaml is well formed"),
    "C002": (ADVISORY, "every declared allowance is still needed"),
}

# U007 (companion files declared in frontmatter `code:`) is authoring guidance
# that no script can verify -- a unit that walks through no files is correct
# with no `code:` key. The checkable half of U007 lives in U001: a declared
# code path must resolve inside the module directory.


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
UNIT_FILENAME = re.compile(r"^(\d{2,})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")
NUMBERED_DIR = re.compile(r"^\d{2,}-")
NUMERIC_TITLE_PREFIX = re.compile(r"^(?:\d+(?:\.\d+)+[.):]?|\d+[.):])\s+")
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
YOUTUBE_IN_TEXT = re.compile(r"https?://(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/\S+")
NAV_HEADING = re.compile(r"^#{1,6}\s+navigation\s*$", re.IGNORECASE)
NAV_LINE = re.compile(
    r"(\[\s*(?:&larr;|<-|←|«)\s*|←\s*prev|prev\s*(?:ious)?\s*(?:lesson|unit)?\s*:"
    r"|next\s*(?:lesson|unit)?\s*:|next\s*(?:&rarr;|->|→|»)|\|\s*\[next)",
    re.IGNORECASE,
)
IGNORED_DIRS = {".git", ".github", ".venv", "venv", "__pycache__", "node_modules", ".tmp"}

MD_LINK = re.compile(r"(!?)\[(?:[^\]\\]|\\.)*\]\(\s*(<[^>]*>|[^()\s]*(?:\([^()]*\)[^()\s]*)*)")
HTML_SRC = re.compile(r"""<(img|a)\b[^>]*?\b(src|href)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")


@dataclass(frozen=True)
class Finding:
    rule: str
    path: str
    line: int
    message: str

    @property
    def rule_class(self) -> str:
        return RULES[self.rule][0]


@dataclass
class Allowance:
    rule: str
    path: str
    reason: str
    used: bool = False


@dataclass
class Repo:
    root: Path
    files: dict[str, Path]  # repo-relative posix path -> absolute path

    def exists(self, rel: str) -> bool:
        return rel in self.files

    def read(self, rel: str) -> str:
        return self.files[rel].read_text(encoding="utf-8")


class DuplicateKeyLoader(yaml.SafeLoader):
    """Mirrors the website parser, which refuses duplicate mapping keys."""


def _no_duplicate_keys(loader: DuplicateKeyLoader, node: yaml.MappingNode) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in mapping:
            raise yaml.MarkedYAMLError(
                context="while constructing a mapping",
                problem=f"duplicate key {key!r}",
                problem_mark=key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=True)
    return mapping


DuplicateKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicate_keys
)


# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------


def iter_prose_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield (1-based line number, line) skipping fenced code blocks."""

    fence: str | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence = match.group(1)[0] * 3
                continue
            yield number, line
        else:
            if match and match.group(1)[0] * 3 == fence:
                fence = None


def split_frontmatter(text: str) -> tuple[str | None, int, str]:
    """Return (frontmatter text or None, first body line number, body text)."""

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, 1, text
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[1:index]), index + 2, "".join(lines[index + 1 :])
    return None, 1, text  # unclosed: reported as U001 by the caller


def first_content_line(body: str, offset: int) -> tuple[int, str] | None:
    """First meaningful line, skipping blanks and leading HTML comments."""

    in_comment = False
    for number, line in iter_prose_lines(body):
        stripped = line.strip()
        if in_comment:
            if "-->" in stripped:
                in_comment = False
            continue
        if not stripped:
            continue
        if stripped.startswith("<!--"):
            if "-->" not in stripped:
                in_comment = True
            continue
        return number + offset - 1, line.rstrip()
    return None


def iter_targets(text: str) -> Iterator[tuple[int, bool, str]]:
    """Yield (line number, is_image, target) for markdown and HTML references."""

    for number, line in iter_prose_lines(text):
        for match in MD_LINK.finditer(line):
            target = match.group(2).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1].strip()
            if target:
                yield number, match.group(1) == "!", target
        for match in HTML_SRC.finditer(line):
            yield number, match.group(1).lower() == "img", match.group(3).strip()


def is_external(target: str) -> bool:
    return bool(re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target)) or target.startswith("//")


# --------------------------------------------------------------------------
# Checker
# --------------------------------------------------------------------------


@dataclass
class Checker:
    repo: Repo
    phase: int
    findings: list[Finding] = field(default_factory=list)
    allowances: list[Allowance] = field(default_factory=list)
    content_ids: dict[str, str] = field(default_factory=dict)
    course_slug: str = ""

    # -- reporting ---------------------------------------------------------

    def report(self, rule: str, path: str, line: int, message: str) -> None:
        for allowance in self.allowances:
            if allowance.rule == rule and allowance.path == path:
                allowance.used = True
                return
        self.findings.append(Finding(rule=rule, path=path, line=line, message=message))

    def severity(self, finding: Finding) -> str:
        return PHASE_SEVERITY[finding.rule_class][self.phase]

    # -- YAML --------------------------------------------------------------

    def load_yaml(self, rel: str) -> dict[str, Any] | None:
        try:
            loaded = yaml.load(self.repo.read(rel), Loader=DuplicateKeyLoader)
        except yaml.YAMLError as error:
            line = getattr(getattr(error, "problem_mark", None), "line", 0) + 1
            self.report("M001", rel, line, f"YAML is invalid: {error.problem or error}")
            return None
        if not isinstance(loaded, dict):
            self.report("M001", rel, 1, "expected a YAML mapping at the top level")
            return None
        return loaded

    def check_keys(
        self, rel: str, mapping: dict[str, Any], allowed: set[str], required: set[str]
    ) -> None:
        for key in sorted(set(mapping) - allowed):
            self.report("M001", rel, 1, f"unknown key {key!r} -- the parser rejects it")
        for key in sorted(required - set(mapping)):
            self.report("M001", rel, 1, f"required key {key!r} is missing")
        if "schema_version" in mapping and mapping["schema_version"] != 1:
            self.report("M003", rel, 1, "schema_version must be the integer 1")

    def check_content_id(self, rel: str, mapping: dict[str, Any], pointer: str = "content_id") -> None:
        value = mapping.get("content_id")
        if value is None:
            return
        if not isinstance(value, str):
            self.report("M002", rel, 1, f"{pointer} must be a UUID string")
            return
        try:
            parsed = UUID(value)
        except ValueError:
            self.report("M002", rel, 1, f"{pointer} {value!r} is not a UUID")
            return
        if str(parsed) != value:
            self.report(
                "M002", rel, 1, f"{pointer} must be the canonical lowercase form {parsed}"
            )
            return
        owner = self.content_ids.get(value)
        if owner is not None and owner != rel:
            self.report(
                "M002",
                rel,
                1,
                f"content_id {value} is already used by {owner}; mint a fresh one (uuidgen)",
            )
            return
        self.content_ids[value] = rel

    # -- entry point -------------------------------------------------------

    def run(self) -> None:
        self.load_config()
        self.check_root()
        cohorts = self.discover_cohorts()
        for cohort in cohorts:
            self.check_cohort(cohort)
        self.check_stray_manifests(cohorts)
        for allowance in self.allowances:
            if not allowance.used:
                self.report(
                    "C002",
                    ".zoomcamp-check.yaml",
                    1,
                    f"allowance {allowance.rule} for {allowance.path} matched nothing -- delete it",
                )

    # -- config ------------------------------------------------------------

    def load_config(self) -> None:
        rel = ".zoomcamp-check.yaml"
        if not self.repo.exists(rel):
            return
        mapping = self.load_yaml(rel)
        if mapping is None:
            return
        for key in sorted(set(mapping) - {"phase", "allow"}):
            self.report("C001", rel, 1, f"unknown key {key!r}")
        for index, raw in enumerate(mapping.get("allow") or []):
            if not isinstance(raw, dict) or set(raw) != {"rule", "path", "reason"}:
                self.report(
                    "C001", rel, 1, f"allow[{index}] needs exactly rule, path and reason"
                )
                continue
            if raw["rule"] not in RULES:
                self.report("C001", rel, 1, f"allow[{index}] names unknown rule {raw['rule']!r}")
                continue
            self.allowances.append(
                Allowance(rule=str(raw["rule"]), path=str(raw["path"]), reason=str(raw["reason"]))
            )

    # -- repository root ---------------------------------------------------

    def check_root(self) -> None:
        if not self.repo.exists("course.yaml"):
            self.report(
                "L001",
                "course.yaml",
                1,
                "no course.yaml at the repository root: the website cannot ingest this repo",
            )
        else:
            self.check_course_manifest()
        if not self.repo.exists("SITE.md"):
            self.report(
                "L010",
                "SITE.md",
                1,
                "no SITE.md: the website course description has no source in this repo",
            )
        if not self.repo.exists("cohorts/README.md"):
            self.report(
                "L011",
                "cohorts/README.md",
                1,
                "no cohorts/README.md telling contributors which cohort is live",
            )
        for entry in sorted(self.repo.root.iterdir()):
            if entry.is_dir() and NUMBERED_DIR.match(entry.name):
                self.report(
                    "L004",
                    entry.name,
                    1,
                    "numbered directory at the repository root: curriculum belongs under "
                    "cohorts/<year>/, non-curriculum material under archive/ or research/",
                )

    def check_course_manifest(self) -> None:
        rel = "course.yaml"
        mapping = self.load_yaml(rel)
        if mapping is None:
            return
        self.check_keys(
            rel,
            mapping,
            allowed={
                "schema_version",
                "content_id",
                "slug",
                "title",
                "description",
                "description_path",
                "outcome",
                "repository_url",
                "docs_url",
                "faq_url",
                "hashtag",
                "published",
            },
            required={
                "schema_version",
                "content_id",
                "slug",
                "title",
                "outcome",
                "repository_url",
                "docs_url",
                "faq_url",
                "hashtag",
                "published",
            },
        )
        self.check_content_id(rel, mapping)
        slug = mapping.get("slug")
        if isinstance(slug, str):
            self.course_slug = slug
            if SLUG.fullmatch(slug) is None:
                self.report("M001", rel, 1, f"slug {slug!r} is not kebab-case")
        if "description" in mapping:
            self.report(
                "M009",
                rel,
                1,
                "inline description: move the text to SITE.md and delete the key",
            )
        path_value = mapping.get("description_path")
        if isinstance(path_value, str) and path_value != "SITE.md":
            self.report(
                "M009",
                rel,
                1,
                f"description_path points at {path_value!r}; the convention is the fixed name SITE.md",
            )
        elif path_value == "SITE.md":
            self.report(
                "M009",
                rel,
                1,
                "description_path is retired: SITE.md is read by fixed name from Phase 3 on",
            )

    # -- cohorts -----------------------------------------------------------

    def discover_cohorts(self) -> list[str]:
        cohorts_dir = self.repo.root / "cohorts"
        if not cohorts_dir.is_dir():
            return []
        found = []
        for entry in sorted(cohorts_dir.iterdir()):
            if entry.is_dir() and self.repo.exists(f"cohorts/{entry.name}/cohort.yaml"):
                found.append(entry.name)
        return found

    def check_cohort(self, cohort: str) -> None:
        rel = f"cohorts/{cohort}/cohort.yaml"
        mapping = self.load_yaml(rel)
        if mapping is None:
            return
        self.check_keys(
            rel,
            mapping,
            allowed={
                "schema_version",
                "content_id",
                "course",
                "identifier",
                "legacy_slug",
                "year",
                "title",
                "description",
                "format",
                "published",
                "start_date",
                "end_date",
                "flow",
            },
            required={
                "schema_version",
                "content_id",
                "course",
                "identifier",
                "legacy_slug",
                "year",
                "title",
                "description",
                "format",
                "published",
                "start_date",
                "end_date",
            },
        )
        self.check_content_id(rel, mapping)
        if str(mapping.get("identifier", cohort)) != cohort:
            self.report(
                "M001",
                rel,
                1,
                f"identifier {mapping.get('identifier')!r} disagrees with the directory {cohort!r}"
                " -- the directory wins",
            )
        if self.course_slug and mapping.get("course") not in (None, self.course_slug):
            self.report(
                "M001",
                rel,
                1,
                f"course {mapping.get('course')!r} disagrees with course.yaml slug {self.course_slug!r}",
            )
        derivable = [
            key
            for key in ("course", "identifier", "year", "legacy_slug", "title", "description")
            if key in mapping
        ]
        if derivable:
            self.report(
                "M004",
                rel,
                1,
                f"{', '.join(derivable)} restate identity the path already carries; retired knobs "
                "(the deployed parser still requires them, so delete them only at Phase 3)",
            )

        if mapping.get("format") == "legacy":
            return

        modules = self.discover_modules(cohort)
        for module in modules:
            self.check_module(cohort, module)
        self.check_flow(rel, mapping, cohort, modules)
        self.check_cohort_extras(cohort, modules)

    def discover_modules(self, cohort: str) -> list[str]:
        base = self.repo.root / "cohorts" / cohort
        return sorted(
            entry.name
            for entry in base.iterdir()
            if entry.is_dir() and self.repo.exists(f"cohorts/{cohort}/{entry.name}/module.yaml")
        )

    def check_cohort_extras(self, cohort: str, modules: list[str]) -> None:
        base = self.repo.root / "cohorts" / cohort
        for entry in sorted(base.iterdir()):
            if not entry.is_dir() or entry.name in modules or entry.name in IGNORED_DIRS:
                continue
            if NUMBERED_DIR.match(entry.name):
                self.report(
                    "L005",
                    f"cohorts/{cohort}/{entry.name}",
                    1,
                    "numbered directory without a module.yaml: either add the manifest or "
                    "give the directory a non-numbered name",
                )

    def check_flow(
        self, rel: str, mapping: dict[str, Any], cohort: str, modules: list[str]
    ) -> None:
        flow = mapping.get("flow")
        if flow is None:
            return
        if not isinstance(flow, list):
            self.report("M005", rel, 1, "flow must be a list")
            return
        referenced: list[str] = []
        for index, item in enumerate(flow):
            if not isinstance(item, dict) or set(item) - {"module", "project"}:
                self.report("M005", rel, 1, f"flow[{index}] must be a module or project entry")
                continue
            if "project" in item:
                continue
            ref = item.get("module")
            if not isinstance(ref, dict) or set(ref) != {"source", "homework"}:
                self.report(
                    "M005", rel, 1, f"flow[{index}].module needs exactly source and homework"
                )
                continue
            source, homework = str(ref["source"]), str(ref["homework"])
            for label, value in (("source", source), ("homework", homework)):
                if not self.repo.exists(value):
                    self.report("M005", rel, 1, f"flow[{index}].module.{label} {value} not found")
            source_dir = posixpath.dirname(source)
            homework_dir = posixpath.dirname(homework)
            if source_dir != homework_dir:
                self.report(
                    "M005",
                    rel,
                    1,
                    f"flow[{index}] pairs module {source_dir} with homework {homework_dir}: "
                    "one module, one homework, side by side",
                )
            parts = PurePosixPath(source).parts
            if parts[:2] != ("cohorts", cohort):
                self.report(
                    "M005",
                    rel,
                    1,
                    f"flow[{index}].module.source {source} is outside cohorts/{cohort}/",
                )
            else:
                referenced.append(parts[2])
        for module in modules:
            if module not in referenced:
                self.report(
                    "M005",
                    rel,
                    1,
                    f"module {module} has a module.yaml but no flow entry: it will not be imported",
                )
        expected = sorted(referenced)
        if referenced and referenced != expected:
            self.report(
                "M005",
                rel,
                1,
                "flow order disagrees with the directory prefixes; ordering comes from the "
                "NN- prefix, so declare the modules in prefix order",
            )
        if self.phase >= 3 and flow and all("module" in item for item in flow if isinstance(item, dict)):
            self.report(
                "M004",
                rel,
                1,
                "flow only restates the module directories -- delete it and let it be derived",
            )

    # -- modules -----------------------------------------------------------

    def check_module(self, cohort: str, module: str) -> None:
        base = f"cohorts/{cohort}/{module}"
        rel = f"{base}/module.yaml"
        if SLUG.fullmatch(module) is None or not NUMBERED_DIR.match(module):
            self.report(
                "L005",
                base,
                1,
                f"module directory {module!r} must be NN-kebab-case (for example 01-intro)",
            )
        mapping = self.load_yaml(rel)
        if mapping is None:
            return
        self.check_keys(
            rel,
            mapping,
            allowed={"schema_version", "content_id", "slug", "title", "units"},
            required={"schema_version", "content_id", "title"},
        )
        self.check_content_id(rel, mapping)
        if "slug" in mapping:
            self.report(
                "M007",
                rel,
                1,
                "module slug only restates the directory name -- delete it",
            )
            if mapping["slug"] != module:
                self.report(
                    "M001",
                    rel,
                    1,
                    f"slug {mapping['slug']!r} disagrees with the directory {module!r}",
                )

        on_disk = self.module_unit_files(cohort, module)
        declared = self.check_declared_units(rel, mapping, cohort, module)
        units = declared if declared is not None else on_disk
        self.check_module_contents(cohort, module, set(units))
        for unit in units:
            self.check_unit(cohort, module, unit)
        if self.repo.exists(f"{base}/homework.md"):
            self.check_homework_page(cohort, module)
        if not self.repo.exists(f"{base}/README.md"):
            self.report(
                "L009",
                f"{base}/README.md",
                1,
                "no module README: GitHub readers need an index page for the module",
            )
        else:
            self.check_module_readme(cohort, module)
        has_yaml = self.repo.exists(f"{base}/homework.yaml")
        has_md = self.repo.exists(f"{base}/homework.md")
        if has_yaml != has_md:
            missing = "homework.md" if has_yaml else "homework.yaml"
            self.report(
                "L008", base, 1, f"{missing} is missing: homework is one pair of co-located files"
            )
        if has_yaml:
            self.check_homework_manifest(cohort, module)

    def module_unit_files(self, cohort: str, module: str) -> list[str]:
        base = self.repo.root / "cohorts" / cohort / module
        names = sorted(
            entry.name
            for entry in base.iterdir()
            if entry.is_file()
            and entry.suffix == ".md"
            and entry.name not in {"README.md", "homework.md"}
        )
        return names

    def check_declared_units(
        self, rel: str, mapping: dict[str, Any], cohort: str, module: str
    ) -> list[str] | None:
        base = f"cohorts/{cohort}/{module}"
        units = mapping.get("units")
        if units is None:
            if self.phase < 3:
                self.report(
                    "M001",
                    rel,
                    1,
                    "units is required by the deployed parser until Phase 3 lands",
                )
            return None
        self.report(
            "M011",
            rel,
            1,
            "units only restates the NN-*.md files on disk -- derived from Phase 3 on",
        )
        if not isinstance(units, list) or not units:
            self.report("M006", rel, 1, "units must be a non-empty list")
            return None
        names: list[str] = []
        prefixes: dict[str, str] = {}
        for index, unit in enumerate(units):
            if not isinstance(unit, dict):
                self.report("M006", rel, 1, f"units[{index}] must be a mapping")
                continue
            for key in sorted(set(unit) - {"content_id", "slug", "title", "path"}):
                self.report("M001", rel, 1, f"units[{index}] has unknown key {key!r}")
            for key in sorted({"content_id", "title", "path"} - set(unit)):
                self.report("M001", rel, 1, f"units[{index}] is missing {key!r}")
            self.check_content_id(rel, unit, pointer=f"units[{index}].content_id")
            if "slug" in unit:
                self.report(
                    "M007", rel, 1, f"units[{index}].slug only restates the filename -- delete it"
                )
            raw_path = unit.get("path")
            if not isinstance(raw_path, str):
                continue
            if not self.repo.exists(f"{base}/{raw_path}"):
                self.report("M006", rel, 1, f"units[{index}].path {raw_path} does not exist")
                continue
            if "/" in raw_path:
                self.report(
                    "L007",
                    f"{base}/{raw_path}",
                    1,
                    f"unit lives in a subdirectory ({raw_path}); units are siblings of module.yaml",
                )
            name = posixpath.basename(raw_path)
            names.append(raw_path)
            declared_title = unit.get("title")
            if isinstance(declared_title, str):
                self.compare_title(f"{base}/{raw_path}", declared_title, rel, index)
            match = UNIT_FILENAME.match(name)
            if match is None:
                self.report(
                    "L007",
                    f"{base}/{raw_path}",
                    1,
                    f"unit filename {name!r} must be NN-kebab.md; the stem is the published URL "
                    "slug, so rename only while the cohort is unpublished",
                )
            else:
                prefix = match.group(1)
                if prefix in prefixes:
                    self.report(
                        "L007",
                        f"{base}/{raw_path}",
                        1,
                        f"prefix {prefix} is already used by {prefixes[prefix]}; ordering comes "
                        "from the prefix so it must be unique",
                    )
                else:
                    prefixes[prefix] = name
        on_disk = set(self.module_unit_files(cohort, module))
        for orphan in sorted(on_disk - {posixpath.basename(n) for n in names}):
            self.report(
                "M006",
                f"{base}/{orphan}",
                1,
                "markdown file beside module.yaml is not listed in units and will not be "
                "imported: list it, rename it, or move it out of the module directory",
            )
        return names

    def compare_title(self, unit_rel: str, declared: str, manifest_rel: str, index: int) -> None:
        if not self.repo.exists(unit_rel):
            return
        _, offset, body = split_frontmatter(self.repo.read(unit_rel))
        first = first_content_line(body, offset)
        if first is None or not first[1].startswith("# "):
            return
        heading = first[1][2:].strip()
        normalized_heading = NUMERIC_TITLE_PREFIX.sub("", heading).strip()
        normalized_declared = NUMERIC_TITLE_PREFIX.sub("", declared).strip()
        if normalized_heading.casefold() != normalized_declared.casefold():
            self.report(
                "M012",
                unit_rel,
                first[0],
                f"H1 {heading!r} disagrees with units[{index}].title {declared!r} in "
                f"{manifest_rel}; the H1 is the title, so fix the YAML",
            )

    def check_module_contents(self, cohort: str, module: str, units: set[str]) -> None:
        base = self.repo.root / "cohorts" / cohort / module
        rel_base = f"cohorts/{cohort}/{module}"
        unit_names = {posixpath.basename(unit) for unit in units}
        for entry in sorted(base.iterdir()):
            if entry.name in IGNORED_DIRS:
                continue
            if entry.is_dir():
                if entry.name == "lessons":
                    self.report(
                        "L007",
                        f"{rel_base}/lessons",
                        1,
                        "units live beside module.yaml, not in a lessons/ subdirectory: "
                        "flattening keeps image references as images/... with no ../",
                    )
                continue
            if entry.suffix != ".md":
                continue
            if entry.name in {"README.md", "homework.md"} or entry.name in unit_names:
                continue
            self.report(
                "L006",
                f"{rel_base}/{entry.name}",
                1,
                "a module directory holds only unit files, README.md and homework.md at "
                "top level; move supporting documents into code/ or link them from a unit",
            )

    # -- homework ----------------------------------------------------------

    def check_homework_manifest(self, cohort: str, module: str) -> None:
        rel = f"cohorts/{cohort}/{module}/homework.yaml"
        mapping = self.load_yaml(rel)
        if mapping is None:
            return
        self.check_keys(
            rel,
            mapping,
            allowed={
                "schema_version",
                "content_id",
                "slug",
                "title",
                "instructions_path",
                "due_at",
                "initial_state",
                "form",
                "questions",
            },
            required={
                "schema_version",
                "content_id",
                "slug",
                "title",
                "due_at",
                "initial_state",
                "form",
                "questions",
            },
        )
        self.check_content_id(rel, mapping)
        for index, question in enumerate(mapping.get("questions") or []):
            if isinstance(question, dict):
                self.check_content_id(rel, question, pointer=f"questions[{index}].content_id")
        instructions = mapping.get("instructions_path")
        if instructions is not None:
            if instructions != "homework.md":
                self.report(
                    "M008",
                    rel,
                    1,
                    f"instructions_path {instructions!r} must be the co-located homework.md",
                )
            else:
                self.report(
                    "M008",
                    rel,
                    1,
                    "instructions_path is retired: homework.md is read by fixed name",
                )
        slug = mapping.get("slug")
        match = UNIT_FILENAME.match(f"{module}.md") or re.match(r"^(\d{2,})-", module)
        if isinstance(slug, str) and match:
            expected = f"hw{match.group(1)}"
            if slug != expected:
                self.report(
                    "M010",
                    rel,
                    1,
                    f"homework slug {slug!r} is not the derived {expected!r}. Published slugs are "
                    "frozen -- keep this one and use the derived form for new cohorts",
                )

    def check_homework_page(self, cohort: str, module: str) -> None:
        rel = f"cohorts/{cohort}/{module}/homework.md"
        text = self.repo.read(rel)
        _, offset, body = split_frontmatter(text)
        first = first_content_line(body, offset)
        if first is None:
            self.report("U009", rel, 1, "homework.md is empty")
            return
        if not first[1].startswith("# ") or first[1].startswith("##"):
            self.report(
                "U009",
                rel,
                first[0],
                f"homework.md must open with a single '# Title' H1, found {first[1][:60]!r}",
            )
        self.check_references(rel, cohort, module, text, kind="homework")

    # -- units -------------------------------------------------------------

    def check_unit(self, cohort: str, module: str, unit: str) -> None:
        rel = f"cohorts/{cohort}/{module}/{unit}"
        if not self.repo.exists(rel):
            return
        text = self.repo.read(rel)
        frontmatter, offset, body = split_frontmatter(text)
        if text.startswith("---") and frontmatter is None:
            self.report("U001", rel, 1, "frontmatter opens with --- but is never closed")
        if frontmatter is not None:
            self.check_frontmatter(rel, cohort, module, frontmatter)
        elif self.phase >= 3:
            self.report("U010", rel, 1, "no frontmatter: a unit must declare its content_id")

        first = first_content_line(body, offset)
        if first is None:
            self.report("U002", rel, 1, "unit file has no content")
            return
        line_number, line = first
        if not line.startswith("# ") or line.startswith("## "):
            self.report(
                "U002",
                rel,
                line_number,
                f"a unit must open with exactly one '# Title' H1, found {line[:60]!r}",
            )
        else:
            title = line[2:].strip()
            if NUMERIC_TITLE_PREFIX.match(title):
                self.report(
                    "U002",
                    rel,
                    line_number,
                    f"title {title!r} carries its own numbering; numbering comes from the "
                    f"{unit.split('-')[0]}- filename prefix and the site renders it",
                )
        for number, text_line in iter_prose_lines(body):
            absolute = number + offset - 1
            if absolute == line_number:
                continue
            if text_line.startswith("# "):
                self.report(
                    "U003",
                    rel,
                    absolute,
                    "second H1 in the body: sections are ##, the H1 is the unit title",
                )
        self.check_navigation(rel, body, offset)
        self.check_video_in_body(rel, body, offset)
        self.check_references(rel, cohort, module, text, kind="unit")

    def check_frontmatter(self, rel: str, cohort: str, module: str, frontmatter: str) -> None:
        try:
            mapping = yaml.load(frontmatter, Loader=DuplicateKeyLoader) or {}
        except yaml.YAMLError as error:
            self.report("U001", rel, 2, f"frontmatter YAML is invalid: {error}")
            return
        if not isinstance(mapping, dict):
            self.report("U001", rel, 2, "frontmatter must be a YAML mapping")
            return
        allowed = {"video_url", "code"}
        if self.phase >= 3:
            allowed.add("content_id")
        for key in sorted(set(mapping) - allowed):
            if key == "content_id":
                self.report(
                    "U010",
                    rel,
                    2,
                    "content_id in frontmatter is rejected by the deployed parser until "
                    "Phase 3 lands; keep it in module.yaml for now",
                )
            else:
                self.report("U001", rel, 2, f"frontmatter key {key!r} is not allowed")
        if self.phase >= 3:
            self.check_content_id(rel, mapping)
            if "content_id" not in mapping:
                self.report("U010", rel, 2, "frontmatter must declare the unit's content_id")
        video = mapping.get("video_url")
        if video is not None:
            if not isinstance(video, str) or not video.startswith("https://"):
                self.report("U001", rel, 2, "video_url must be an https URL")
            else:
                host = re.sub(r"^https://([^/]+).*$", r"\1", video).casefold()
                if host not in YOUTUBE_HOSTS:
                    self.report("U001", rel, 2, f"video_url host {host!r} is not YouTube")
        code = mapping.get("code")
        if code is not None:
            if not isinstance(code, list):
                self.report("U001", rel, 2, "code must be a list of {label, path} entries")
                return
            for index, entry in enumerate(code):
                if not isinstance(entry, dict) or set(entry) != {"label", "path"}:
                    self.report("U001", rel, 2, f"code[{index}] needs exactly label and path")
                    continue
                target = str(entry["path"])
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(rel), target))
                if not self.repo.exists(resolved):
                    self.report("U001", rel, 2, f"code[{index}].path {target} does not exist")
                elif not resolved.startswith(f"cohorts/{cohort}/{module}/"):
                    self.report(
                        "U001",
                        rel,
                        2,
                        f"code[{index}].path {target} leaves the module directory",
                    )

    def check_navigation(self, rel: str, body: str, offset: int) -> None:
        for number, line in iter_prose_lines(body):
            stripped = line.strip()
            if not stripped:
                continue
            if NAV_HEADING.match(stripped) or (NAV_LINE.search(stripped) and "](" in stripped):
                self.report(
                    "U008",
                    rel,
                    number + offset - 1,
                    "hand-maintained navigation: the site renders prev/next from the unit "
                    "order and GitHub readers use the module README index",
                )
                return

    def check_video_in_body(self, rel: str, body: str, offset: int) -> None:
        for number, line in iter_prose_lines(body):
            if YOUTUBE_IN_TEXT.search(line):
                self.report(
                    "U006",
                    rel,
                    number + offset - 1,
                    "video link in the body: move it to frontmatter video_url so the site "
                    "renders a player and GitHub still shows it in the frontmatter table",
                )
                return

    def check_references(self, rel: str, cohort: str, module: str, text: str, kind: str) -> None:
        module_dir = f"cohorts/{cohort}/{module}"
        cohort_dir = f"cohorts/{cohort}"
        here = posixpath.dirname(rel)
        for line, is_image, raw in iter_targets(text):
            target = raw.split("#", 1)[0].split("?", 1)[0].strip()
            if not target or is_external(raw):
                continue
            rule = "U004" if is_image else "U005"
            if "%2f" in target.casefold():
                self.report(
                    rule,
                    rel,
                    line,
                    f"URL-encoded path separator in {target!r}: write it as images/name.png",
                )
                continue
            resolved = posixpath.normpath(posixpath.join(here, target))
            if resolved.startswith(".."):
                self.report(rule, rel, line, f"{target!r} escapes the repository")
                continue
            if is_image and not resolved.startswith(f"{module_dir}/"):
                self.report(
                    "U004",
                    rel,
                    line,
                    f"image {target!r} lives outside the module directory; every image a "
                    f"unit uses belongs in {module_dir}/images/",
                )
                continue
            if not is_image and not resolved.startswith(f"{cohort_dir}/"):
                self.report(
                    "U005",
                    rel,
                    line,
                    f"link {target!r} leaves cohorts/{cohort}/; write targets outside the "
                    "cohort as absolute GitHub URLs",
                )
                continue
            if not is_image and not resolved.startswith(f"{module_dir}/"):
                depth = len(PurePosixPath(resolved).parts) - len(PurePosixPath(cohort_dir).parts)
                if depth < 2:
                    self.report(
                        "U005",
                        rel,
                        line,
                        f"link {target!r} points at the cohort directory itself; link a "
                        "sibling module's unit instead",
                    )
                    continue
            if not self.repo.exists(resolved) and not (self.repo.root / resolved).is_dir():
                self.report(rule, rel, line, f"{target!r} does not exist ({resolved})")

    def check_module_readme(self, cohort: str, module: str) -> None:
        rel = f"cohorts/{cohort}/{module}/README.md"
        module_dir = f"cohorts/{cohort}/{module}"
        here = module_dir
        for line, is_image, raw in iter_targets(self.repo.read(rel)):
            target = raw.split("#", 1)[0].split("?", 1)[0].strip()
            if not target or is_external(raw):
                continue
            resolved = posixpath.normpath(posixpath.join(here, target))
            if resolved.startswith(".."):
                self.report(
                    "L012", rel, line, f"link {target!r} escapes the repository"
                )
                continue
            if not self.repo.exists(resolved) and not (self.repo.root / resolved).is_dir():
                self.report("L012", rel, line, f"{target!r} does not exist ({resolved})")

    # -- stray manifests ---------------------------------------------------

    def check_stray_manifests(self, cohorts: list[str]) -> None:
        for rel in sorted(self.repo.files):
            parts = PurePosixPath(rel).parts
            name = parts[-1]
            if name == "module.yaml":
                if not (len(parts) == 4 and parts[0] == "cohorts"):
                    self.report(
                        "L002",
                        rel,
                        1,
                        "module.yaml must live at cohorts/<year>/<NN-module>/module.yaml; "
                        "curriculum at the repository root is the abolished layout",
                    )
            elif name == "cohort.yaml" and not (len(parts) == 3 and parts[0] == "cohorts"):
                self.report("L003", rel, 1, "cohort.yaml must live at cohorts/<year>/cohort.yaml")
            elif name == "homework.yaml" and not (len(parts) == 4 and parts[0] == "cohorts"):
                self.report(
                    "L003",
                    rel,
                    1,
                    "homework.yaml must live beside its module at "
                    "cohorts/<year>/<NN-module>/homework.yaml",
                )
            elif name == "course.yaml" and len(parts) != 1:
                self.report("L003", rel, 1, "course.yaml must live at the repository root")


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------


def collect_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    stack = [root]
    while stack:
        current = stack.pop()
        for entry in current.iterdir():
            if entry.name in IGNORED_DIRS:
                continue
            if entry.is_symlink():
                continue
            if entry.is_dir():
                stack.append(entry)
            elif entry.is_file():
                files[entry.relative_to(root).as_posix()] = entry
    return files


def render(findings: Iterable[Finding], checker: Checker, style: str) -> str:
    lines = []
    for finding in sorted(findings, key=lambda item: (item.path, item.line, item.rule)):
        severity = checker.severity(finding)
        if style == "github":
            lines.append(
                f"::{severity} file={finding.path},line={finding.line},"
                f"title={finding.rule}::{finding.message}"
            )
        else:
            lines.append(
                f"{severity.upper():7} {finding.rule}  {finding.path}:{finding.line}\n"
                f"        {finding.message}"
            )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="check-zoomcamp",
        description="Check a zoomcamp course repository against the curriculum conventions.",
    )
    parser.add_argument("path", nargs="?", default=".", help="course repository checkout")
    parser.add_argument(
        "--phase",
        type=int,
        choices=(1, 2, 3),
        default=None,
        help="migration phase: 1 layout, 2 unit shape, 3 derived contract (default 1, "
        "or the phase declared in .zoomcamp-check.yaml)",
    )
    parser.add_argument("--format", choices=("text", "github"), default="text")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    parser.add_argument(
        "--warn-only", action="store_true", help="always exit 0 (adoption window)"
    )
    parser.add_argument("--rules", action="store_true", help="print the rule reference and exit")
    args = parser.parse_args(argv)

    if args.rules:
        for rule, (rule_class, description) in sorted(RULES.items()):
            print(f"{rule}  [{rule_class:8}] {description}")
        return 0

    root = Path(args.path).resolve()
    if not root.is_dir():
        sys.stderr.write(f"not a directory: {root}\n")
        return 2

    files = collect_files(root)
    repo = Repo(root=root, files=files)

    phase = args.phase
    if phase is None:
        phase = 1
        config = root / ".zoomcamp-check.yaml"
        if config.is_file():
            try:
                declared = (yaml.safe_load(config.read_text(encoding="utf-8")) or {}).get("phase")
            except yaml.YAMLError:
                declared = None
            if declared in (1, 2, 3):
                phase = int(declared)

    checker = Checker(repo=repo, phase=phase)
    checker.run()

    errors = [f for f in checker.findings if checker.severity(f) == ERROR]
    warnings = [f for f in checker.findings if checker.severity(f) == WARNING]

    if args.json:
        print(
            json.dumps(
                {
                    "path": str(root),
                    "phase": phase,
                    "errors": len(errors),
                    "warnings": len(warnings),
                    "findings": [
                        {
                            "rule": f.rule,
                            "severity": checker.severity(f),
                            "path": f.path,
                            "line": f.line,
                            "message": f.message,
                        }
                        for f in sorted(checker.findings, key=lambda i: (i.path, i.line, i.rule))
                    ],
                },
                indent=2,
            )
        )
    else:
        output = render(checker.findings, checker, args.format)
        if output:
            print(output)
        print(
            f"\ncheck-zoomcamp: phase {phase}, {len(errors)} error(s), "
            f"{len(warnings)} warning(s) in {root}"
        )
        if checker.findings:
            print("Rules: STRUCTURE.md and docs/curriculum-contract.md in DataTalksClub/zoomcamp-template")

    if args.warn_only:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
