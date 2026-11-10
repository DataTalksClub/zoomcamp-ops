#!/usr/bin/env python3
"""Join CMP submissions to identity evidence per author (CMP student id).

Evidence hierarchy (strongest first), see README.md:
  1. self_submitted_linkedin  - a linkedin.com/in/<id> or /posts/<id>_ URL the student submitted in CMP
  2. github_declared_linkedin - a LinkedIn URL on the author's own GitHub profile (social accounts/blog/bio)
  3. domain_signal            - corporate email domain (company signal only, not an identity link)
  4. public_match             - a candidate found by search/Treg by GitHub handle; needs corroboration
Emails never leave memory: only the domain is cached.
"""
from collections import defaultdict, Counter
import json
import re
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, unquote

from scan import repo_name

FREE_DOMAINS = {
    'gmail.com', 'googlemail.com', 'outlook.com', 'hotmail.com', 'live.com', 'msn.com', 'yahoo.com', 'ymail.com',
    'icloud.com', 'me.com', 'mac.com', 'aol.com', 'proton.me', 'protonmail.com', 'pm.me', 'gmx.de', 'gmx.net', 'gmx.com',
    'web.de', 'mail.ru', 'yandex.ru', 'yandex.com', 'ya.ru', 'qq.com', '163.com', '126.com', 'naver.com', 'hanmail.net',
    'zoho.com', 'tutanota.com', 'tuta.io', 'fastmail.com', 'hey.com', 'duck.com', 'mail.com', 'rocketmail.com',
    'hotmail.co.uk', 'yahoo.co.uk', 'yahoo.fr', 'hotmail.fr', 'outlook.fr', 'laposte.net', 'orange.fr', 'free.fr',
    'libero.it', 'yahoo.es', 'hotmail.es', 'outlook.es', 'yahoo.com.br', 'bol.com.br', 'uol.com.br', 'rediffmail.com',
    'yahoo.in', 'yahoo.co.in', 'outlook.in', 't-online.de', 'posteo.de', 'seznam.cz', 'wp.pl', 'o2.pl', 'interia.pl',
    'ukr.net', 'bk.ru', 'inbox.ru', 'list.ru', 'rambler.ru', 'sina.com', 'foxmail.com', 'live.co.uk', 'btinternet.com',
    'comcast.net', 'verizon.net', 'att.net', 'sbcglobal.net', 'cox.net', 'shaw.ca', 'rogers.com', 'bigpond.com',
    'optusnet.com.au', 'telus.net', 'yahoo.ca', 'hotmail.ca', 'live.ca', 'outlook.de', 'hotmail.de', 'yahoo.de',
    'hotmail.it', 'outlook.it', 'live.it', 'live.fr', 'skynet.be', 'telenet.be', 'ziggo.nl', 'kpnmail.nl', 'xs4all.nl',
    'bluewin.ch', 'gmx.ch', 'gmx.at', 'aon.at', 'chello.at', 'abv.bg', 'yahoo.gr', 'otenet.gr', 'mail.bg', 'yahoo.co.jp',
    'privaterelay.appleid.com', 'users.noreply.github.com', 'cloud.com', 'email.com', 'usa.com', 'yahoo.com.sg', 'yahoo.com.ph',
}
ACADEMIC_RE = re.compile(r'(\.edu(\.[a-z]{2})?$|\.ac\.[a-z]{2}$|(^|\.)uni-[\w-]+\.de$|(^|\.)(student|students|alumni|stud|etu|estudiante|alumnos)\.|university|univ|\.edu\.|tu-\w+\.de$|ethz\.ch$|epfl\.ch$)', re.I)
LI_IN = re.compile(r'linkedin\.com/in/([A-Za-z0-9\-_%]+)', re.I)
LI_POST = re.compile(r'linkedin\.com/posts/([A-Za-z0-9\-%]+)_', re.I)
X_RE = re.compile(r'(?:twitter|x)\.com/([A-Za-z0-9_]{1,15})/status', re.I)


def domain_kind(domain):
    if not domain:
        return ''
    if domain in FREE_DOMAINS or re.match(r'^(yahoo|hotmail|outlook|live|gmail)\.', domain):
        return 'free'
    if ACADEMIC_RE.search(domain):
        return 'academic'
    return 'corporate'


def linkedin_ids(links):
    ids = Counter()
    for link in links or []:
        s = unquote(str(link))
        for rx in (LI_IN, LI_POST):
            for m in rx.finditer(s):
                v = m.group(1).strip('-').lower()
                if v and v not in ('feed', 'company', 'pulse', 'share'):
                    ids[v] += 1
    return ids


def x_ids(links):
    return Counter(m.group(1).lower() for link in links or [] for m in X_RE.finditer(str(link)))


def gh_json(path):
    p = subprocess.run(['gh', 'api', path], capture_output=True, text=True, timeout=60)
    if p.returncode:
        return {'_error': (p.stderr or '')[:200]}
    return json.loads(p.stdout)


def github_profile(cache, handle):
    dest = cache / f'gh-user-{handle.lower()}.json'
    if dest.exists():
        return json.loads(dest.read_text())
    user = gh_json(f'users/{handle}')
    keep = {k: user.get(k) for k in ('login', 'type', 'name', 'company', 'blog', 'location', 'bio', 'twitter_username',
                                      'hireable', 'created_at', 'public_repos', 'followers')} if '_error' not in user else user
    social = gh_json(f'users/{handle}/social_accounts') if '_error' not in user else []
    keep['social'] = [s.get('url') for s in social] if isinstance(social, list) else []
    dest.write_text(json.dumps(keep))
    return keep


def personal_site_links(cache, url):
    """Public personal site (GitHub blog field): look for a LinkedIn profile link."""
    if not url or 'linkedin.com' in url or 'github.com' in url:
        return []
    url = url if url.startswith('http') else 'https://' + url
    key = re.sub(r'[^\w.-]', '_', url)[:150]
    dest = cache / f'site-{key}.txt'
    if not dest.exists():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 dtc-course-audience'})
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read(800_000).decode('utf-8', errors='replace')
            dest.write_text(' '.join(sorted(set(m.group(0) for m in LI_IN.finditer(body)))))
        except Exception:
            dest.write_text('')
    return linkedin_ids([dest.read_text()])


def commit_name(cache, repo, handle):
    """Most common human commit-author name in the submitted repo (public). Email never stored."""
    dest = cache / f"commit-names-{repo.replace('/', '__').lower()}.json"
    if dest.exists():
        return json.loads(dest.read_text())
    p = subprocess.run(['gh', 'api', f'repos/{repo}/commits?per_page=100', '--jq',
                        '[.[] | {n: .commit.author.name, d: (.commit.author.email | split("@") | .[1])}]'],
                       capture_output=True, text=True, timeout=60)
    if p.returncode:
        return None  # not cached: rate limit or access failure, retry on the next run
    rows = json.loads(p.stdout or '[]')
    names = Counter(r['n'] for r in rows if r.get('n') and r['n'].lower() not in (handle.lower(), 'github', 'github actions'))
    doms = Counter(r['d'] for r in rows if r.get('d') and domain_kind(r['d']) == 'corporate')
    res = {'name': names.most_common(1)[0][0] if names else '', 'corporate_domain': doms.most_common(1)[0][0] if doms else ''}
    dest.write_text(json.dumps(res))
    return res


def build(output, workers=8):
    cache = output / 'cache'
    cmp_prof = {}
    for p in cache.glob('cmp-profiles-*.json'):
        cmp_prof.update({int(k): v for k, v in json.loads(p.read_text()).items()})
    authors = defaultdict(lambda: {'years': set(), 'repos': set(), 'handles': Counter(), 'hw_handles': Counter(),
                                   'domains': Counter(), 'li': Counter(), 'x': Counter(), 'hw_submitted': set()})
    for p in sorted(cache.glob('submissions-*.json')):
        year = p.stem.split('-')[1]
        for r in json.loads(p.read_text())['submissions']:
            a = authors[r['student_id']]
            a['years'].add(year)
            repo = repo_name(r.get('github_link'))
            if repo:
                a['repos'].add(f'{year}:{repo}')
                a['handles'][repo.split('/')[0]] += 1
            if r.get('email_domain'):
                a['domains'][r['email_domain']] += 1
            a['li'].update(linkedin_ids(r.get('learning_in_public_links')))
            a['x'].update(x_ids(r.get('learning_in_public_links')))
    for p in sorted(cache.glob('homework-*.json')):
        _, year, slug = p.stem.split('-', 2)
        for r in json.loads(p.read_text())['submissions']:
            if r['student_id'] not in authors:
                continue
            a = authors[r['student_id']]
            a['hw_submitted'].add(f'{year}:{slug}')
            a['li'].update(linkedin_ids(r.get('learning_in_public_links')))
            a['x'].update(x_ids(r.get('learning_in_public_links')))
            repo = repo_name(r.get('homework_link'))
            if repo:
                a['hw_handles'][repo.split('/')[0]] += 1
    handles = sorted({h for a in authors.values() for h in a['handles']} | {h for a in authors.values() for h in a['hw_handles']})
    with ThreadPoolExecutor(max_workers=workers) as pool:
        profiles = dict(zip(handles, pool.map(lambda h: github_profile(cache, h), handles)))
    out = []
    for sid, a in sorted(authors.items()):
        handle = a['handles'].most_common(1)[0][0] if a['handles'] else (a['hw_handles'].most_common(1)[0][0] if a['hw_handles'] else '')
        prof = profiles.get(handle, {}) if handle else {}
        gh_li = Counter()
        for s in (prof.get('social') or []) + [prof.get('blog') or '', prof.get('bio') or '']:
            gh_li.update(linkedin_ids([s]))
        site_li = personal_site_links(cache, prof.get('blog') or '') if not gh_li else []
        cp = cmp_prof.get(sid, {})
        cmp_li = linkedin_ids([cp.get('profile', {}).get('linkedin', '')])
        self_li = [k for k, _ in (cmp_li + a['li']).most_common()]
        domain = a['domains'].most_common(1)[0][0] if a['domains'] else ''
        cn = None
        # CMP assigns random "adjective scientist" display names (e.g. "Adoring Gould") unless the student
        # opted into a public profile, so a display name only counts as a real name with a public profile.
        cmp_name = cp.get('display_name', '') if cp.get('profile') else ''
        if handle and not (prof.get('name') or cmp_name) and not (self_li or gh_li) and a['repos']:
            cn = commit_name(cache, sorted(a['repos'])[-1].split(':', 1)[1], handle)
        out.append({
            'student_id': sid, 'years': sorted(a['years']), 'repos': sorted(a['repos']), 'github': handle,
            'github_other': sorted(set(a['handles']) | set(a['hw_handles']) - {handle}),
            'github_profile': prof, 'self_submitted_linkedin': self_li,
            'self_submitted_linkedin_source': 'cmp_profile' if cmp_li else ('cmp_learning_in_public' if a['li'] else ''),
            'github_declared_linkedin': [k for k, _ in gh_li.most_common()] + [k for k in site_li if k not in gh_li],
            'github_declared_linkedin_source': 'github_profile' if gh_li else ('personal_site' if site_li else ''),
            'cmp_display_name': cmp_name, 'cmp_about_me': cp.get('about_me', ''),
            'cmp_website': cp.get('profile', {}).get('globe', ''), 'x_handles': [k for k, _ in a['x'].most_common()],
            'email_domain': domain if domain_kind(domain) != 'free' else '', 'email_domain_kind': domain_kind(domain),
            'homeworks': sorted(a['hw_submitted']),
            'commit_name': (cn or {}).get('name', ''), 'commit_corporate_domain': (cn or {}).get('corporate_domain', ''),
        })
    dest = cache / 'authors.json'
    dest.write_text(json.dumps(out))
    dest.chmod(0o600)
    stats = {'authors': len(out), 'by_year': {y: sum(y in r['years'] for r in out) for y in sorted({y for r in out for y in r['years']})},
             'with_github': sum(bool(r['github']) for r in out),
             'github_profile_ok': sum(bool(r['github_profile']) and '_error' not in r['github_profile'] for r in out),
             'github_org_owner': sum(r['github_profile'].get('type') == 'Organization' for r in out),
             'self_submitted_linkedin': sum(bool(r['self_submitted_linkedin']) for r in out),
             'github_declared_linkedin': sum(bool(r['github_declared_linkedin']) for r in out),
             'any_linkedin': sum(bool(r['self_submitted_linkedin'] or r['github_declared_linkedin']) for r in out),
             'domain_kind': dict(Counter(r['email_domain_kind'] for r in out)),
             'github_company': sum(bool((r['github_profile'] or {}).get('company')) for r in out)}
    (output / 'identity-stats.json').write_text(json.dumps(stats, indent=2))
    return stats
