#!/usr/bin/env python3
"""Re-check previously rejected or low-confidence identity candidates with every evidence type.

Input  (private): DIR/recheck-candidates.json  [{github, candidate_linkedin, candidate_name, candidate_company, previous}]
Output (private): DIR/rechecks.json  {github: {status, outcome, checked: [...]}} used by classify.py
A candidate is CONFIRMED only by a linking fact: a self-submitted or GitHub-declared LinkedIn equal to it,
a matching corporate commit-email domain ("email domain matches"), or commit author name equal to the
candidate's name plus an identity-provider match. Otherwise it stays rejected and the checks are listed.
"""
import json
import subprocess

from identities import domain_kind
from classify import name_tokens


def commit_identities(repo):
    p = subprocess.run(['gh', 'api', f'repos/{repo}/commits?per_page=100', '--jq',
                        '[.[] | {n: .commit.author.name, d: (.commit.author.email | split("@") | .[1])}]'],
                       capture_output=True, text=True, timeout=60)
    if p.returncode:
        return []
    return json.loads(p.stdout or '[]')


def recheck(output):
    cands = json.loads((output / 'recheck-candidates.json').read_text())
    authors = {a['github'].lower(): a for a in json.loads((output / 'cache' / 'authors.json').read_text()) if a['github']}
    out = {}
    for c in cands:
        a = authors.get(c['github'].lower())
        checked, status, outcome = [], 'rejected', ''
        if not a:
            out[c['github']] = {'status': 'rejected', 'outcome': 'author not in this course/year set', 'checked': []}
            continue
        slug = (c.get('candidate_linkedin') or '').lower()
        self_li, gh_li = a['self_submitted_linkedin'], a['github_declared_linkedin']
        checked.append(f"CMP self-submitted LinkedIn: {', '.join(self_li) or 'none'}")
        checked.append(f"GitHub/personal-site LinkedIn: {', '.join(gh_li) or 'none'}")
        names, corp_domains = set(), set()
        for repo in [r.split(':', 1)[1] for r in a['repos']]:
            for ci in commit_identities(repo):
                if ci.get('n'):
                    names.add(ci['n'])
                if ci.get('d') and domain_kind(ci['d']) == 'corporate':
                    corp_domains.add(ci['d'])
        checked.append(f"commit author names: {', '.join(sorted(names)) or 'none'}")
        checked.append('commit email domains: ' + ('corporate domain present' if corp_domains else 'free/noreply only'))
        checked.append(f"CMP email domain: {a['email_domain_kind'] or 'none'}")
        cand_tokens = name_tokens(c.get('candidate_name') or '')
        name_match = bool(cand_tokens) and any(cand_tokens <= name_tokens(n) or name_tokens(n) <= cand_tokens and len(name_tokens(n)) >= 2 for n in names)
        company = (c.get('candidate_company') or '').lower().split()[0] if c.get('candidate_company') else ''
        dom_match = bool(company) and any(company in d for d in corp_domains)
        if self_li or gh_li:
            li = (self_li or gh_li)[0]
            status = 'confirmed'
            outcome = (f"self-submitted LinkedIn {li} confirms identity" if self_li else f"GitHub-declared LinkedIn {li} confirms identity")
            outcome += '; earlier candidate ' + ('matches' if li == slug else f"{slug or 'none'} superseded")
        elif dom_match:
            status, outcome = 'confirmed', 'email domain matches candidate company'
        elif name_match and c.get('provider_confidence', 0) >= 8:
            status, outcome = 'confirmed', f"commit author name matches candidate name and identity provider matched ({c.get('provider_confidence')}/10)"
        else:
            reasons = []
            if names and cand_tokens and not name_match:
                reasons.append(f"commit author name ({', '.join(sorted(names))}) differs from candidate ({c.get('candidate_name')})")
            if not names:
                reasons.append('no commit author name')
            reasons.append('no self-submitted/declared LinkedIn, no corporate domain')
            outcome = 'kept rejected: ' + '; '.join(reasons)
        out[c['github']] = {'status': status, 'outcome': outcome, 'checked': checked, 'previous': c.get('previous', ''),
                            'candidate_linkedin': slug, 'commit_names': sorted(names)}
    (output / 'rechecks.json').write_text(json.dumps(out, indent=1))
    (output / 'rechecks.json').chmod(0o600)
    return {k: v['status'] for k, v in out.items()}
