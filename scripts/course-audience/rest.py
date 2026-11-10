#!/usr/bin/env python3
"""Public-signal audit for authors missed by the main enrichment pass.

Run gather while paid enrichment is active; search/merge only after its owner exits.
All research artifacts stay in the private report directory. Never execute repo code.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import html
import ipaddress
import json
from pathlib import Path
import re
import socket
import subprocess
import urllib.request
from urllib.parse import urlparse

from classify import FIELDS, FREELANCE_RE, STUDENT_RE, SEEKER_RE, country_of, role_family, seniority, clean_company, li_data, apply_linkedin
from identities import domain_kind

EMAIL = re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+')
ROLE = re.compile(r'\b(?:(?:senior|junior|lead|staff|principal|freelance|aspiring)\s+)?(?:data engineer|analytics engineer|data scientist|machine learning engineer|software engineer|backend engineer|data analyst|business intelligence analyst|QA automation lead|DevOps engineer)\b', re.I)


def safe(text):
    return EMAIL.sub('[address removed]', str(text))


def redact(value):
    if isinstance(value, dict):
        return {k: redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return safe(value) if isinstance(value, str) else value


def gh(args):
    p = subprocess.run(['gh', 'api'] + args, capture_output=True, text=True, timeout=65)
    if p.returncode:
        return {'error': safe(p.stderr[:250])}
    try:
        return json.loads(p.stdout)
    except ValueError:
        return {'error': 'invalid response'}


def readme(repo):
    import base64
    r = gh([f'repos/{repo}/readme'])
    if not r.get('content'):
        return {'error': r.get('error', 'no README')}
    return {'url': r.get('html_url'), 'text': safe(base64.b64decode(r['content']).decode('utf8', 'replace')[:100000])}


def site(url):
    """Only public HTTP(S); bound body/time and refuse private address destinations."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        host = urlparse(url).hostname
        if not host or any(not ipaddress.ip_address(x[4][0]).is_global for x in socket.getaddrinfo(host, None)):
            return {'url': url, 'error': 'nonpublic host'}
        # Refuse redirects: do not follow a public URL into a private destination.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 public-course-research'})
        with urllib.request.build_opener(NoRedirect).open(request, timeout=12) as r:
            raw = r.read(300000).decode('utf8', 'replace')
        raw = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', raw, flags=re.S|re.I)
        text = re.sub('<[^>]+>', ' ', raw)
        return {'url': url, 'text': safe(re.sub(r'\s+', ' ', html.unescape(text))[:60000])}
    except Exception as e:
        return {'url': url, 'error': type(e).__name__}


def audit(a, cache):
    dest = cache / f"{a['student_id']}.json"
    if dest.exists():
        return json.loads(dest.read_text())
    handle = a['github']
    out = {'student_key': f"cmp-{a['student_id']}", 'github': handle, 'sources': [], 'commit_domains': [], 'checks': []}
    if handle and a.get('github_profile', {}).get('type') != 'Organization':
        prof = a.get('github_profile') or {}
        out['sources'].append({'url': 'https://github.com/'+handle, 'kind': 'github_profile', 'text': safe(prof.get('bio') or '')})
        out['sources'].append(dict(readme(f'{handle}/{handle}'), kind='profile_readme'))
        q = 'query($login:String!){user(login:$login){pinnedItems(first:6,types:REPOSITORY){nodes{... on Repository{nameWithOwner description owner{login}}}}}}'
        pins = gh(['graphql', '-f', 'query='+q, '-f', 'login='+handle])
        nodes = (((pins.get('data') or {}).get('user') or {}).get('pinnedItems') or {}).get('nodes') or []
        out['checks'].append('pinned repositories: '+str(len(nodes)) if 'errors' not in pins and 'error' not in pins else 'pinned repositories unavailable')
        for pin in nodes:
            # A pinned repo authored by someone else cannot establish the user's occupation.
            out['sources'].append({'url':'https://github.com/'+pin['nameWithOwner'], 'kind':'pinned_description', 'text':safe(pin.get('description') or '')})
            if pin['owner']['login'].lower() == handle.lower():
                out['sources'].append(dict(readme(pin['nameWithOwner']), kind='pinned_readme'))
        urls = [prof.get('blog')] + (prof.get('social') or [])
        for url in dict.fromkeys(u for u in urls if u):
            if 'linkedin.com' not in url and 'github.com' not in url:
                out['sources'].append(dict(site(url), kind='linked_public_site'))
        for tagged in a['repos'][:2]:
            repo = tagged.split(':',1)[1]
            out['sources'].append(dict(readme(repo), kind='project_readme'))
            commits = gh([f'repos/{repo}/commits?author={handle}&per_page=30', '--jq', '[.[] | {login:.author.login,domain:(.commit.author.email | split("@") | last)}]'])
            if isinstance(commits,list):
                out['commit_domains'] += [{'domain':safe(c['domain'].lower()), 'kind':domain_kind(c['domain'].lower())} for c in commits if c.get('login','') and c['login'].lower()==handle.lower() and '.' in c.get('domain','') and not c['domain'].lower().endswith(('.local','.localhost','.invalid'))]
            else:
                out['checks'].append('commit domains unavailable')
    else:
        out['checks'].append('No attributable personal GitHub account; no identity inferred from organization/repo contributors')
    out['checks'].append('Slack: no existing Slack display-name dataset; no lookup attempted')
    out['commit_domains'] = list({(x['domain'],x['kind']):x for x in out['commit_domains']}.values())
    dest.write_text(json.dumps(redact(out),ensure_ascii=False,indent=1))
    dest.chmod(0o600)
    return out


def follow(output, workers):
    """Check social profiles and personal GitHub Pages sites linked in profile READMEs."""
    def one(path):
        evidence=json.loads(path.read_text())
        existing={s.get('url') for s in evidence['sources']}
        texts=[s.get('text','') for s in evidence['sources'] if s['kind']=='profile_readme']
        urls=set(re.findall(r'https?://[^\s<>\[\]()"\']+', '\n'.join(texts)))
        for url in sorted(urls):
            host=(urlparse(url).hostname or '').lower()
            social=host.removeprefix('www.') in {'kaggle.com','medium.com','dev.to','x.com','twitter.com'}
            personal=host==evidence['github'].lower()+'.github.io'
            if not (social or personal) or url in existing or urlparse(url).path in ('','/'):
                continue
            evidence['sources'].append(dict(site(url),kind='readme_linked_social'))
        path.write_text(json.dumps(redact(evidence),ensure_ascii=False,indent=1))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(one,(output/'cache/rest').glob('[0-9]*.json')))


def role_claim(text, profile=False):
    """Require a self-description; technical project prose is never an occupation."""
    if profile:
        matches = list(ROLE.finditer(text))
        return matches[0].group(0) if matches and not re.search(r'was |former |previous|used to|ex-',text[:matches[0].start()],re.I) else ''
    for line in text.splitlines():
        line = re.sub(r'<[^>]+>', ' ', line).replace('**', '').strip(' #*_-')
        if re.search(r'looking|seeking|learning|studying|want to|become|tutorial|course', line, re.I):
            continue
        if re.search(r"\b(?:I am|I.m|I work as|I currently work as|my current role is)\s+(?:a |an )?",line,re.I):
            m = ROLE.search(line)
            if m and not re.search(r'was |former |previous|used to|ex-',line[:m.start()],re.I):
                return m.group(0)
    return ''


def improve(row, evidence):
    row = dict(row)
    if row['flag'] or row['enriched']=='yes':
        return row
    for src in evidence['sources']:
        if src['kind'] not in ('github_profile','profile_readme','linked_public_site'):
            continue
        text = src.get('text','')
        title = role_claim(text,src['kind']=='github_profile')
        if title:
            row.update(title=title, confidence='high', enriched='yes', evidence_type=src['kind'],source='public_rest_audit', source_url=src.get('url',''),role_family=role_family(title),seniority=seniority(title,text[:300],has_company=bool(row['company'])))
            row['freelance'] = 'freelance' if FREELANCE_RE.search(title) else row['freelance']
            row['notes'] += '; Own public self-description; occupation only, no employer inferred'
            break
    # Domain observations are historical affiliations, never asserted as a current employer.
    corp = [x['domain'] for x in evidence['commit_domains'] if x['kind']=='corporate']
    if corp:
        row['notes'] += '; Corporate commit domain signal (historical affiliation only): '+', '.join(corp)
    return row



def apply_reviewed(row, evidence, fact):
    """A reviewed exact self-description; rejected third-party matches stay rejected."""
    if not fact or row['enriched']=='yes' and not row['flag']:
        return row
    sources=[s for s in evidence['sources'] if s['kind']==fact['kind'] and fact['quote'] in s.get('text','')]
    assert sources and fact['kind'] in ('github_profile','profile_readme','linked_public_site','readme_linked_social'), 'Missing own-source quote'
    row=dict(row)
    row.update(title=fact['title'], company=fact.get('company',''), confidence='high',enriched='yes',flag='',
               source='reviewed_public_rest_audit',source_url=sources[0].get('url',''),evidence_type=fact['kind'],
               role_family=fact.get('role_family') or role_family(fact['title']),
               seniority=fact.get('seniority') or seniority(fact['title'], '',has_company=bool(fact.get('company'))),
               freelance=fact.get('freelance',''))
    row['notes']+='; Reviewed own-source quote: '+fact['quote']+'; Any prior third-party identity candidate remains unconfirmed and is not used'
    return row


def declared_links(output):
    """Preserve URL path encoding, including non-ASCII LinkedIn identifiers."""
    targets=set(json.loads((output/'rest-baseline.json').read_text())['targets'])
    result=[]
    reviewed_path=output/'rest-declared-reviewed.json'
    reviewed=json.loads(reviewed_path.read_text()) if reviewed_path.exists() else {}
    for author in json.loads((output/'cache/authors.json').read_text()):
        key=f"cmp-{author['student_id']}"
        if key not in targets:
            continue
        prof=author.get('github_profile') or {}
        texts=list(prof.get('social') or [])+[prof.get('blog') or '',prof.get('bio') or '']
        path=output/'cache/rest'/f"{author['student_id']}.json"
        if path.exists():
            texts += [s.get('text','') for s in json.loads(path.read_text())['sources'] if s['kind'] in ('profile_readme','linked_public_site')]
        slugs=sorted({slug.lower() for slug in re.findall(r'linkedin\.com/in/([\w%.-]+)', '\n'.join(texts),re.I)}-{'https','your-linkedin','your-name','username'})
        fact=reviewed.get(author['github'])
        if fact:
            evidence=json.loads(path.read_text())
            assert any(s.get('url')==fact['source_url'] and fact['quote'] in s.get('text','') for s in evidence['sources']), 'Missing reviewed declaration quote'
            slugs=sorted(set(slugs+[fact['slug']]))
        if slugs:
            result.append({'github':author['github'],'student_key':key,'slugs':slugs,'uncached':[] if any(li_data(output/'cache',slug) for slug in slugs) else [slug for slug in slugs if not (output/'cache'/f'li-full-{slug}.json').exists()]})
    (output/'rest-new-linkedin.json').write_text(json.dumps(result,indent=1))
    return result


def gather(output,workers):
    baseline=json.loads((output/'rest-baseline.json').read_text())
    targets=set(baseline['targets']); authors=json.loads((output/'cache/authors.json').read_text())
    cache=output/'cache/rest';cache.mkdir(parents=True,exist_ok=True)
    selected=[a for a in authors if 'cmp-'+str(a['student_id']) in targets]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        records=list(pool.map(lambda a:audit(a,cache),selected))
    declared_links(output)
    bykey={e['student_key']:e for e in records}
    facts_path=output/'rest-reviewed.json'
    facts=json.loads(facts_path.read_text()) if facts_path.exists() else {}
    rows=[]
    links_path=output/'rest-new-linkedin.json'
    links={x['github']:x for x in json.loads(links_path.read_text())} if links_path.exists() else {}
    for original in baseline['rows']:
        if original['student_key'] not in targets: continue
        row=improve(original,bykey[original['student_key']])
        row=apply_reviewed(row,bykey[original['student_key']],facts.get(original['github']))
        for slug in links.get(original['github'],{}).get('slugs',[]):
            if slug in ('https','your-linkedin','your-name','username'):
                continue
            profile=li_data(output/'cache',slug)
            if profile:
                row=dict(row)
                apply_linkedin(row,profile,int(max(row['years'].split(';'))))
                row.update(confidence='high',flag='',enriched='yes',evidence_type='github_declared_linkedin',source='own_public_declared_link',linkedin_url='https://www.linkedin.com/in/'+slug,source_url='https://www.linkedin.com/in/'+slug)
                row['enriched']='yes' if row['company'] or row['title'] or row['seniority']!='unknown' else ''
                row['notes']+='; LinkedIn explicitly declared in own public profile/README/site; third-party candidate not used'
                break
        row['confidence']='flagged' if row['flag'] else row['confidence']
        row['audit_sources']=str(len(bykey[row['student_key']]['sources']))
        row['audit_checks']='; '.join(bykey[row['student_key']]['checks'])
        rows.append(row)
    with (output/'enrichment-rest.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS+['audit_sources','audit_checks']);w.writeheader();w.writerows(rows)
    print(json.dumps({'targets':len(rows),'public_role_claims':sum(r['enriched']=='yes' for r in rows)}))


def search(output,workers):
    from treg_budget import Ledger
    baseline=json.loads((output/'rest-baseline.json').read_text())
    ledger=Ledger(output,10,9)
    authors=json.loads((output/'cache/authors.json').read_text())
    targets=set(baseline['targets'])
    def one(a):
        dest=output/'cache/rest'/f"search-{a['student_id']}.json"
        if dest.exists() or not a['github']:return
        name=(a.get('github_profile') or {}).get('name') or a.get('commit_name') or ''
        q=' '.join(filter(None,[f'"{name}"' if name else '',f'"{a["github"]}"','data engineer career employer']))
        result=ledger.call('treg.web.search',{'q':q,'limit':5},0.005,label='rest-search:'+str(a['student_id']))
        dest.write_text(json.dumps(redact(result)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(one,[a for a in authors if 'cmp-'+str(a['student_id']) in targets]))
    print(json.dumps({'spent_usd':ledger.spent()/1e6}))


def read_rows(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def baseline(output, baseline_enriched=None):
    dest=output/'rest-baseline.json'
    if dest.exists():
        raise ValueError('Baseline already exists; preserve the original target set')
    rows=read_rows(output/'enrichment-all.csv')
    targets=[r['student_key'] for r in rows if not r['evidence_type'] or r['evidence_type']=='none' or r['confidence']=='none']
    n=sum(r['enriched']=='yes' and not r['flag'] for r in rows)
    dest.write_text(json.dumps({'baseline_enriched':n if baseline_enriched is None else baseline_enriched,'targets':targets,'rows':rows},indent=1))
    dest.chmod(0o600)
    print(json.dumps({'targets':len(targets),'baseline_enriched':n}))


def merge(output, predecessor_pid):
    if not predecessor_pid or Path(f'/proc/{predecessor_pid}').exists():
        raise ValueError('Supply the original predecessor PID and wait for it to exit')
    current=read_rows(output/'enrichment-all.csv')
    audited={r['student_key']:r for r in read_rows(output/'enrichment-rest.csv')}
    before=sum(r['enriched']=='yes' and not r['flag'] for r in current)
    for index,row in enumerate(current):
        rest=audited.get(row['student_key'])
        if rest and rest['confidence'] in ('high','medium') and rest['enriched']=='yes' and not rest['flag'] and not (row['enriched']=='yes' and not row['flag']):
            current[index]={k:rest[k] for k in FIELDS}
    authors={f"cmp-{a['student_id']}":a for a in json.loads((output/'cache/authors.json').read_text())}
    for row in current:
        if row['enriched']!='yes' or row['flag']:
            continue
        author=authors[row['student_key']]
        prof=author.get('github_profile') or {}
        if not row['company'] and prof.get('type')=='User':
            company=clean_company(prof.get('company') or '')
            if not company:
                m=re.search(r'\b(?:engineer|analyst|scientist|developer)\s+@\s*([\w][\w &.-]{1,60})',prof.get('bio') or '',re.I)
                company=clean_company(m.group(1).split(',')[0]) if m else ''
            if company:
                row['company']=company
                row['notes']+='; Employer self-declared on https://github.com/'+row['github']+' (snapshot; currentness unverified)'
        match=re.match(r'^(?:Founder & CTO|Founder|CTO) at (.+)$',row['company'],re.I)
        if match:
            row['company']=match.group(1)
            row['notes']+='; Employer extracted from own company field role statement'
    employer_facts_path=output/'rest-employer-reviewed.json'
    employer_facts=json.loads(employer_facts_path.read_text()) if employer_facts_path.exists() else {}
    for row in current:
        fact=employer_facts.get(row['github'])
        if not fact or row['company'] or row['enriched']!='yes' or row['flag']:
            continue
        audit_path=output/'cache/rest'/f"{row['student_key'].removeprefix('cmp-')}.json"
        evidence=json.loads(audit_path.read_text())
        source=next(s for s in evidence['sources'] if s.get('url')==fact['url'] and fact['quote'] in s.get('text',''))
        row['company']=fact['company'];row['notes']+='; Employer from linked public staff page: '+source['url']
    # Preserve the final accepted outcome in the audit CSV, including rows enriched
    # by the predecessor after the original baseline was taken.
    latest={r['student_key']:r for r in current}
    for key,row in audited.items():
        accepted=latest[key]
        if accepted['enriched']=='yes' and not accepted['flag']:
            row.update({k:accepted[k] for k in FIELDS})
        row['confidence']='flagged' if row['flag'] else row['confidence']
        search_path=output/'cache/rest'/f"search-{key.removeprefix('cmp-')}.json"
        if search_path.exists():
            result=json.loads(search_path.read_text()) or {}
            count=len((result.get('output') or {}).get('results') or [])
            row['audit_checks']+=f'; name+handle web search: {count} results; unconfirmed identities excluded'
        else:
            row['audit_checks']+='; no usable GitHub handle for corroborated search'
    with (output/'enrichment-all.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(current)
    with (output/'enrichment-rest.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS+['audit_sources','audit_checks']);w.writeheader();w.writerows(audited.values())
    from aggregate import aggregate
    from employers import append
    aggregate(output,['Airflow','Astronomer'])
    stats=append(output)
    print(json.dumps({'before_predecessor':before,'after':stats['enriched_authors'],'rest_targets':len(audited)}))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['baseline','gather','follow','search','merge'])
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--baseline-enriched',type=int)
    p.add_argument('--predecessor-pid',type=int)
    a=p.parse_args()
    if a.action=='baseline':baseline(a.output,a.baseline_enriched)
    elif a.action=='merge':merge(a.output,a.predecessor_pid)
    else:globals()[a.action](a.output,a.workers)
