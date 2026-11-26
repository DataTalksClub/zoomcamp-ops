#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6", "yt-dlp>=2025.1.1"]
# ///
"""Record each lesson video's length in the lesson frontmatter.

A schema-2 course repository lists its lessons in ``<module>/module.yaml``.
For every lesson whose frontmatter has a YouTube ``video_url``, this script
asks YouTube for the video's length and writes it next to the URL:

    ---
    video_url: "https://www.youtube.com/watch?v=rQYyFxf1FWw"
    video_duration_seconds: 208
    ---

The website's curriculum importer reads ``video_duration_seconds`` into the
lesson row, so the module page can show lesson lengths without calling YouTube
at request time. The value is fetched, never typed by hand: re-run the script
after adding or replacing a lesson video.

Where the length comes from, in order:

1. The YouTube Data API (``videos.list``, ``contentDetails.duration``) when
   ``YOUTUBE_API_KEY`` is set. One request per 50 videos.
2. Otherwise ``yt-dlp`` (mobile web client). YouTube often answers a
   datacenter IP with a bot check, so the script routes yt-dlp through the
   same residential proxy the fetch-youtube skill uses when its credentials
   are present (``DATAIMPULSE_*`` or ``OXYLABS_*``, read from the environment
   or from ``--env-file``, default ``~/.config/youtube/.env``). The proxy URL
   is built in memory and never printed.

Usage:
    uv run fill_video_durations.py REPO_DIR             # fill missing lengths
    uv run fill_video_durations.py REPO_DIR --refresh   # refetch every length
    uv run fill_video_durations.py REPO_DIR --check     # exit 1 if any is missing
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

KEY = "video_duration_seconds"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
VIDEO_URL_LINE = re.compile(r"^video_url:.*$", re.MULTILINE)
DURATION_LINE = re.compile(rf"^{KEY}:.*\n?", re.MULTILINE)
ISO_DURATION = re.compile(r"^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$")


def video_id(url: str) -> str | None:
    parts = urllib.parse.urlsplit(url)
    host = (parts.hostname or "").lower()
    if host == "youtu.be":
        return parts.path.strip("/").split("/")[0] or None
    if host.endswith("youtube.com"):
        query = urllib.parse.parse_qs(parts.query)
        if query.get("v"):
            return query["v"][0]
        segments = [s for s in parts.path.split("/") if s]
        if len(segments) >= 2 and segments[0] in {"live", "embed", "shorts", "v"}:
            return segments[1]
    return None


def lessons(repo: Path):
    """Yield (path, frontmatter mapping) for every lesson module.yaml lists."""
    for manifest in sorted(repo.glob("*/module.yaml")):
        data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        for unit in data.get("units") or []:
            path = manifest.parent / unit["path"]
            text = path.read_text(encoding="utf-8")
            match = FRONTMATTER.match(text)
            mapping = (yaml.safe_load(match.group(1)) or {}) if match else {}
            yield path, mapping


def load_env_file(path: Path) -> None:
    """Load KEY=VALUE lines without overriding variables already exported."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip("'\""))


def proxy_url() -> str | None:
    quote = urllib.parse.quote
    user, password = os.environ.get("DATAIMPULSE_USER"), os.environ.get("DATAIMPULSE_PASSWORD")
    if user and password:
        endpoint = os.environ.get("DATAIMPULSE_ENDPOINT") or "{}:{}".format(
            os.environ.get("DATAIMPULSE_HOST", "gw.dataimpulse.com"),
            os.environ.get("DATAIMPULSE_PORT", "823"),
        )
        endpoint = endpoint.removeprefix("http://").removeprefix("https://").rstrip("/")
        return f"http://{quote(user, safe='')}:{quote(password, safe='')}@{endpoint}"
    user, password = os.environ.get("OXYLABS_USER"), os.environ.get("OXYLABS_PASSWORD")
    endpoint = os.environ.get("OXYLABS_ENDPOINT")
    if user and password and endpoint:
        return f"http://customer-{user}:{quote(password, safe='')}@{endpoint}"
    return None


def iso_seconds(value: str) -> int | None:
    match = ISO_DURATION.match(value or "")
    if not match:
        return None
    days, hours, minutes, seconds = (int(group or 0) for group in match.groups())
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


def durations_from_api(ids: list[str], api_key: str) -> dict[str, int]:
    found: dict[str, int] = {}
    for start in range(0, len(ids), 50):
        query = urllib.parse.urlencode(
            {"part": "contentDetails", "id": ",".join(ids[start : start + 50]), "key": api_key}
        )
        url = f"https://www.googleapis.com/youtube/v3/videos?{query}"
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = json.load(response)
        for item in payload.get("items", []):
            seconds = iso_seconds(item.get("contentDetails", {}).get("duration", ""))
            if seconds:
                found[item["id"]] = seconds
    return found


class _SilentLogger:
    """yt-dlp prints every failed attempt; the script reports failures itself."""

    def debug(self, message: str) -> None:
        pass

    info = warning = error = debug


def durations_from_ytdlp(ids: list[str], attempts: int = 6) -> dict[str, int]:
    import yt_dlp

    options = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
        "logger": _SilentLogger(),
        "extractor_args": {"youtube": {"player_client": ["mweb"]}},
    }
    proxy = proxy_url()
    if proxy:
        options["proxy"] = proxy
    found: dict[str, int] = {}
    with yt_dlp.YoutubeDL(options) as client:
        for index, vid in enumerate(ids, start=1):
            message = "no duration in the response"
            # A rotating proxy hands out a new exit IP per request, so a bot
            # check on one attempt is usually gone on the next.
            for _attempt in range(attempts):
                try:
                    info = client.extract_info(
                        f"https://www.youtube.com/watch?v={vid}", download=False, process=False
                    )
                except Exception as error:  # noqa: BLE001 - report and retry
                    message = str(error).splitlines()[0][:160]
                    continue
                if info and info.get("duration"):
                    found[vid] = int(info["duration"])
                    break
            else:
                print(f"  {vid}: no duration ({message})", file=sys.stderr)
            print(f"  fetched {index}/{len(ids)}", file=sys.stderr, end="\r")
    print(file=sys.stderr)
    return found


def write_duration(path: Path, seconds: int) -> bool:
    raw = path.read_bytes().decode("utf-8")
    newline = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")
    match = FRONTMATTER.match(text)
    block = match.group(1)
    block = DURATION_LINE.sub("", block)
    url_line = VIDEO_URL_LINE.search(block)
    line = f"{KEY}: {seconds}"
    block = block[: url_line.end()] + "\n" + line + block[url_line.end() :]
    new = "---\n" + block.rstrip("\n") + "\n---\n" + text[match.end() :]
    new = new.replace("\n", newline)
    if new == raw:
        return False
    path.write_bytes(new.encode("utf-8"))
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("repo", type=Path, help="course repository root")
    parser.add_argument("--refresh", action="store_true", help="refetch lengths already recorded")
    parser.add_argument("--check", action="store_true", help="only report missing lengths")
    parser.add_argument(
        "--env-file",
        type=Path,
        default=Path.home() / ".config" / "youtube" / ".env",
        help="optional KEY=VALUE file with YOUTUBE_API_KEY or proxy credentials",
    )
    args = parser.parse_args()

    todo: list[tuple[Path, str]] = []
    missing: list[str] = []
    for path, mapping in lessons(args.repo):
        url = mapping.get("video_url")
        if not url:
            continue
        vid = video_id(str(url))
        if vid is None:
            print(f"{path}: cannot read a video id from {url}", file=sys.stderr)
            continue
        recorded = mapping.get(KEY)
        if isinstance(recorded, int) and recorded > 0 and not args.refresh:
            continue
        missing.append(str(path.relative_to(args.repo)))
        todo.append((path, vid))

    if args.check:
        for rel in missing:
            print(f"missing {KEY}: {rel}")
        return 1 if missing else 0
    if not todo:
        print("every lesson video already has a length")
        return 0

    load_env_file(args.env_file)
    ids = sorted({vid for _path, vid in todo})
    api_key = os.environ.get("YOUTUBE_API_KEY")
    found = durations_from_api(ids, api_key) if api_key else durations_from_ytdlp(ids)

    changed = failed = 0
    for path, vid in todo:
        seconds = found.get(vid)
        if not seconds:
            failed += 1
            print(f"no length for {path.relative_to(args.repo)} ({vid})", file=sys.stderr)
            continue
        changed += write_duration(path, seconds)
    print(f"{len(todo)} lessons to fill, {changed} updated, {failed} without a length")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
