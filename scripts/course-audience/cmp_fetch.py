#!/usr/bin/env python3
"""Fetch CMP project and homework exports for one course family and a set of years.

Only identifiers, links, commits, scores and learning-in-public links are kept.
Student emails are reduced to their domain in memory (domain_signal) and the
full address is never written anywhere.
"""
import json
import os
import re
import urllib.request

BASE = os.environ.get('CMP_BASE', 'https://courses.datatalks.club/api')
FINAL_RE = re.compile(r'project|capstone|final', re.I)
PROJECT_KEEP = ('id', 'student_id', 'github_link', 'commit_id', 'project_score', 'total_score',
                'passed', 'learning_in_public_links')
HOMEWORK_KEEP = ('student_id', 'homework_link', 'learning_in_public_links', 'total_score')


def cmp_get(path):
    req = urllib.request.Request(BASE + path, headers={'Authorization': 'Token ' + os.environ['AUTH_TOKEN']})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def email_domain(email):
    """Return only the lower-cased domain part; never the local part."""
    if not email or '@' not in str(email):
        return ''
    return str(email).rsplit('@', 1)[1].strip().lower()


def write_private(path, data):
    path.write_text(json.dumps(data))
    path.chmod(0o600)


def fetch(output, course, years, include_midterms=False):
    cache = output / 'cache'
    cache.mkdir(parents=True, exist_ok=True)
    cache.chmod(0o700)
    summary = {}
    for year in years:
        slug = f'{course}-{year}'
        meta = cmp_get(f'/courses/{slug}/')
        write_private(cache / f'course-{year}.json', meta)
        summary[year] = {'projects': {}, 'homeworks': {}}
        for project in meta.get('projects', []):
            title = project.get('title', '') + ' ' + project['slug']
            if not FINAL_RE.search(title) and not include_midterms:
                continue
            if re.search('midterm', title, re.I) and not include_midterms:
                continue
            data = cmp_get(f"/courses/{slug}/projects/{project['slug']}/submissions")
            if not isinstance(data, dict) or not isinstance(data.get('submissions'), list):
                raise ValueError('Unexpected CMP envelope; inspect pagination before proceeding')
            rows = []
            for r in data['submissions']:
                row = {k: r.get(k) for k in PROJECT_KEEP}
                row['email_domain'] = email_domain(r.get('student_email'))
                rows.append(row)
            write_private(cache / f"submissions-{year}-{project['slug']}.json",
                          {'course': slug, 'project': project['slug'], 'submissions': rows})
            summary[year]['projects'][project['slug']] = len(rows)
        for hw in meta.get('homeworks', []):
            data = cmp_get(f"/courses/{slug}/homeworks/{hw['slug']}/submissions")
            rows = [{k: r.get(k) for k in HOMEWORK_KEEP} for r in data.get('submissions', [])]
            write_private(cache / f"homework-{year}-{hw['slug']}.json",
                          {'course': slug, 'homework': hw['slug'], 'submissions': rows})
            summary[year]['homeworks'][hw['slug']] = {
                'rows': len(rows), 'unique_submitters': len({r['student_id'] for r in rows})}
    (output / 'cmp-fetch-summary.json').write_text(json.dumps(summary, indent=2))
    return summary
