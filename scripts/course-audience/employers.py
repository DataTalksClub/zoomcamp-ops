"""Employer aggregates with explicit provenance and unknown categories.

Metadata is a private, manually reviewed company-metadata.json mapping normalized
employer keys to industry, segment, size and primary-source URLs. Do not infer a
startup from an unfamiliar name, or current employment from an email domain.
"""
from collections import Counter
import json


def analyze(output, rows):
    from aggregate import company_key, NOT_COMPANY
    path=output/'company-metadata.json'
    metadata=json.loads(path.read_text()) if path.exists() else {}
    companies=Counter(); display={}; domain_only=0; missing=0
    for r in rows:
        company=r['company'].strip()
        if r['evidence_type']=='domain_signal' or 'Company from corporate email domain only' in r['notes']:
            domain_only+=1
            continue
        if r.get('seniority')=='student' or not company or NOT_COMPANY.match(company) or company.lower() in {'nda','dream job','tbd','seeking opportunities','no','self','personal project','personal development','engineer','data engineering student','data engineering zoomcamp','zoomcamp / self-directed project'} or r['freelance'] in ('freelance','self-employed'):
            missing+=1
            continue
        key=company_key(company)
        companies[key]+=1;display.setdefault(key,company)
    industry=Counter();segment=Counter();covered=0
    for key,count in companies.items():
        meta=metadata.get(key,{})
        # Only reviewed, sourced metadata may affect the breakdown.
        if not meta.get('sources'):
            meta={}
        industry[meta.get('industry','unknown')]+=count
        segment[meta.get('segment','unknown')]+=count
        covered+=count if meta else 0
    total=sum(companies.values()); n=len(rows)
    def share(count,denom):return round(100*count/denom,1) if denom else 0
    top=[]
    for key,count in companies.most_common():
        meta=metadata.get(key,{}) if metadata.get(key,{}).get('sources') else {}
        top.append({'company':display[key],'key':key,'authors':count,'industry':meta.get('industry','unknown'),'segment':meta.get('segment','unknown'),'size':meta.get('size','unknown'),'sources':meta.get('sources',[])})
    return {'enriched_authors':n,'authors_with_named_employer':total,'named_employer_share_pct':share(total,n),'distinct_employers':len(companies),'domain_only_excluded':domain_only,'no_named_employer_or_independent':missing,'metadata_covered_authors':covered,'top_employers':top,'industry':dict(industry),'segment':dict(segment),'segment_share_of_named_employer_pct':{k:share(v,total) for k,v in segment.items()},'segment_share_of_enriched_pct':{k:share(v,n) for k,v in segment.items()}}


def section(stats):
    from aggregate import table
    n=stats['authors_with_named_employer'];g=stats['enriched_authors']
    lines=['## Employers','',f'{n} of {g} enriched authors ({stats["named_employer_share_pct"]}%) name an employer; {stats["distinct_employers"]} distinct normalized employers. '+f'{stats["domain_only_excluded"]} domain-only affiliations are excluded from current-employer counts. Independent practitioners remain in the freelancer segment.','',
    'These are public self-reports at collection time, not employment verification. GitHub profiles can be stale. Unknown industry, size and business model stay unknown; a small or unfamiliar firm is never assumed to be a startup. Agency/consultancy takes precedence over enterprise size so segments do not overlap.','',
    'Top employers by author count (ties alphabetical):','']
    top=sorted(stats['top_employers'],key=lambda r:(-r['authors'],r['company'].lower()))[:30]
    lines+=[table(['Employer','Authors','Industry','Segment','Size (public description)'],[[r['company'],r['authors'],r['industry'],r['segment'],r['size']] for r in top]),'',
    f'Industry breakdown among {n} authors with a named employer. Metadata has sourced coverage for {stats["metadata_covered_authors"]} authors; the rest stay unknown.','',table(['Industry','Authors','Share of named employers'],[[k,v,f'{100*v/n:.1f}%' if n else '-'] for k,v in sorted(stats['industry'].items(),key=lambda x:-x[1])]),'',
    'Business-model segments (denominators shown explicitly):','',table(['Segment','Authors','Share of named employers','Share of enriched authors'],[[k,stats['segment'].get(k,0),f'{stats["segment_share_of_named_employer_pct"].get(k,0):.1f}%',f'{stats["segment_share_of_enriched_pct"].get(k,0):.1f}%'] for k in ['enterprise','startup','agency/consultancy','other','unknown']]),'',
    '### Named companies relevant to sponsor pitches','',
    'The following are audience affiliations, not evidence of adoption, purchase intent, or permission to contact. Pitch relevance is an editorial inference from the industry.','']
    known=[r for r in stats['top_employers'] if r['sources']]
    for name,industries,why in [('Astronomer',{'IT services / consulting','Software / cloud','Finance / insurance','Retail / ecommerce','Telecom','Manufacturing / automotive','Transport / logistics','Energy'},'production pipeline orchestration, client implementations, and operational reliability'),('Snowflake',{'Finance / insurance','Retail / ecommerce','Software / cloud','IT services / consulting','Healthcare / life sciences','Media / advertising','Telecom','Energy'},'warehouse consolidation, governed analytics, and shared reporting')]:
        candidates=sorted([r for r in known if r['industry'] in industries],key=lambda r:(-r['authors'],r['company'].lower()))[:20]
        lines += [f'**{name}:** '+('; '.join(f'{r["company"]} ({r["authors"]})' for r in candidates) or 'No sourced company classification available')+f'. Potential angle: {why}.','']
    lines+=['Company classification sources (company facts only; no private author data):','']
    for r in known:
        lines.append(f'- {r["company"]}: '+', '.join(f'[source {i+1}]({u})' for i,u in enumerate(r['sources'])))
    return '\n'.join(lines)+'\n'


def append(output):
    from aggregate import load
    _,good=load(output);stats=analyze(output,good)
    summary=output/'audience-summary.md'; text=summary.read_text()
    marker='\n## Employers\n'
    if marker in text:text=text.split(marker)[0]+'\n'
    baseline=json.loads((output/'rest-baseline.json').read_text())['baseline_enriched']
    text+=f'\nCoverage before/after: **{baseline} -> {len(good)} enriched** authors.\n\n'+section(stats)
    summary.write_text(text)
    dest=output/'audience-stats.json';d=json.loads(dest.read_text());d['coverage_before_after']={'before':baseline,'after':len(good)};d['employers']=stats
    d['shares']={'denominator_enriched':len(good),'seniority':{},'role_family':{},'freelancer_pct':round(100*d['freelance']/len(good),1) if good else 0,'named_employer_pct':stats['named_employer_share_pct']}
    for kind in ['seniority','role_family']:
        d['shares'][kind]={k:round(100*v/len(good),1) if good else 0 for k,v in d[kind].items()}
    ledger=json.loads((output/'treg-ledger.json').read_text());d['treg']={'charged_usd':sum(e['charged_micro'] or 0 for e in ledger)/1e6,'unsettled':sum(e['charged_micro'] is None for e in ledger),'cap_usd':10}
    summary.write_text(text+f'\nShared Treg spend: **${d["treg"]["charged_usd"]:.6f} / $10**; unsettled calls: {d["treg"]["unsettled"]}.\n')
    dest.write_text(json.dumps(d,indent=2))
    return stats
