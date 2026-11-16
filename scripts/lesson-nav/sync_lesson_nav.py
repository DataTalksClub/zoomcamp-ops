#!/usr/bin/env python3
"""Write a GitHub-clickable prev/next block at the end of every lesson.

The lesson frontmatter (`prev_url`, `next_url`) stays the single source of
truth. GitHub renders frontmatter as a plain table, so this script mirrors it
into a marked block at the end of the body:

    <!-- nav:start -->
    [← Previous: <title>](<prev_url>) · [Next: <title> →](<next_url>)
    <!-- nav:end -->

The website strips everything between the markers, and the checker exempts
it from U008. Re-run the script whenever the frontmatter changes.

Usage:
    python sync_lesson_nav.py REPO_DIR            # rewrite files
    python sync_lesson_nav.py REPO_DIR --check    # exit 1 if any file is stale
"""

import argparse
import re
import sys
from pathlib import Path

IGNORED_DIRS = {".git", ".github", ".venv", "venv", "__pycache__", "node_modules", ".tmp"}
START, END = "<!-- nav:start -->", "<!-- nav:end -->"
BLOCK = re.compile(r"\n*<!-- nav:start -->.*?<!-- nav:end -->\n*", re.DOTALL)
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
KEY = re.compile(r"^(prev_url|next_url):\s*(.*?)\s*$", re.MULTILINE)


def frontmatter_links(text):
    match = FRONTMATTER.match(text)
    if not match:
        return {}
    links = {}
    for key, value in KEY.findall(match.group(1)):
        value = value.strip("\"'")
        if value:
            links[key] = value
    return links


def title_of(path):
    text = path.read_text(encoding="utf-8")
    body = FRONTMATTER.sub("", text, count=1)
    in_code = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_code = not in_code
        elif not in_code and line.startswith("# "):
            return line[2:].strip()
    return path.stem


def nav_block(path, links):
    parts = []
    for key, label in (("prev_url", "← Previous: {}"), ("next_url", "Next: {} →")):
        url = links.get(key)
        if not url:
            continue
        target = (path.parent / url.split("#")[0]).resolve()
        title = title_of(target) if target.is_file() else Path(url).stem
        text = label.format(title)
        parts.append(f"[{text}]({url})")
    return f"{START}\n" + " · ".join(parts) + f"\n{END}\n"


def sync(path):
    raw = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")
    links = frontmatter_links(text)
    if not links and START not in text:
        return raw, raw
    body = BLOCK.sub("\n", text).rstrip("\n") + "\n"
    if links:
        body = body + "\n" + nav_block(path, links)
    new = body.replace("\n", newline)
    return raw, new


def lesson_files(root):
    for path in sorted(root.rglob("*.md")):
        if not IGNORED_DIRS.intersection(path.relative_to(root).parts):
            yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("repo", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.repo.resolve()
    stale = []
    for path in lesson_files(root):
        raw, new = sync(path)
        if raw == new:
            continue
        stale.append(path.relative_to(root))
        if not args.check:
            path.write_bytes(new.encode("utf-8"))

    for rel in stale:
        print(rel)
    if args.check and stale:
        print(f"{len(stale)} lesson(s) have a stale nav block", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
