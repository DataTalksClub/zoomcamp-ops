#!/usr/bin/env python3
"""Fetch a YouTube transcript through Oxylabs, retrying with fresh sticky sessions.

Usage: fetch-transcript.py <video-id> [more-ids...]
Caches to ~/.cache/youtube_transcripts/<id>.txt like the standard tool.
"""
import random
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

creds = {}
for line in Path("/home/alexey/.config/youtube/.env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        creds[k] = v


def proxy_url(sid):
    user = creds["OXYLABS_USER"]
    ep = creds["OXYLABS_ENDPOINT"]
    pw = quote(creds["OXYLABS_PASSWORD"], safe="")
    return f"http://customer-{user}-sessid-{sid}:{pw}@{ep}"


def fetch(vid, attempts=12):
    cache = Path.home() / ".cache" / "youtube_transcripts" / f"{vid}.txt"
    if cache.exists():
        print(f"{vid}: cached at {cache}")
        return
    for i in range(attempts):
        sid = f"{random.randint(0, 10**8):08d}"
        url = proxy_url(sid)
        try:
            api = YouTubeTranscriptApi(
                proxy_config=GenericProxyConfig(http_url=url, https_url=url)
            )
            t = api.fetch(vid)
            lines = []
            for e in t:
                s = int(e.start)
                h, rem = divmod(s, 3600)
                m, sec = divmod(rem, 60)
                ts = f"{h}:{m:02}:{sec:02}" if h else f"{m}:{sec:02}"
                lines.append(ts + " " + e.text.replace("\n", " "))
            cache.write_text("\n".join(lines), encoding="utf-8")
            print(f"{vid}: OK ({len(lines)} lines) sid={sid}")
            return
        except Exception as e:
            print(f"{vid}: attempt {i + 1} sid={sid} failed: {type(e).__name__}")
            time.sleep(2)
    raise SystemExit(f"{vid}: all attempts failed")


for vid in sys.argv[1:]:
    fetch(vid)
