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
against DataTalksClub/zoomcamp-ops.

Usage:

    uv run check_zoomcamp.py                 # check the current directory
    uv run check_zoomcamp.py PATH            # check a course repo checkout
    uv run check_zoomcamp.py --phase 3       # enforce the end-state contract
    uv run check_zoomcamp.py --warn-only     # never exit non-zero (adoption)
    uv run check_zoomcamp.py --rules         # print the rule reference and exit

Run it straight from the template repo without cloning (pin the ref):

    uv run https://raw.githubusercontent.com/DataTalksClub/zoomcamp-ops/<SHA>/scripts/check-zoomcamp/check_zoomcamp.py .

Exit codes: 0 = no errors, 1 = at least one error, 2 = the checker could not run.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from dataclasses import dataclass, field
from datetime import date
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
#   content  -- unit page shape that is safe to fix TODAY, against the
#               currently deployed site. Warning during Phase 1 while the
#               repos are still being normalized, error from Phase 2.
#   knob     -- configuration the convention deletes. Warning until Phase 3,
#               when the website parser starts rejecting it outright.
#   pending  -- the convention's end state, blocked on a website change that
#               has NOT shipped. Acting on one of these today makes a
#               published page worse, so it is never an error at any phase and
#               its message must say what has to ship first. See the note
#               below -- this class exists because the checker got it wrong
#               once and would have told three repos to break themselves.
#               A rule leaves this class only when the thing it waits for
#               actually lands. U011 left it: what it waited on turned out to
#               be an owner decision, and the decision was made. U006 and U009
#               have NOT: the importer still drops frontmatter video_url, and
#               the homework page still renders the declared title as its own
#               h1 with no strip for a leading heading. Moving either out of
#               `pending` re-creates the bug this class was invented for.
#   advisory -- always a warning; a human decision, never a gate.

LAYOUT = "layout"
CONTENT = "content"
KNOB = "knob"
PENDING = "pending"
ADVISORY = "advisory"

ERROR = "error"
WARNING = "warning"

PHASE_SEVERITY: dict[str, dict[int, str]] = {
    LAYOUT: {1: ERROR, 2: ERROR, 3: ERROR},
    CONTENT: {1: WARNING, 2: ERROR, 3: ERROR},
    KNOB: {1: WARNING, 2: WARNING, 3: ERROR},
    PENDING: {1: WARNING, 2: WARNING, 3: WARNING},
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
    "M012": (CONTENT, "a declared unit title matches the unit file's H1 exactly"),
    "U001": (LAYOUT, "unit frontmatter carries only the allowed keys with valid values"),
    "U002": (CONTENT, "a unit opens with exactly one '# Title' H1"),
    "U003": (CONTENT, "a unit body has no second H1"),
    "U004": (CONTENT, "images resolve inside the module directory"),
    "U005": (CONTENT, "relative links resolve and stay inside the cohort"),
    "U006": (PENDING, "videos move to frontmatter video_url when the site can render it"),
    "U008": (CONTENT, "no hand-maintained navigation furniture"),
    "U009": (PENDING, "homework.md opens with a single H1 (needs the homework-page strip)"),
    "U010": (KNOB, "unit content_id lives in the unit's frontmatter (Phase 3)"),
    "U011": (CONTENT, "a unit title carries no 'N.M ' ordinal; order comes from the filename"),
    "C001": (ADVISORY, ".zoomcamp-check.yaml is well formed"),
    "C002": (ADVISORY, "every declared allowance is still needed"),
}

# The v2 catalogue is intentionally separate from RULES.  The v1 self-test
# asserts the exact historical catalogue and its phase classes; adding the
# shared-curriculum rules there would make a v1 fixture appear to have changed
# even though the v1 checker is untouched.  Finding.rule_class and allowance
# validation consult both catalogues.  Keep these IDs stable: they are part of
# the machine-readable CI output and are referenced by course repositories.
V2_RULES: dict[str, tuple[str, str]] = {
    "v2_schema": (LAYOUT, "v2 YAML has bounded types, required fields and no duplicate keys"),
    "v2_mixed_version": (LAYOUT, "a v2 source cannot mix v1 cohort/module manifests"),
    "v2_path_unsafe": (LAYOUT, "v2 paths stay relative, contained and free of symlinks"),
    "current_module_missing": (LAYOUT, "a current curriculum must have discovered root modules"),
    "module_path_not_root": (LAYOUT, "module.yaml files are direct root NN-kebab/module.yaml paths"),
    "archive_module_reference": (LAYOUT, "archive descendants never become current module references"),
    "archive_manifest_ignored": (ADVISORY, "historical archive module manifests are opaque to website import"),
    "invalid_curriculum_kind": (LAYOUT, "curriculum is current or github_archive"),
    "invalid_delivery": (LAYOUT, "delivery is live or self-paced"),
    "self_paced_homework_rejected": (
        LAYOUT,
        "self-paced phase one requires an explicit homework: []",
    ),
    "curriculum_source_mismatch": (LAYOUT, "cohort curriculum uses the shared root graph"),
    "homework_mapping_missing": (LAYOUT, "mapped homework has a module, source and existing pair"),
    "homework_path_outside_cohort": (LAYOUT, "homework source is contained by its declaring cohort"),
    "homework_unreferenced": (LAYOUT, "current homework is reachable only through an explicit mapping"),
    "archive_notice_missing": (LAYOUT, "github archives have a checked-in notice README"),
    "archive_url_invalid": (LAYOUT, "archive notice paths are safe repository-relative paths"),
    "numbered_module_required": (LAYOUT, "root curriculum directories are numbered and have module.yaml"),
    "numbered_lesson_required": (LAYOUT, "root module lessons are numbered Markdown siblings"),
    "duplicate_number_prefix": (LAYOUT, "module and lesson numeric prefixes are unique"),
    "content_id_duplicate": (LAYOUT, "registered v2 content IDs are canonical and unique"),
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
        catalogue = RULES if self.rule in RULES else V2_RULES
        return catalogue[self.rule][0]


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


def _collapse(value: str) -> str:
    """Whitespace-and-case normalization, matching the site's title comparison."""

    return re.sub(r"\s+", " ", value).strip().casefold()


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
    body_videos: dict[str, list[str]] = field(default_factory=dict)

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
        for key in sorted(set(mapping) - allowed, key=repr):
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
            if raw["rule"] not in RULES and raw["rule"] not in V2_RULES:
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
        self.report_pending(cohort)

    def report_pending(self, cohort: str) -> None:
        """One finding per cohort for the bulk item that is NOT yet safe.

        `U006` describes the convention's end state and needs a website change
        that has not shipped. Reported once, with a count and an example,
        because a hundred identical warnings about one blocked migration is how
        a checker teaches people to ignore it. `U011` used to be reported here
        too; the owner settled the ordinal question, so it is now an ordinary
        per-file content rule with an actionable fix (see check_unit).
        """

        videos = self.body_videos.get(cohort, [])
        if videos:
            self.report(
                "U006",
                f"cohorts/{cohort}",
                1,
                f"{len(videos)} units carry the video in the body (e.g. {videos[0]}). The "
                "convention moves it to frontmatter video_url -- but not yet: the deployed "
                "importer parses that key and then drops it, there is no column to store it "
                "and no player fed by it, and the live page renders the video from a body "
                "'video: [Label](url)' line. Moving these today deletes the video from the "
                "published page. This becomes actionable when frontmatter video is "
                "persisted and rendered.",
            )

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
            if re.match(r"^\d{2,}", entry.name):
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
        # Mirrors the deployed view's _same_title: whitespace and case only.
        # Deliberately NOT ordinal-insensitive -- the page strips the leading H1
        # only on an exact match, so an H1 whose ordinal was stripped while the
        # declared title kept its own is the state that prints the title twice.
        # This is the half-migrated state U011's fix can create, and catching it
        # is the whole reason both sides must move in one commit.
        if _collapse(heading) == _collapse(declared):
            return
        if NUMERIC_TITLE_PREFIX.sub("", heading).strip().casefold() == (
            NUMERIC_TITLE_PREFIX.sub("", declared).strip().casefold()
        ):
            self.report(
                "M012",
                unit_rel,
                first[0],
                f"H1 {heading!r} and units[{index}].title {declared!r} in {manifest_rel} "
                "differ only in their 'N.M ' ordinal prefix: one side dropped the ordinal "
                "and the other kept it. The published page removes the leading H1 only on "
                "an exact match, so this renders the title twice. Finish the edit in one "
                "commit -- the ordinal comes off both sides (U011).",
            )
            return
        self.report(
            "M012",
            unit_rel,
            first[0],
            f"H1 {heading!r} disagrees with units[{index}].title {declared!r} in "
            f"{manifest_rel}; the H1 is the title, so fix the YAML. While they differ the "
            "published page prints the title twice.",
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
                f"homework.md opens with {first[1][:50]!r}; the convention is a single "
                "'# Title' H1 equal to the homework's title. Not yet, though: the homework "
                "page already renders the declared title as its h1 and has no strip for a "
                "leading heading in the instructions, so an H1 equal to the title would "
                "print it twice. Leave this until the homework page gains the strip the "
                "unit page has.",
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
                # The un-migrated unit. A unit whose H1 is already clean while
                # the declared title still carries the ordinal is the
                # half-migrated state, and that one is M012's (compare_title).
                match = UNIT_FILENAME.match(posixpath.basename(unit))
                where = (
                    f"the filename prefix ({match.group(1)})" if match else "the filename prefix"
                )
                self.report(
                    "U011",
                    rel,
                    line_number,
                    f"unit title {title!r} carries an 'N.M ' ordinal prefix. Ordering comes "
                    f"from {where} and the title carries no number. Strip it here AND in "
                    "this unit's module.yaml title, in the same commit: the published page "
                    "removes the leading H1 only when it matches the declared title exactly, "
                    "so stripping one side alone prints the title twice (M012).",
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
        self.check_video_in_body(cohort, rel, body, offset)
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

    def check_video_in_body(self, cohort: str, rel: str, body: str, offset: int) -> None:
        for _number, line in iter_prose_lines(body):
            if YOUTUBE_IN_TEXT.search(line):
                # Counted per cohort and reported once (see check_cohort).
                self.body_videos.setdefault(cohort, []).append(rel)
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
# Shared-curriculum v2 checker
# --------------------------------------------------------------------------

# v2 is deliberately implemented beside (rather than on top of) the v1
# cohort walker.  The old walker treats a cohort-owned module as importable;
# reusing it for an archive would make a historical module silently reappear
# in the website graph.  The dispatcher below selects one checker before any
# module discovery happens.
V2_MODULE_DIR = re.compile(r"^\d{2,}-[a-z0-9]+(?:-[a-z0-9]+)*$")
V2_LESSON_FILE = re.compile(r"^\d{2,}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
V2_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
V2_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
V2_PATH_ESCAPE = re.compile(r"%(?:2f|2F|5c|5C)")
V2_DELIVERIES = {"live", "self_paced"}
V2_CURRICULUM_KINDS = {"current", "github_archive"}
V2_HOMEWORK_V1_KEYS = {
    "schema_version",
    "content_id",
    "slug",
    "title",
    "instructions_path",
    "due_at",
    "initial_state",
    "form",
    "questions",
}


class SharedCurriculumChecker(Checker):
    """Strict checker for the root-shared curriculum contract (schema 2).

    It intentionally does not call :meth:`Checker.run`: v1's discovery rules
    are the opposite of the v2 layout.  The class still reuses the bounded
    Finding/Allowance transport so the standalone CLI and JSON output remain
    compatible with existing course workflows.
    """

    def __init__(self, repo: Repo, phase: int) -> None:
        super().__init__(repo=repo, phase=phase)
        self.root_modules: dict[str, str] = {}
        self.current_cohorts: set[str] = set()
        self.archive_cohorts: set[str] = set()
        self.mapped_homework: dict[str, set[str]] = {}
        self._reported_paths: set[str] = set()
        self.declared_cohorts: dict[str, str] = {}
        self.declared_current_cohort: str | None = None

    # -- bounded YAML and path helpers ------------------------------------

    def _v2_report(self, rule: str, rel: str, message: str, line: int = 1) -> None:
        self.report(rule, rel, line, message)

    def _bounded(self, value: Any, rel: str, depth: int = 0, active: set[int] | None = None) -> None:
        """Reject pathological YAML before any recursive validation.

        PyYAML's safe loader already blocks Python object construction.  The
        explicit bounds keep aliases and very large authoring mistakes from
        consuming unbounded checker memory, and make the source contract match
        the website snapshot admission ceiling.
        """

        if active is None:
            active = set()
        if depth > 32:
            self._v2_report("v2_schema", rel, "YAML nesting exceeds the maximum depth of 32")
            return
        if isinstance(value, str):
            if len(value) > 100_000:
                self._v2_report("v2_schema", rel, "YAML string exceeds the 100000-character bound")
            return
        if isinstance(value, (list, tuple)):
            if len(value) > 1_000:
                self._v2_report("v2_schema", rel, "YAML list exceeds the 1000-item bound")
            marker = id(value)
            if marker in active:
                self._v2_report("v2_schema", rel, "YAML aliases form a recursive value")
                return
            active.add(marker)
            for item in value:
                self._bounded(item, rel, depth + 1, active)
            active.remove(marker)
            return
        if isinstance(value, dict):
            if len(value) > 1_000:
                self._v2_report("v2_schema", rel, "YAML mapping exceeds the 1000-item bound")
            marker = id(value)
            if marker in active:
                self._v2_report("v2_schema", rel, "YAML aliases form a recursive value")
                return
            active.add(marker)
            for key, item in value.items():
                if not isinstance(key, str):
                    self._v2_report("v2_schema", rel, "YAML mapping keys must be strings")
                self._bounded(item, rel, depth + 1, active)
            active.remove(marker)

    def _load_v2_yaml(self, rel: str) -> dict[str, Any] | None:
        if not self.repo.exists(rel):
            self._v2_report("v2_schema", rel, "required YAML file does not exist")
            return None
        try:
            loaded = yaml.load(self.repo.read(rel), Loader=DuplicateKeyLoader)
        except (yaml.YAMLError, TypeError, ValueError) as error:
            line = getattr(getattr(error, "problem_mark", None), "line", 0) + 1
            self._v2_report("v2_schema", rel, f"YAML is invalid or has duplicate keys: {error}", line)
            return None
        if not isinstance(loaded, dict):
            self._v2_report("v2_schema", rel, "top-level YAML value must be a mapping")
            return None
        self._bounded(loaded, rel)
        return loaded

    def _keys(
        self,
        rel: str,
        mapping: dict[str, Any],
        allowed: set[str],
        required: set[str],
    ) -> None:
        for key in sorted(set(mapping) - allowed, key=repr):
            self._v2_report("v2_schema", rel, f"unknown key {key!r}")
        for key in sorted(required - set(mapping)):
            self._v2_report("v2_schema", rel, f"required key {key!r} is missing")

    def _schema(self, rel: str, mapping: dict[str, Any], expected: int = 2) -> bool:
        value = mapping.get("schema_version")
        if type(value) is not int or value != expected:
            self._v2_report(
                "v2_mixed_version" if value == 1 else "v2_schema",
                rel,
                f"schema_version must be the integer {expected} for this v2 source",
            )
            return False
        return True

    def _string(
        self,
        rel: str,
        mapping: dict[str, Any],
        key: str,
        *,
        required: bool = False,
        maximum: int = 100_000,
        nonempty: bool = False,
    ) -> str | None:
        if key not in mapping:
            if required:
                self._v2_report("v2_schema", rel, f"{key} must be a string")
            return None
        value = mapping[key]
        if type(value) is not str:
            self._v2_report("v2_schema", rel, f"{key} must be a native YAML string")
            return None
        if len(value) > maximum:
            self._v2_report("v2_schema", rel, f"{key} exceeds the {maximum}-character bound")
        if nonempty and not value.strip():
            self._v2_report("v2_schema", rel, f"{key} must not be empty")
        return value

    def _safe_path(self, rel: str, value: Any, *, rule: str = "v2_path_unsafe") -> str | None:
        """Mirror the website parser's actual path-safety checks
        (content_sync/course_repository.py's _validate_repository_path and
        _relative_source_reference): relative, contained, no traversal, no
        URL scheme -- but the parser never demands canonical PurePosixPath
        form. A trailing slash ("code/") or a leading "./" ("./terraform")
        names an ordinary directory reference and the parser accepts it; only
        ".." components, absolute paths, control characters and schemes make
        a path genuinely unsafe.
        """
        if type(value) is not str:
            self._v2_report(rule, rel, "path must be a repository-relative POSIX string")
            return None
        if (
            not value
            or len(value) > 512
            or value != value.strip()
            or value.startswith(("/", "\\"))
            or "\\" in value
            or "\x00" in value
            or any(ord(character) < 32 or ord(character) == 127 for character in value)
            or V2_SCHEME.match(value)
            or V2_PATH_ESCAPE.search(value)
        ):
            self._v2_report(rule, rel, f"unsafe repository-relative path {value!r}")
            return None
        parts = PurePosixPath(value).parts
        if not parts or ".." in parts:
            self._v2_report(rule, rel, f"unsafe repository-relative path {value!r}")
            return None
        return value

    def _inside(self, path: str, prefix: str) -> bool:
        return path == prefix or path.startswith(prefix.rstrip("/") + "/")

    def _register_id(self, rel: str, value: Any, pointer: str = "content_id") -> None:
        if type(value) is not str:
            self._v2_report("content_id_duplicate", rel, f"{pointer} must be a canonical UUID string")
            return
        try:
            parsed = UUID(value)
        except (ValueError, AttributeError):
            self._v2_report("content_id_duplicate", rel, f"{pointer} {value!r} is not a UUID")
            return
        if str(parsed) != value:
            self._v2_report(
                "content_id_duplicate",
                rel,
                f"{pointer} must use canonical lowercase UUID form {parsed}",
            )
            return
        previous = self.content_ids.get(value)
        if previous is not None:
            self._v2_report(
                "content_id_duplicate",
                rel,
                f"{pointer} {value} is already registered at {previous}",
            )
            return
        self.content_ids[value] = rel

    def _check_symlinks(self) -> None:
        """Walk without following links and reject every source-tree link."""

        def visit(directory: Path, prefix: str) -> None:
            try:
                entries = sorted(directory.iterdir(), key=lambda item: item.name)
            except OSError as error:
                self._v2_report("v2_path_unsafe", prefix or ".", f"cannot inspect source tree: {error}")
                return
            for entry in entries:
                if entry.name in IGNORED_DIRS:
                    continue
                path = f"{prefix}/{entry.name}" if prefix else entry.name
                if entry.is_symlink():
                    if path not in self._reported_paths:
                        self._reported_paths.add(path)
                        self._v2_report("v2_path_unsafe", path, "symlinks are not admitted in a v2 source tree")
                    continue
                if entry.is_dir():
                    visit(entry, path)

        visit(self.repo.root, "")

    # -- v2 entry point ----------------------------------------------------

    def run(self) -> None:
        self.load_config()
        self._check_symlinks()
        course = self._check_course()
        if course is None:
            self._check_allowances()
            return
        self._discover_root_modules()
        cohorts = self._discover_v2_cohorts()
        for cohort in cohorts:
            self._check_v2_cohort(cohort)
        self._check_declared_cohorts_against_reality()
        self._check_allowances()

    def _check_allowances(self) -> None:
        for allowance in self.allowances:
            if not allowance.used:
                self.report(
                    "C002",
                    ".zoomcamp-check.yaml",
                    1,
                    f"allowance {allowance.rule} for {allowance.path} matched nothing -- delete it",
                )

    # -- course and root curriculum --------------------------------------

    def _check_course(self) -> dict[str, Any] | None:
        rel = "course.yaml"
        mapping = self._load_v2_yaml(rel)
        if mapping is None:
            return None
        self._keys(
            rel,
            mapping,
            {
                "schema_version",
                "content_id",
                "slug",
                "title",
                "current_cohort",
                "cohorts",
                "description",
                "outcome",
                "urls",
                "hashtag",
                "published",
            },
            {
                "schema_version",
                "content_id",
                "slug",
                "title",
                "current_cohort",
                "cohorts",
                "description",
                "outcome",
                "urls",
                "hashtag",
                "published",
            },
        )
        if not self._schema(rel, mapping):
            return None
        self._register_id(rel, mapping.get("content_id"))
        slug = self._string(rel, mapping, "slug", required=True, maximum=100, nonempty=True)
        self.course_slug = slug or ""
        if slug is not None and SLUG.fullmatch(slug) is None:
            self._v2_report("v2_schema", rel, f"slug {slug!r} is not kebab-case")
        for key in ("title", "outcome", "hashtag", "description", "current_cohort"):
            self._string(rel, mapping, key, required=True, nonempty=True)
        current_cohort = mapping.get("current_cohort")
        self.declared_current_cohort = current_cohort if type(current_cohort) is str else None
        self._check_declared_cohorts_list(rel, mapping.get("cohorts"))
        urls = mapping.get("urls")
        if not isinstance(urls, dict):
            self._v2_report("v2_schema", rel, "urls must be a mapping")
        else:
            urls_rel = f"{rel}:urls"
            self._keys(urls_rel, urls, {"repository", "docs", "faq"}, {"repository", "docs", "faq"})
            for key in ("repository", "docs", "faq"):
                value = self._string(urls_rel, urls, key, required=True, maximum=2048, nonempty=True)
                if value is not None and not value.startswith("https://"):
                    self._v2_report("v2_schema", rel, f"urls.{key} must be an https URL")
        if type(mapping.get("published")) is not bool:
            self._v2_report("v2_schema", rel, "published must be a boolean")
        if not self.repo.exists("cohorts/README.md"):
            self._v2_report("v2_schema", "cohorts/README.md", "cohorts/README.md is required")
        return mapping

    def _check_declared_cohorts_list(self, rel: str, raw: Any) -> None:
        """course.yaml:cohorts is the explicit index of every cohort and
        where its content lives -- 'root' for the current one, its own
        cohorts/<id> path for every other one. An archive entry may add
        legacy: true to mark a cohort.yaml retrofitted onto pre-v2 content
        (dates inferred after the fact, not authored at the time) rather
        than one a v2-native archive-then-bootstrap cycle produced. This
        method only checks the list is well-formed;
        _check_declared_cohorts_against_reality (run at the end, once every
        cohort.yaml has actually been read) checks it against what is
        really on disk.
        """
        if not isinstance(raw, list) or not raw:
            self._v2_report("v2_schema", rel, "cohorts must be a non-empty list")
            return
        seen_root = None
        for index, entry in enumerate(raw):
            pointer = f"{rel}:cohorts[{index}]"
            if not isinstance(entry, dict):
                self._v2_report("v2_schema", pointer, "each cohorts[] entry must be a mapping")
                continue
            self._keys(pointer, entry, {"identifier", "content", "legacy"}, {"identifier", "content"})
            identifier = self._string(pointer, entry, "identifier", required=True, maximum=80, nonempty=True)
            content = self._string(pointer, entry, "content", required=True, nonempty=True)
            legacy = entry.get("legacy", False)
            if "legacy" in entry and type(legacy) is not bool:
                self._v2_report("v2_schema", pointer, "legacy must be a boolean")
            if identifier is None or content is None:
                continue
            if identifier in self.declared_cohorts:
                self._v2_report("v2_schema", pointer, f"identifier {identifier!r} is already listed")
                continue
            expected_archive_content = f"cohorts/{identifier}"
            if content == "root":
                if seen_root is not None:
                    self._v2_report(
                        "v2_schema", pointer, f"only one cohort may declare content: root (already {seen_root!r})"
                    )
                else:
                    seen_root = identifier
                if legacy is True:
                    self._v2_report("v2_schema", pointer, "the current cohort (content: root) cannot be legacy: true")
            elif content != expected_archive_content:
                self._v2_report(
                    "v2_schema",
                    pointer,
                    f"content must be 'root' or its own {expected_archive_content!r}, not {content!r}",
                )
            self.declared_cohorts[identifier] = content
        if seen_root is None:
            self._v2_report("v2_schema", rel, "exactly one cohorts[] entry must declare content: root")
        elif self.declared_current_cohort is not None and seen_root != self.declared_current_cohort:
            self._v2_report(
                "v2_schema",
                rel,
                f"current_cohort {self.declared_current_cohort!r} disagrees with the cohorts[] entry "
                f"declaring content: root ({seen_root!r})",
            )

    def _check_declared_cohorts_against_reality(self) -> None:
        actual = self.current_cohorts | self.archive_cohorts
        declared = set(self.declared_cohorts)
        for missing in sorted(actual - declared):
            self._v2_report(
                "v2_schema", "course.yaml", f"cohorts/{missing}/cohort.yaml exists but is not listed in cohorts[]"
            )
        for stale in sorted(declared - actual):
            self._v2_report(
                "v2_schema", "course.yaml", f"cohorts[] lists {stale!r} but cohorts/{stale}/cohort.yaml was not found"
            )
        for identifier in sorted(declared & actual):
            content = self.declared_cohorts[identifier]
            is_current = identifier in self.current_cohorts
            if is_current and content != "root":
                self._v2_report(
                    "v2_schema", "course.yaml", f"cohorts[{identifier!r}] is curriculum: current but content != root"
                )
            elif not is_current and content == "root":
                self._v2_report(
                    "v2_schema",
                    "course.yaml",
                    f"cohorts[{identifier!r}] is curriculum: github_archive but content: root",
                )

    def _discover_root_modules(self) -> None:
        if not self.repo.exists("module.yaml"):
            pass
        else:
            self._v2_report("module_path_not_root", "module.yaml", "module.yaml must be inside a numbered root module")
        try:
            entries = sorted(self.repo.root.iterdir(), key=lambda item: item.name)
        except OSError:
            return
        candidates: list[str] = []
        for entry in entries:
            if entry.name in IGNORED_DIRS or entry.is_symlink() or not entry.is_dir():
                continue
            if NUMBERED_DIR.match(entry.name):
                if V2_MODULE_DIR.fullmatch(entry.name) is None:
                    self._v2_report(
                        "numbered_module_required",
                        entry.name,
                        "root numbered directory must be NN-kebab-case",
                    )
                else:
                    candidates.append(entry.name)
        if not candidates:
            self._v2_report("current_module_missing", ".", "no numbered root modules were found")
        prefixes: dict[str, str] = {}
        for slug in candidates:
            prefix = slug.split("-", 1)[0].lstrip("0") or "0"
            if prefix in prefixes:
                self._v2_report(
                    "duplicate_number_prefix",
                    slug,
                    f"module prefix {prefix} is already used by {prefixes[prefix]}",
                )
            else:
                prefixes[prefix] = slug
            self._check_root_module(slug)

    def _check_root_module(self, slug: str) -> None:
        base = slug
        rel = f"{base}/module.yaml"
        if not self.repo.exists(rel):
            # Not an error: the parser's own discovery (_root_module_dirs in
            # content_sync/course_repository_v2.py) only considers a
            # directory a module when it has a module.yaml -- a validly
            # numbered directory without one is silently excluded from the
            # current curriculum, exactly like shared-curriculum-v2.md's
            # "modules are discovered, never listed" documents. It is a
            # legitimate draft, not a defect, so the checker reports nothing.
            return
        mapping = self._load_v2_yaml(rel)
        if mapping is None:
            return
        self._keys(rel, mapping, {"schema_version", "content_id", "title", "units"}, {"schema_version", "content_id", "title", "units"})
        if not self._schema(rel, mapping):
            return
        self._register_id(rel, mapping.get("content_id"))
        title = self._string(rel, mapping, "title", required=True, nonempty=True)
        units = mapping.get("units")
        if not isinstance(units, list) or not units:
            self._v2_report("v2_schema", rel, "units must be a non-empty list")
            units = []
        self.root_modules[slug] = rel
        declared_paths: set[str] = set()
        prefixes: dict[str, str] = {}
        for index, raw in enumerate(units):
            pointer = f"units[{index}]"
            if not isinstance(raw, dict):
                self._v2_report("v2_schema", rel, f"{pointer} must be a mapping")
                continue
            self._keys(rel, raw, {"content_id", "title", "path"}, {"content_id", "title", "path"})
            self._register_id(rel, raw.get("content_id"), f"{pointer}.content_id")
            unit_title = self._string(rel, raw, "title", nonempty=True)
            raw_path = self._safe_path(rel, raw.get("path"))
            if raw_path is None:
                continue
            if "/" in raw_path or not V2_LESSON_FILE.fullmatch(raw_path):
                self._v2_report(
                    "numbered_lesson_required",
                    f"{base}/{raw_path}",
                    "lesson path must be a direct NN-kebab.md sibling of module.yaml",
                )
                continue
            unit_rel = f"{base}/{raw_path}"
            if not self.repo.exists(unit_rel):
                self._v2_report("numbered_lesson_required", unit_rel, "declared lesson does not exist")
                continue
            declared_paths.add(raw_path)
            prefix = raw_path.split("-", 1)[0].lstrip("0") or "0"
            if prefix in prefixes:
                self._v2_report(
                    "duplicate_number_prefix",
                    unit_rel,
                    f"lesson prefix {prefix} is already used by {prefixes[prefix]}",
                )
            else:
                prefixes[prefix] = raw_path
            if unit_title is not None:
                self._check_lesson(unit_rel, unit_title)
        module_dir = self.repo.root / base
        on_disk: set[str] = set()
        if module_dir.is_dir() and not module_dir.is_symlink():
            for entry in sorted(module_dir.iterdir(), key=lambda item: item.name):
                if entry.name in IGNORED_DIRS or entry.is_symlink():
                    continue
                if entry.is_dir():
                    if entry.name == "lessons":
                        self._v2_report("numbered_lesson_required", f"{base}/lessons", "lessons/ is not part of v2")
                    continue
                if entry.name in {"homework.yaml", "homework.md"}:
                    self._v2_report(
                        "homework_path_outside_cohort",
                        f"{base}/{entry.name}",
                        "homework belongs under cohorts/<id>/, never inside a root module",
                    )
                    continue
                if entry.name in {"module.yaml", "README.md"}:
                    continue
                if entry.suffix == ".md":
                    if V2_LESSON_FILE.fullmatch(entry.name) is None:
                        self._v2_report("numbered_lesson_required", f"{base}/{entry.name}", "lesson filename must be NN-kebab.md")
                    else:
                        on_disk.add(entry.name)
        for orphan in sorted(on_disk - declared_paths):
            self._v2_report("curriculum_source_mismatch", f"{base}/{orphan}", "lesson exists but is absent from module.yaml units")
        if not self.repo.exists(f"{base}/README.md"):
            self._v2_report("numbered_module_required", f"{base}/README.md", "each module needs a README.md index")
        # A module README is GitHub-facing decoration only: the website
        # parser (_parse_module in content_sync/course_repository_v2.py)
        # decodes it into overview_markdown and never scans its body for
        # links, so the checker must not link-check its content either --
        # existence above is the whole contract.

    def _check_frontmatter(self, rel: str, frontmatter: str, module_base: str) -> None:
        try:
            mapping = yaml.load(frontmatter, Loader=DuplicateKeyLoader) or {}
        except (yaml.YAMLError, TypeError, ValueError) as error:
            self._v2_report("v2_schema", rel, f"unit frontmatter is invalid: {error}")
            return
        if not isinstance(mapping, dict):
            self._v2_report("v2_schema", rel, "unit frontmatter must be a mapping")
            return
        self._bounded(mapping, rel)
        self._keys(rel, mapping, {"video_url", "code"}, set())
        video = mapping.get("video_url")
        if video is not None and (type(video) is not str or not video.startswith("https://")):
            self._v2_report("v2_schema", rel, "video_url must be an https string")
        code = mapping.get("code")
        if code is None:
            return
        if not isinstance(code, list):
            self._v2_report("v2_schema", rel, "code must be a list of label/path mappings")
            return
        for index, entry in enumerate(code):
            if not isinstance(entry, dict) or set(entry) != {"label", "path"}:
                self._v2_report("v2_schema", rel, f"code[{index}] needs exactly label and path")
                continue
            target = self._safe_path(rel, entry.get("path"))
            if target is None:
                continue
            resolved = posixpath.normpath(posixpath.join(module_base, target))
            if not self._inside(resolved, module_base) or not self.repo.exists(resolved):
                self._v2_report("v2_path_unsafe", rel, f"code[{index}].path {target!r} is not inside the module")

    def _check_lesson(self, rel: str, title: str) -> None:
        text = self.repo.read(rel)
        frontmatter, offset, body = split_frontmatter(text)
        if text.startswith("---") and frontmatter is None:
            self._v2_report("v2_schema", rel, "lesson frontmatter is not closed")
        if frontmatter is not None:
            self._check_frontmatter(rel, frontmatter, posixpath.dirname(rel))
        first = first_content_line(body, offset)
        if first is None or not first[1].startswith("# ") or first[1].startswith("## "):
            self._v2_report("numbered_lesson_required", rel, "lesson must begin with exactly one '# Title' H1")
        else:
            heading = first[1][2:].strip()
            if NUMERIC_TITLE_PREFIX.match(heading):
                self._v2_report("numbered_lesson_required", rel, "lesson H1 must be unnumbered; numbering belongs to its filename")
            if _collapse(heading) != _collapse(title):
                self._v2_report("curriculum_source_mismatch", rel, f"lesson H1 {heading!r} disagrees with module title {title!r}")
            for line_number, line in iter_prose_lines(body):
                if line_number + offset - 1 != first[0] and line.startswith("# "):
                    self._v2_report("numbered_lesson_required", rel, "lesson has a second H1")
        self._check_local_links(rel, text, posixpath.dirname(rel), image_inside=True)

    def _check_local_links(self, rel: str, text: str, base: str, *, image_inside: bool) -> None:
        for line, is_image, raw in iter_targets(text):
            target = raw.split("#", 1)[0].split("?", 1)[0].strip()
            if not target or is_external(raw):
                continue
            # A prose link may intentionally climb one level, to a sibling
            # root module or to a root-level file (for example
            # ../02-agents/01-loops.md or ../project.md).  cohorts/README.md
            # documents both as legitimate relative-link targets, and the
            # website parser's own reference resolver
            # (_relative_source_reference in content_sync/course_repository.py)
            # imposes no narrower restriction on where such a link may land:
            # any existing repository path that does not escape the
            # repository root is fine.  Images and code remain module-local
            # (checked separately, below and in _check_frontmatter).
            if ".." in PurePosixPath(target).parts:
                if (
                    len(target) > 512
                    or target != target.strip()
                    or target.startswith(("/", "\\"))
                    or "\\" in target
                    or "\x00" in target
                    or any(ord(character) < 32 or ord(character) == 127 for character in target)
                    or V2_SCHEME.match(target)
                    or V2_PATH_ESCAPE.search(target)
                    or not target.startswith("../")
                    or target.count("..") != 1
                ):
                    self._v2_report("v2_path_unsafe", rel, f"unsafe repository-relative path {target!r}", line)
                    continue
                safe = target
            else:
                safe = self._safe_path(rel, target)
            if safe is None:
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(rel), safe))
            if resolved.startswith("../") or resolved == ".." or resolved.startswith("cohorts/"):
                self._v2_report("v2_path_unsafe", rel, f"local link {raw!r} leaves current curriculum", line)
                continue
            if is_image and image_inside and not self._inside(resolved, base):
                self._v2_report("v2_path_unsafe", rel, f"image {raw!r} leaves its module", line)
                continue
            if not self.repo.exists(resolved) and not (self.repo.root / resolved).is_dir():
                self._v2_report("v2_path_unsafe", rel, f"local link {raw!r} does not exist", line)

    # -- cohort and homework bindings -------------------------------------

    def _discover_v2_cohorts(self) -> list[str]:
        base = self.repo.root / "cohorts"
        if not base.is_dir() or base.is_symlink():
            self._v2_report("v2_schema", "cohorts", "cohorts/ must be a directory")
            return []
        found: list[str] = []
        for entry in sorted(base.iterdir(), key=lambda item: item.name):
            if entry.name in IGNORED_DIRS or entry.is_symlink() or not entry.is_dir():
                continue
            manifest = f"cohorts/{entry.name}/cohort.yaml"
            if self.repo.exists(manifest):
                found.append(entry.name)
            elif (entry / "archive.yaml").is_file():
                # bootstrap's additive archive plan can exist briefly before
                # its v2 cohort notice manifest is authored.  Its descendants
                # remain opaque; they are never sent to the current walker.
                continue
            elif any(item.name != "README.md" for item in entry.iterdir()):
                self._v2_report("v2_schema", f"cohorts/{entry.name}", "cohort directory needs cohort.yaml")
        return found

    def _check_v2_cohort(self, cohort: str) -> None:
        rel = f"cohorts/{cohort}/cohort.yaml"
        mapping = self._load_v2_yaml(rel)
        if mapping is None:
            return
        self._keys(
            rel,
            mapping,
            {
                "schema_version",
                "content_id",
                "identifier",
                "course",
                "delivery",
                "published",
                "start_date",
                "end_date",
                "title",
                "description",
                "curriculum",
                "homework",
                "archive",
            },
            {"schema_version", "content_id", "identifier", "course", "delivery", "published", "curriculum", "homework"},
        )
        if not self._schema(rel, mapping):
            return
        self._register_id(rel, mapping.get("content_id"))
        identifier = self._string(rel, mapping, "identifier", required=True, maximum=80, nonempty=True)
        if identifier != cohort:
            self._v2_report("v2_schema", rel, f"identifier {identifier!r} must equal cohort directory {cohort!r}")
        course = self._string(rel, mapping, "course", required=True, maximum=100, nonempty=True)
        if self.course_slug and course != self.course_slug:
            self._v2_report("v2_schema", rel, f"course {course!r} disagrees with course.yaml slug {self.course_slug!r}")
        delivery = self._string(rel, mapping, "delivery", required=True, maximum=20, nonempty=True)
        if delivery not in V2_DELIVERIES:
            self._v2_report("invalid_delivery", rel, "delivery must be live or self-paced")
        published = mapping.get("published")
        if type(published) is not bool:
            self._v2_report("v2_schema", rel, "published must be a boolean")
            published = False
        start = self._date_value(rel, mapping, "start_date")
        end = self._date_value(rel, mapping, "end_date")
        if start and end and end < start:
            self._v2_report("v2_schema", rel, "end_date must not precede start_date")
        if published and delivery == "live" and (start is None or end is None):
            self._v2_report("v2_schema", rel, "published live cohorts require start_date and end_date")
        # An archive cohort's required notice file is whatever archive.notice_path
        # names (checked in _check_archive_block below) -- the parser's
        # _parse_archive_block in content_sync/course_repository_v2.py never
        # requires that file to be specifically README.md, and
        # machine-learning-zoomcamp's cohorts/2021 and mlops-zoomcamp's
        # cohorts/2022 both point notice_path at leaderboard.md instead. Only
        # a non-archive (current) cohort needs cohorts/<id>/README.md itself.
        if mapping.get("curriculum") != "github_archive" and not self.repo.exists(f"cohorts/{cohort}/README.md"):
            self._v2_report("v2_schema", f"cohorts/{cohort}/README.md", "cohort README.md is required")
        curriculum = mapping.get("curriculum")
        if type(curriculum) is not str:
            self._v2_report("v2_schema", rel, "curriculum must be the scalar current or github_archive")
            return
        kind = curriculum
        if kind not in V2_CURRICULUM_KINDS:
            self._v2_report("invalid_curriculum_kind", rel, "curriculum must be current or github_archive")
            return
        if kind == "current":
            self.current_cohorts.add(cohort)
        else:
            self.archive_cohorts.add(cohort)
        if kind == "current" and not self.root_modules:
            self._v2_report("current_module_missing", rel, "current curriculum has no discovered root modules")
        if kind == "github_archive":
            self._check_archive_block(cohort, mapping.get("archive"), rel)
        elif "archive" in mapping:
            self._v2_report("v2_schema", rel, "current cohorts cannot declare archive metadata")
        self._check_homework_mappings(cohort, kind, mapping.get("homework", []), rel, delivery)

    def _date_value(self, rel: str, mapping: dict[str, Any], key: str) -> date | None:
        if key not in mapping or mapping[key] is None:
            return None
        value = mapping[key]
        if type(value) is not str or V2_DATE.fullmatch(value) is None:
            self._v2_report("v2_schema", rel, f"{key} must be a quoted YYYY-MM-DD string or null")
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            self._v2_report("v2_schema", rel, f"{key} is not a calendar date")
            return None

    def _check_archive_block(self, cohort: str, raw: Any, rel: str) -> None:
        if not isinstance(raw, dict) or set(raw) != {"notice_path"}:
            self._v2_report("archive_notice_missing", rel, "github_archive requires archive.notice_path")
            return
        notice = self._safe_path(rel, raw.get("notice_path"), rule="archive_url_invalid")
        if notice is None:
            return
        if not self._inside(notice, f"cohorts/{cohort}/") or not notice.endswith(".md"):
            self._v2_report("archive_url_invalid", rel, "archive.notice_path must be Markdown inside its cohort")
        elif not self.repo.exists(notice):
            self._v2_report("archive_notice_missing", notice, "archive notice file does not exist")

    def _check_homework_mappings(
        self, cohort: str, kind: str, raw: Any, rel: str, delivery: str = "live"
    ) -> None:
        if raw is None:
            raw = []
        if not isinstance(raw, list):
            self._v2_report("homework_mapping_missing", rel, "homework must be a list (use [] when there are none)")
            return
        if delivery == "self_paced" and raw:
            # The bootstrap producer refuses to author self-paced assignments
            # (self_paced_homework_unsupported).  The checker refuses a
            # hand-authored attempt for the same reason: self-paced phase one
            # is reading, shared progress and ungraded practice only, so a
            # graded assignment and its deadline cannot sneak in through a
            # manifest the producer never wrote.
            self._v2_report(
                "self_paced_homework_rejected",
                rel,
                "self-paced requires homework: [] in this slice; graded assignments are a live-cohort capability",
            )
        mapped: set[str] = set()
        modules_seen: set[str | None] = set()
        for index, item in enumerate(raw):
            pointer = f"homework[{index}]"
            if not isinstance(item, dict) or set(item) != {"module", "source"}:
                self._v2_report("homework_mapping_missing", rel, f"{pointer} needs exactly module and source")
                continue
            module = item.get("module")
            if kind == "github_archive":
                if module is not None:
                    self._v2_report("archive_module_reference", rel, f"{pointer}.module must be null for archive homework")
            elif type(module) is not str:
                self._v2_report("homework_mapping_missing", rel, f"{pointer}.module must be a root module slug")
            elif module not in self.root_modules:
                self._v2_report("curriculum_source_mismatch", rel, f"{pointer}.module {module!r} is not a current root module")
            module_key: str | None = module if type(module) is str or module is None else repr(module)
            if kind == "current" and module_key in modules_seen:
                self._v2_report("homework_mapping_missing", rel, f"{pointer}.module is mapped more than once")
            if kind == "current":
                modules_seen.add(module_key)
            source = self._safe_path(rel, item.get("source"))
            if source is None:
                continue
            cohort_prefix = f"cohorts/{cohort}/"
            if not self._inside(source, cohort_prefix):
                self._v2_report("homework_path_outside_cohort", rel, f"{pointer}.source leaves {cohort_prefix}")
                continue
            if not source.endswith("/homework.yaml"):
                self._v2_report("homework_mapping_missing", rel, f"{pointer}.source must end in homework.yaml")
                continue
            if kind == "current" and source != f"cohorts/{cohort}/homework/{module}/homework.yaml":
                self._v2_report("homework_mapping_missing", rel, "current homework uses cohorts/<id>/homework/<module>/homework.yaml")
            if source in mapped:
                self._v2_report("homework_mapping_missing", rel, f"{pointer}.source is mapped more than once")
            mapped.add(source)
            if not self.repo.exists(source):
                self._v2_report("homework_mapping_missing", source, "mapped homework.yaml does not exist")
                continue
            md = f"{posixpath.dirname(source)}/homework.md"
            if not self.repo.exists(md):
                self._v2_report("homework_mapping_missing", md, "mapped homework needs a co-located homework.md")
            self._check_homework_manifest(cohort, kind, source)
        self.mapped_homework[cohort] = mapped
        if kind == "current":
            base = f"cohorts/{cohort}"
            for path in sorted(self.repo.files):
                if not path.startswith(base + "/") or not path.endswith("/homework.yaml"):
                    continue
                if path not in mapped:
                    self._v2_report("homework_unreferenced", path, "homework.yaml is not reachable from cohort.yaml")

    def _check_homework_manifest(self, cohort: str, kind: str, rel: str) -> None:
        mapping = self._load_v2_yaml(rel)
        if mapping is None:
            return
        allowed = set(V2_HOMEWORK_V1_KEYS)
        self._keys(rel, mapping, allowed, {"schema_version", "content_id"})
        version = mapping.get("schema_version")
        if kind == "current" and not self._schema(rel, mapping):
            return
        if kind == "github_archive" and (type(version) is not int or version not in {1, 2}):
            self._v2_report("v2_mixed_version", rel, "archive homework may be schema 1 or 2 during migration")
        self._register_id(rel, mapping.get("content_id"))
        for key in ("slug", "title"):
            if key in mapping:
                self._string(rel, mapping, key, nonempty=True)
        instructions = mapping.get("instructions_path")
        if instructions is not None and instructions != "homework.md":
            self._v2_report("homework_path_outside_cohort", rel, "instructions_path must be the co-located homework.md")
        due = mapping.get("due_at")
        if due is not None and type(due) is not str and not (kind == "github_archive" and isinstance(due, date)):
            self._v2_report("v2_schema", rel, "due_at must be a quoted timestamp or null")
        if kind == "current" and self.repo.exists(f"{posixpath.dirname(rel)}/homework.md") and due is None:
            self._v2_report("v2_schema", rel, "a mapped current/live homework needs a real due_at")
        questions = mapping.get("questions")
        if questions is not None:
            if not isinstance(questions, list):
                self._v2_report("v2_schema", rel, "questions must be a list")
            else:
                for index, question in enumerate(questions):
                    if not isinstance(question, dict):
                        self._v2_report("v2_schema", rel, f"questions[{index}] must be a mapping")
                        continue
                    self._keys(
                        rel,
                        question,
                        {"content_id", "id", "type", "prompt", "options", "points", "answer_type", "answer"},
                        set(),
                    )
                    if "content_id" in question:
                        self._register_id(rel, question["content_id"], f"questions[{index}].content_id")


# Short compatibility name for callers that treat the checker as a schema
# version rather than a layout description.
V2Checker = SharedCurriculumChecker


def checker_for_repo(repo: Repo, phase: int) -> Checker:
    """Choose v1 or v2 before any cohort/module discovery takes place."""

    if not repo.exists("course.yaml"):
        return Checker(repo=repo, phase=phase)
    raw_manifest = repo.read("course.yaml")
    try:
        root_manifest = yaml.load(raw_manifest, Loader=DuplicateKeyLoader)
    except (yaml.YAMLError, TypeError, ValueError):
        # A malformed v2 manifest still needs the v2 diagnostic and must not
        # fall back to the old cohort walker.  BaseLoader is used only for
        # dispatch; the v2 checker reparses with DuplicateKeyLoader and emits
        # the actionable duplicate/schema finding.
        try:
            root_manifest = yaml.load(raw_manifest, Loader=yaml.BaseLoader)
        except (yaml.YAMLError, TypeError, ValueError):
            root_manifest = None
    if isinstance(root_manifest, dict) and type(root_manifest.get("schema_version")) is int and root_manifest.get("schema_version") == 2:
        return SharedCurriculumChecker(repo=repo, phase=phase)
    if isinstance(root_manifest, dict) and root_manifest.get("schema_version") == "2":
        return SharedCurriculumChecker(repo=repo, phase=phase)
    return Checker(repo=repo, phase=phase)


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
        for rule, (rule_class, description) in sorted({**RULES, **V2_RULES}.items()):
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

    checker = checker_for_repo(repo, phase)
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
            print("Rules: STRUCTURE.md and docs/curriculum-contract.md in DataTalksClub/zoomcamp-ops")

    if args.warn_only:
        return 0
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
