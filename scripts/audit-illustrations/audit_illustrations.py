#!/usr/bin/env python3
"""Generate an auditable active-unit and illustration-reference report.

The scanner is intentionally read-only with respect to the course repositories.
It checks Markdown references, local image existence, and basic image metadata;
it does not pretend to verify visual crispness, crop orientation, semantic
fidelity, or overlays. Those checks remain an independent review responsibility.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import html
import re
import struct
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote


IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
REMOTE_PREFIXES = ("http://", "https://", "data:")
UNIT_HEADING_RE = re.compile(
    r"^(?P<hashes>#{2,4})\s+(?P<number>\d+(?:[A-Za-z]+)?\.\d+(?:\.\d+)?)\b(?P<title>.*)$"
)
MARKDOWN_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(\s*(?:<(?P<bracket>[^>]+)>|(?P<plain>[^\s)]+))"
)
HTML_IMAGE_RE = re.compile(
    r"<img\b[^>]*?\bsrc\s*=\s*[\"'](?P<src>[^\"']+)[\"']",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ScopeSpec:
    name: str
    repository: str
    mode: str
    path: str
    state: str
    selection: str


@dataclass
class Unit:
    scope: ScopeSpec
    path: Path
    title: str
    module: str
    refs: list["ImageRef"] = field(default_factory=list)


@dataclass
class ImageRef:
    unit: Unit
    line: int
    target: str
    kind: str = ""
    resolved_path: Path | None = None
    status: str = ""
    dimensions: str = "—"
    quality: str = ""


DEFAULT_SCOPE_SPECS = (
    ScopeSpec(
        "ML",
        "machine-learning-zoomcamp",
        "cohort",
        "cohorts/2026",
        "published current cohort",
        "the published 2026 cohort flow and its module manifests",
    ),
    ScopeSpec(
        "LLM",
        "llm-zoomcamp",
        "cohort",
        "cohorts/2026",
        "published current cohort",
        "the published 2026 cohort flow and its module manifests",
    ),
    ScopeSpec(
        "MLOps",
        "mlops-zoomcamp",
        "module-pages",
        "",
        "current self-paced curriculum",
        "numbered root module/project README pages; no published cohort manifest exists",
    ),
    ScopeSpec(
        "DE",
        "data-engineering-zoomcamp",
        "cohort",
        "cohorts/2027",
        "current draft; unpublished",
        "the current 2027 draft cohort and its module manifests; historical cohorts excluded",
    ),
)


def unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if value.startswith(("'", '"')):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value.strip("'\"")
        return str(parsed)
    return value.split(" #", 1)[0].strip()


def read_cohort_metadata(cohort_dir: Path) -> tuple[str, str]:
    cohort_file = cohort_dir / "cohort.yaml"
    if not cohort_file.is_file():
        return "metadata missing", "cohort.yaml missing"
    text = cohort_file.read_text(encoding="utf-8")
    published_match = re.search(r"^published:\s*(true|false)\s*$", text, re.MULTILINE)
    published = published_match.group(1) if published_match else "unknown"
    year_match = re.search(r"^year:\s*(\S+)\s*$", text, re.MULTILINE)
    year = year_match.group(1) if year_match else cohort_dir.name
    return f"published={published}", f"cohort {year}"


def flow_module_paths(repo: Path, cohort_dir: Path) -> list[Path]:
    cohort_file = cohort_dir / "cohort.yaml"
    if cohort_file.is_file():
        text = cohort_file.read_text(encoding="utf-8")
        sources = re.findall(r"^\s+source:\s*([^\s#]+)", text, re.MULTILINE)
        paths = [repo / unquote_yaml_scalar(source) for source in sources]
        if paths:
            return paths
    return sorted(cohort_dir.glob("*/module.yaml"))


def parse_module_units(scope: ScopeSpec, repo: Path) -> list[Unit]:
    cohort_dir = repo / scope.path
    units: list[Unit] = []
    for module_manifest in flow_module_paths(repo, cohort_dir):
        if not module_manifest.is_file():
            continue
        text = module_manifest.read_text(encoding="utf-8")
        current: dict[str, str] = {}
        module_name = module_manifest.parent.relative_to(repo).as_posix()

        def flush() -> None:
            if "path" not in current:
                return
            unit_path = module_manifest.parent / current["path"]
            title = current.get("title", Path(current["path"]).stem)
            units.append(Unit(scope, unit_path, title, module_name))

        for line in text.splitlines():
            if re.match(r"^\s*-\s+content_id:", line):
                flush()
                current = {}
                continue
            title_match = re.match(r"^\s+title:\s*(.+?)\s*$", line)
            path_match = re.match(r"^\s+path:\s*(.+?)\s*$", line)
            if title_match:
                current["title"] = unquote_yaml_scalar(title_match.group(1))
            elif path_match:
                current["path"] = unquote_yaml_scalar(path_match.group(1))
        flush()
    return units


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return re.sub(r"[*_`]", "", match.group(1)).strip()
    return fallback


def parse_module_page_units(scope: ScopeSpec, repo: Path) -> list[Unit]:
    units: list[Unit] = []
    for directory in sorted(repo.iterdir()):
        if not directory.is_dir() or not re.match(r"^\d{2}-", directory.name):
            continue
        readme = directory / "README.md"
        if not readme.is_file():
            continue
        title = first_heading(readme.read_text(encoding="utf-8"), directory.name)
        units.append(Unit(scope, readme, title, directory.name))
    return units


def iter_units(scope: ScopeSpec, repo: Path) -> list[Unit]:
    if scope.mode == "cohort":
        return parse_module_units(scope, repo)
    if scope.mode == "module-pages":
        return parse_module_page_units(scope, repo)
    raise ValueError(f"unsupported scope mode: {scope.mode}")


def image_targets(text: str) -> list[tuple[int, str]]:
    refs: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in MARKDOWN_IMAGE_RE.finditer(line):
            refs.append((number, match.group("bracket") or match.group("plain")))
        for match in HTML_IMAGE_RE.finditer(line):
            refs.append((number, match.group("src")))
    return refs


def clean_target(raw: str) -> str:
    target = html.unescape(raw.strip())
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target)


def classify_target(target: str) -> str:
    lowered = target.lower()
    if lowered.startswith(REMOTE_PREFIXES):
        return "remote"
    basename = Path(lowered).name
    if "thumbnail" in basename or "youtube" in lowered:
        return "navigation thumbnail"
    if "homework" in basename or "checklist" in basename:
        return "homework/support"
    if "illustration" in lowered or "imagegen" in basename or "crisp" in basename:
        return "instructional illustration"
    return "local image"


def resolve_local_target(repo: Path, unit_path: Path, target: str) -> Path | None:
    if target.startswith(REMOTE_PREFIXES):
        return None
    if target.startswith("/"):
        candidate = repo / target.lstrip("/")
    else:
        candidate = unit_path.parent / target
    return candidate.resolve(strict=False)


def parse_dimensions(path: Path) -> tuple[int, int] | None:
    """Read dimensions for common raster formats without third-party packages."""

    try:
        data = path.read_bytes()
    except OSError:
        return None

    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        return struct.unpack("<HH", data[6:10])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP" and len(data) >= 30:
        if data[12:16] == b"VP8X" and len(data) >= 30:
            width = 1 + int.from_bytes(data[24:27], "little")
            height = 1 + int.from_bytes(data[27:30], "little")
            return width, height
    if data[:2] == b"\xff\xd8":
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                index += 1
                continue
            while index < len(data) and data[index] == 0xFF:
                index += 1
            if index >= len(data):
                break
            marker = data[index]
            index += 1
            if marker in (0xD8, 0xD9):
                continue
            if index + 2 > len(data):
                break
            segment_length = struct.unpack(">H", data[index : index + 2])[0]
            if segment_length < 2 or index + segment_length > len(data):
                break
            if marker in {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            }:
                height, width = struct.unpack(">HH", data[index + 3 : index + 7])
                return width, height
            index += segment_length
    if path.suffix.lower() == ".svg":
        text = data.decode("utf-8", errors="ignore")[:8192]
        viewbox = re.search(r"viewBox\s*=\s*[\"']\s*[-\d.]+\s+[-\d.]+\s+(\d+)\s+(\d+)", text)
        if viewbox:
            return int(viewbox.group(1)), int(viewbox.group(2))
        width = re.search(r"\bwidth\s*=\s*[\"'](\d+)", text)
        height = re.search(r"\bheight\s*=\s*[\"'](\d+)", text)
        if width and height:
            return int(width.group(1)), int(height.group(1))
    return None


def format_dimensions(dimensions: tuple[int, int] | None) -> str:
    return f"{dimensions[0]}×{dimensions[1]}" if dimensions else "unknown"


def assess_reference(ref: ImageRef, repo: Path) -> None:
    ref.kind = classify_target(ref.target)
    if ref.kind == "remote":
        ref.status = "REMOTE"
        ref.quality = "not locally checked"
        return

    ref.resolved_path = resolve_local_target(repo, ref.unit.path, ref.target)
    if ref.resolved_path is None:
        ref.status = "REMOTE"
        ref.quality = "not locally checked"
        return
    try:
        ref.resolved_path.relative_to(repo.resolve())
    except ValueError:
        ref.status = "OUTSIDE"
        ref.quality = "action required"
        return
    if not ref.resolved_path.is_file():
        ref.status = "MISSING"
        ref.quality = "action required"
        return

    dimensions = parse_dimensions(ref.resolved_path)
    ref.dimensions = format_dimensions(dimensions)
    # This is only a filesystem/readability check. Do not call it PASS: that
    # wording was repeatedly misread as a visual crispness approval.
    ref.status = "PRESENT" if dimensions else "DECODE?"
    if ref.kind in {"navigation thumbnail", "homework/support"}:
        ref.quality = "reference checked; non-illustration asset"
    elif "-cropped" in ref.resolved_path.stem and not any(
        marker in ref.resolved_path.stem for marker in ("-crisp", "imagegen")
    ):
        ref.quality = "review required: crop-only reference"
    elif any(marker in ref.resolved_path.stem for marker in ("-crisp", "imagegen")):
        ref.quality = "review required: crisp/generated asset"
    else:
        ref.quality = "review required: native/source asset"


def collect_refs(units: list[Unit], repo: Path) -> list[ImageRef]:
    refs: list[ImageRef] = []
    for unit in units:
        if not unit.path.is_file():
            continue
        text = unit.path.read_text(encoding="utf-8")
        for line, target in image_targets(text):
            clean = clean_target(target)
            if not clean:
                continue
            ref = ImageRef(unit, line, clean)
            assess_reference(ref, repo)
            unit.refs.append(ref)
            refs.append(ref)
    return refs


def git_value(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return result.stdout.strip() or "(empty)"


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def short_path(path: Path, repo: Path) -> str:
    try:
        return path.relative_to(repo).as_posix()
    except ValueError:
        return path.as_posix()


def render_scope_summary(scope: ScopeSpec, repo: Path, units: list[Unit], refs: list[ImageRef]) -> str:
    instructional_units = sum(
        any(ref.kind == "instructional illustration" and ref.status in {"PRESENT", "DECODE?"} for ref in unit.refs)
        for unit in units
    )
    missing_units = len(units) - instructional_units
    local_refs = [ref for ref in refs if ref.kind != "remote"]
    missing_refs = sum(ref.status in {"MISSING", "OUTSIDE"} for ref in refs)
    review_refs = sum(
        ref.kind == "instructional illustration" and ref.status in {"PRESENT", "DECODE?"} for ref in refs
    )
    return (
        f"| {markdown_cell(scope.name)} | `{markdown_cell(scope.state)}` | {len(units)} | "
        f"{instructional_units} present / {missing_units} missing | {len(refs)} ({len(local_refs)} local) | "
        f"{review_refs} visual reviews required | {missing_refs} missing/outside |"
    )


def render_report(workspace_root: Path, output: Path, data: list[tuple[ScopeSpec, Path, list[Unit], list[ImageRef]]]) -> str:
    generated = dt.date.today().isoformat()
    command = (
        "python scripts/audit-illustrations/audit_illustrations.py "
        f"--workspace-root {workspace_root} --output {output}"
    )
    lines = [
        "# Current illustration audit",
        "",
        "> **Important:** This inventory is not a crispness approval. Every image row is unverified until an independent visual review records a pass in `docs/visual-review-evidence-2026-09-08.md`. A resolving file, pixel dimensions, or an `imagegen` filename is not evidence that the published pixels are crisp.",
        "",
        f"Generated on **{generated}** by the read-only audit script.",
        "",
        "This is a committed snapshot of the four current Zoomcamp scopes. The script reads the course repositories but does not modify them.",
        "",
        "## Source snapshots",
        "",
        "| Scope | Repository | HEAD | Worktree | Active selection |",
        "| --- | --- | --- | --- | --- |",
    ]
    for scope, repo, _, _ in data:
        head = git_value(repo, "rev-parse", "HEAD")
        dirty = git_value(repo, "status", "--porcelain")
        worktree = "clean" if dirty == "(empty)" else "dirty (snapshot still read-only)"
        lines.append(
            f"| {scope.name} | `{repo}` | `{head}` | {worktree} | {scope.selection} |"
        )
    lines.extend(
        [
            "",
            "## Status contract",
            "",
            "- `PRESENT` means the local Markdown target resolves and a basic raster/vector dimension check succeeded. It says nothing about crispness, fidelity, overlays, or whether the file is an upscale.",
            "- `MISSING`/`OUTSIDE` is an actionable broken reference; `REMOTE` is recorded but not locally checked; `DECODE?` needs an image decoder check.",
            "- `review required` is intentional: filesystem checks cannot prove crop direction/order, visual crispness at lesson size, text or semantic fidelity, or overlay removal. An independent reviewer must record the visual verdict before publishing.",
            "- Completed visual-review evidence is recorded in [`docs/visual-review-evidence-2026-09-08.md`](visual-review-evidence-2026-09-08.md); this scanner's queue remains conservative and is not a substitute for that evidence.",
            "- Thumbnail and homework/support assets are reference-checked but are not counted as instructional illustrations in the unit list.",
            "",
            "## Scope summary",
            "",
            "| Scope | State | Active units | Illustration coverage | Image references | Visual review queue | Broken refs |",
            "| --- | --- | ---: | --- | ---: | ---: | ---: |",
        ]
    )
    for scope, repo, units, refs in data:
        lines.append(render_scope_summary(scope, repo, units, refs))

    lines.extend(
        [
            "",
            "## Active units",
            "",
            "Every row is in the selected active scope. `YES` means at least one resolving local instructional illustration reference; navigation thumbnails and homework checklists do not satisfy that column.",
            "",
            "| Scope | Module | Unit | Unit file | Illustration present/missing | Instructional refs | All local/remote image refs |",
            "| --- | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for scope, repo, units, _ in data:
        for unit in units:
            instructional = [
                ref for ref in unit.refs if ref.kind == "instructional illustration" and ref.status in {"PRESENT", "DECODE?"}
            ]
            local_or_remote = [ref for ref in unit.refs if ref.kind != "homework/support"]
            presence = "YES" if instructional else "MISSING"
            lines.append(
                f"| {scope.name} | `{markdown_cell(unit.module)}` | {markdown_cell(unit.title)} | "
                f"`{short_path(unit.path, repo)}` | **{presence}** | {len(instructional)} | {len(local_or_remote)} |"
            )

    lines.extend(
        [
            "",
            "## Active illustration references and quality/check status",
            "",
            "This is the complete image-reference occurrence list for the selected unit files. Repeated references remain separate so the Markdown consumer is auditable.",
            "",
            "| Scope | Unit | Line | Markdown target | Kind | Check | Dimensions | Quality status |",
            "| --- | --- | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for scope, repo, _, refs in data:
        for ref in refs:
            lines.append(
                f"| {scope.name} | `{markdown_cell(short_path(ref.unit.path, repo))}` | {ref.line} | "
                f"`{markdown_cell(ref.target)}` | {ref.kind} | {ref.status} | {ref.dimensions} | {ref.quality} |"
            )

    all_refs = [ref for _, _, _, refs in data for ref in refs]
    missing = [ref for ref in all_refs if ref.status in {"MISSING", "OUTSIDE"}]
    cropped = [
        ref
        for ref in all_refs
        if ref.kind == "instructional illustration" and "crop-only" in ref.quality
    ]
    lines.extend(
        [
            "",
            "## Review handoff",
            "",
            f"- The machine-check snapshot contains {len(all_refs)} image-reference occurrences; {len(missing)} are missing or outside their repository.",
            f"- {len(cropped)} active instructional references are crop-only candidates and must be checked against their retained original source before acceptance.",
            "- The implementation agent must retain each original non-crisp source, crop only when it isolates useful content, merge adjacent screenshots on the content side in the correct orientation, and pass the original source image(s) plus any merged source reference to imagegen. A 2×/3× resized derivative must never be the only imagegen input.",
            "- The independent reviewer must inspect crop direction/order, visual crispness, text/semantic fidelity, overlays, and every Markdown reference, then record an explicit verdict in the rollout report.",
            "",
            f"Reproduce this snapshot with: `{command}`",
            "",
            "The selected DE scope is explicitly `published=false`; it is included because it is the current 2027 draft work scope, not because it is already live. Historical cohorts and unrelated course repositories are excluded.",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd().parent,
        help="directory containing the four sibling course repositories (default: parent of cwd)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="report path; may be inside zoomcamp-ops",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    workspace_root = args.workspace_root.resolve()
    data: list[tuple[ScopeSpec, Path, list[Unit], list[ImageRef]]] = []
    for scope in DEFAULT_SCOPE_SPECS:
        repo = workspace_root / scope.repository
        if not repo.is_dir():
            raise SystemExit(f"missing course repository for {scope.name}: {repo}")
        units = iter_units(scope, repo)
        refs = collect_refs(units, repo)
        data.append((scope, repo, units, refs))

    report = render_report(workspace_root, args.output, data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(
        "generated",
        args.output,
        "with",
        sum(len(units) for _, _, units, _ in data),
        "units and",
        sum(len(refs) for _, _, _, refs in data),
        "image references",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
