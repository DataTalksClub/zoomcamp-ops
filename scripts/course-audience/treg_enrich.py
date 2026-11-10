#!/usr/bin/env python3
"""Paid enrichment steps (Treg), run only after public sources and only for authors who need them.

linkedin_profiles: read a full LinkedIn profile for every author with a CONFIRMED LinkedIn id
                   (self-submitted in CMP, or declared on their own GitHub/personal site).
name_search:       for authors with a real name but no LinkedIn link and no public employer,
                   search LinkedIn by first/last name; candidates need corroboration (classify.py).
"""
from concurrent.futures import ThreadPoolExecutor
import json
import re
import unicodedata

from treg_budget import Ledger, BudgetExceeded

FULL = 'anyapi.linkedin.user.profile.full'
FULL_USD = 0.0042
SEARCH = 'crawl4ai.linkedin.search.people'
SEARCH_USD = 0.0036
FIELDS = 'found,data.name,data.headline,data.location,data.city,data.country,data.countryCode,data.currentPosition,data.experience,data.education,data.certifications,data.publicIdentifier,data.openToWork,data.about'


def load_authors(output):
    return json.loads((output / 'cache' / 'authors.json').read_text())


def _run(ledger, jobs, workers):
    done, stopped = 0, ''
    def one(job):
        nonlocal done, stopped
        dest, tool, body, reserve, label, query = job
        if dest.exists() or stopped:
            return
        try:
            res = ledger.call(tool, body, reserve, label, query)
        except BudgetExceeded as e:
            stopped = str(e)
            return
        dest.write_text(json.dumps(res))
        dest.chmod(0o600)
        done += 1
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(one, jobs))
    return done, stopped


def linkedin_profiles(output, cap_usd, stop_usd, limit=0, dry_run=False, workers=6):
    ledger = Ledger(output, cap_usd, stop_usd)
    jobs, seen = [], set()
    for a in load_authors(output):
        ids = a['self_submitted_linkedin'] or a['github_declared_linkedin']
        if not ids or ids[0] in seen:
            continue
        seen.add(ids[0])
        dest = output / 'cache' / f'li-full-{ids[0]}.json'
        if not dest.exists():
            jobs.append((dest, FULL, {'url': f'https://www.linkedin.com/in/{ids[0]}'}, FULL_USD, 'li-full:' + ids[0], None))
    if limit:
        jobs = jobs[:limit]
    estimate = len(jobs) * FULL_USD
    info = {'pending_lookups': len(jobs), 'estimate_usd_max': round(estimate, 4), 'spent_usd': ledger.spent() / 1e6, 'stop_usd': stop_usd}
    if dry_run:
        return info
    done, stopped = _run(ledger, jobs, workers)
    return info | {'done': done, 'stopped': stopped, 'spent_usd_after': ledger.spent() / 1e6}


def split_name(name):
    name = re.sub(r'\(.*?\)|[|,].*$', '', name or '').strip()
    parts = [p for p in re.split(r'\s+', name) if re.search(r'[^\W\d_]', p)]
    if len(parts) < 2 or any(len(p) < 2 for p in (parts[0], parts[-1])):
        return None
    return parts[0], parts[-1]


def name_candidates_needed(a):
    prof = a.get('github_profile') or {}
    if a['self_submitted_linkedin'] or a['github_declared_linkedin']:
        return None
    return split_name(prof.get('name') or a.get('cmp_display_name') or a.get('commit_name') or '')


def github_to_linkedin(output, cap_usd, stop_usd, limit=0, dry_run=False, workers=4):
    """Name search for authors without any LinkedIn link (kept under this CLI name for symmetry)."""
    ledger = Ledger(output, cap_usd, stop_usd)
    jobs = []
    for a in load_authors(output):
        nm = name_candidates_needed(a)
        if not nm:
            continue
        key = search_key(nm)
        dest = output / 'cache' / f'li-search-{key}.json'
        if not dest.exists() and key:
            jobs.append((dest, SEARCH, {'first_name': nm[0], 'last_name': nm[1], 'limit': 10}, SEARCH_USD, 'li-search:' + key, None))
    uniq = {j[0]: j for j in jobs}
    jobs = list(uniq.values())[: limit or None]
    info = {'pending_searches': len(jobs), 'estimate_usd_max': round(len(jobs) * SEARCH_USD, 4), 'spent_usd': ledger.spent() / 1e6, 'stop_usd': stop_usd}
    if dry_run:
        return info
    done, stopped = _run(ledger, jobs, workers)
    return info | {'done': done, 'stopped': stopped, 'spent_usd_after': ledger.spent() / 1e6}


def search_key(nm):
    return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', ' '.join(nm)).encode('ascii', 'ignore').decode().lower()).strip('-')


def search_rows(result):
    if not isinstance(result, dict):
        return []
    rows = result.get('rows') or result.get('data') or result.get('results') or []
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def profile_slug(value):
    """Keep the public identifier, dropping search-provider language suffixes."""
    slug = str(value or '').strip('/').split('/', 1)[0].lower()
    return slug if re.fullmatch(r'(?:[\w-]|%[0-9a-f]{2})+', slug) else ''


def candidate_slugs(output, a, max_per_author=2):
    """Name-matching candidates from the name search, location-matching first."""
    from classify import name_tokens, country_of
    nm = name_candidates_needed(a)
    if not nm:
        return []
    p = output / 'cache' / f'li-search-{search_key(nm)}.json'
    if not p.exists():
        return []
    want = name_tokens(' '.join(nm))
    gh_country = country_of((a.get('github_profile') or {}).get('location') or '')
    rows = [r for r in search_rows(json.loads(p.read_text() or 'null')) if r.get('profile_id') and want <= name_tokens(r.get('name') or '')]
    rows.sort(key=lambda r: (not (gh_country and country_of(r.get('location') or '') == gh_country),))
    slugs = dict.fromkeys(profile_slug(r['profile_id']) for r in rows)
    return [s for s in slugs if s][:max_per_author]


def candidate_profiles(output, cap_usd, stop_usd, limit=0, dry_run=False, workers=6):
    ledger = Ledger(output, cap_usd, stop_usd)
    slugs = []
    for a in load_authors(output):
        slugs += candidate_slugs(output, a)
    rp = output / 'rechecks.json'
    if rp.exists():
        slugs += [v['candidate_linkedin'] for v in json.loads(rp.read_text()).values() if v['status'] == 'confirmed' and v.get('candidate_linkedin')]
    jobs = []
    for s in dict.fromkeys(slugs):
        dest = output / 'cache' / f'li-full-{s}.json'
        if not dest.exists():
            jobs.append((dest, FULL, {'url': f'https://www.linkedin.com/in/{s}'}, FULL_USD, 'li-candidate:' + s, None))
    jobs = jobs[: limit or None]
    info = {'pending_candidate_reads': len(jobs), 'estimate_usd_max': round(len(jobs) * FULL_USD, 4), 'spent_usd': ledger.spent() / 1e6, 'stop_usd': stop_usd}
    if dry_run:
        return info
    done, stopped = _run(ledger, jobs, workers)
    return info | {'done': done, 'stopped': stopped, 'spent_usd_after': ledger.spent() / 1e6}
