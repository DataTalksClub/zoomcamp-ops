#!/usr/bin/env python3
"""Read opt-in public CMP profile links (GitHub, LinkedIn, website, about me) from public
leaderboard breakdown pages, and join them to project authors by submitted repository URL.

Only enrollments that chose `display_public_profile` expose these links. Pages are public
and cached by CMP; crawl politely (low concurrency) and stop once pages no longer join.
"""
from concurrent.futures import ThreadPoolExecutor
import html
import json
import re
import time
import urllib.request

from scan import repo_name

SITE = 'https://courses.datatalks.club'


def get(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'dtc-course-audience/1.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception:
            time.sleep(3 * (attempt + 1))
    return ''


def parse_breakdown(page):
    head = page.split('leaderboard-flag-button', 1)[0]
    name = re.search(r'<h1[^>]*>(.*?)</h1>', head, re.S)
    about = re.search(r'<strong>About me:</strong>(.*?)</p>', head, re.S)
    socials = re.findall(r'<a href="([^"]+)" target="_blank" class="app-muted app-link">\s*<i class="fa[bs] fa-(github|linkedin|globe) social-icon', head)
    links = re.findall(r'href="(https://(?:www\.)?github\.com/[^"]+)"', page)
    return {'display_name': html.unescape(name.group(1).strip()) if name else '',
            'about_me': html.unescape(' '.join(about.group(1).split()))[:500] if about else '',
            'profile': {kind: html.unescape(url) for url, kind in socials},
            'repos': sorted({repo_name(html.unescape(u)).lower() for u in links if repo_name(html.unescape(u))})}


def crawl(output, course, years, workers=4, max_pages=60):
    cache = output / 'cache'
    authors_repos = {}
    for p in cache.glob('submissions-*.json'):
        year = p.stem.split('-')[1]
        for r in json.loads(p.read_text())['submissions']:
            repo = repo_name(r.get('github_link'))
            if repo:
                authors_repos[(year, repo.lower())] = r['student_id']
    joined = {}
    for year in years:
        slug = f'{course}-{year}'
        dest = cache / f'cmp-profiles-{year}.json'
        if dest.exists():
            joined.update({int(k): v for k, v in json.loads(dest.read_text()).items()})
            continue
        found, misses, page_no = {}, 0, 1
        while page_no <= max_pages and misses < 3:
            listing = get(f'{SITE}/{slug}/leaderboard?page={page_no}')
            ids = sorted(set(re.findall(rf'/{slug}/leaderboard/(\d+)/', listing)))
            if not ids:
                break
            with ThreadPoolExecutor(max_workers=workers) as pool:
                pages = list(pool.map(lambda i: get(f'{SITE}/{slug}/leaderboard/{i}/'), ids))
            hits = 0
            for page in pages:
                info = parse_breakdown(page)
                sids = {authors_repos[(year, r)] for r in info['repos'] if (year, r) in authors_repos}
                if len(sids) == 1:
                    hits += 1
                    found[sids.pop()] = {k: info[k] for k in ('display_name', 'about_me', 'profile')}
            misses = misses + 1 if hits == 0 else 0
            page_no += 1
        dest.write_text(json.dumps(found))
        dest.chmod(0o600)
        joined.update(found)
    return joined
