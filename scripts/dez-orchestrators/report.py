#!/usr/bin/env python3
"""Render reconciled summaries and a manually reviewed project shortlist."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path


def table(headers, rows):
    def clean(x):return str(x).replace('|','/').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(clean,r))+' |' for r in rows])


def generate(output):
    rows=list(csv.DictReader((output/'orchestrators.csv').open()))
    selected=json.loads((output/'shortlist.json').read_text())
    enrichment=list(csv.DictReader((output/'enrichment.csv').open()))
    assert 10<=len(selected)<=20
    assert len({r['repo'].lower() for r in selected})==len(selected)
    counts={y:Counter(t for r in rows if r['year']==y for t in r['orchestrator(s)'].split(';')) for y in ('2025','2026')}
    cats=sorted(set(counts['2025'])|set(counts['2026']))
    summary=['# DE Zoomcamp final-project orchestrator audit','',
        'Snapshot: 2026-11-10. Source: authenticated CMP exports; submitted GitHub commits scanned as source, without running project code.','',
        '## Per-year counts','',table(['Orchestrator / classification','2025','2026'],[(t,counts['2025'][t],counts['2026'][t]) for t in cats]),'',
        'Counts are distinct normalized repository URLs within each year, across all three final-project attempts. Labels overlap; Astronomer is a subset of Airflow, so do not add them. None and unknown are mutually exclusive with detected orchestrators. These are static evidence counts, not verified production deployments.','']
    totals=[]
    for y in ('2025','2026'):
        exports=[json.loads(p.read_text()) for p in sorted((output/'cache').glob(f'submissions-{y}-*.json'))]
        submissions=[r for d in exports for r in d['submissions']]
        yr=[r for r in rows if r['year']==y]
        assert sum(int(r['submission_rows']) for r in yr)==len(submissions)
        totals.append([y,len(submissions),len({r['student_id'] for r in submissions}),len(yr),sum(r['status']=='scanned' for r in yr),sum(r['status']!='scanned' for r in yr)])
        summary += [f"- {y}: slugs `project1`, `project2`, `project3`; attempt submission totals "+', '.join(str(len(d['submissions'])) for d in exports)+'.']
    summary += ['',table(['Year','Submission rows','Distinct students','CSV rows / repositories','Scanned','Unknown / failed'],totals),'',
        '## Method and limits','',
        'CMP course metadata identifies all three entries as final-project attempts, not three separate capstones. The course project instructions for 2026 point to the same final-project document. The OpenAPI schema identifies the submissions route as an export with no pagination parameters. All rows, including failed or unpassed submissions, were included. Student counts use private identifiers only; no email is included in outputs.','',
        'GitHub links are normalized case-insensitively to owner/repository (trailing slash, .git and tree/blob suffix removed). Retries of the same repository within a year are combined; the latest attempt and submission ID selects the commit. Distinct repositories by the same student remain distinct observations. Thus repository counts differ from both student counts and raw submission counts. `submission_rows` reconciles every export row.','',
        'Detection greps executable source/configuration and dependency declarations. Airflow imports and apache-airflow dependencies; Astronomer runtime images; Kestra plugins/container images; Dagster/Prefect/Mage/Luigi and other framework imports/configs are recorded with paths and minimal signal snippets. Markdown mentions stay in `weak_mentions` and do not count. A submitted subdirectory limits eligible evidence; common teaching/homework directories are excluded. Manual overrides, when present, are recorded in notes and in the private review log. Dependencies/container definitions show implementation intent, not proof of successful execution.','',
        'Archives are fetched with authenticated gh at the submitted commit when valid. Missing/malformed commits use the default archive; inaccessible commits remain unknown. Private/deleted repositories, invalid URLs, archive/time/text limits and rate-limit failures stay explicit. Binary data, dependency environments and lockfiles are skipped. Text files larger than 2 MB and archive text beyond 60 MB are not scanned. Static detection may miss renamed/custom orchestration or notebook-only implementations. Whole-course repositories can still be ambiguous; use the evidence before making individual claims.','',
        'For pitch use, Airflow/Astronomer examples demonstrate learners independently adopting an orchestration ecosystem. They do not establish causal impact of curriculum or a representative employer distribution. Shortlist selection intentionally favors documented, reproducible, technically varied examples; it is not a random sample.','',
        '## Author enrichment','',table(['Author','GitHub','Employer / status','Source'],[(r['author'],r['GitHub'],r['employer'],r['source']) for r in enrichment]),'',
        'Public GitHub profiles were checked first, followed by public LinkedIn/web search for missing employers. Treg was used only for unresolved authors. Employer claims are dated profile observations; unresolved or historical affiliations are explicitly labeled. See enrichment.csv for URLs and identity/verification notes, flagged-projects.md for project details, and treg-usage.md for the complete spend ledger.']
    (output/'summary.md').write_text('\n'.join(summary)+'\n')
    flagged=['# Selected final projects','', 'Curated for technical interest, documentation and pitch relevance; not a production-readiness ranking. Scores are CMP project rubric scores, not total scores and not directly comparable across years. Public identity/employer observations are current-profile snapshots on 2026-11-10.','']
    for i,item in enumerate(selected,1):
        matches=[r for r in rows if r['repo'].lower()==item['repo'].lower() and r['year']==str(item['year'])]
        assert len(matches)==1,item
        r=matches[0];user=r['repo'].split('/')[0]
        e=next(x for x in enrichment if x['GitHub'].lower()=='https://github.com/'+user.lower())
        flagged += [f"## {i}. {r['repo']} ({r['year']})",'',f"- Repository: https://github.com/{r['repo']}",f"- Author: [{e['author']}](https://github.com/{user})",f"- Orchestrators: {r['orchestrator(s)']}; CMP project score: {r['project_score']}.",f"- Why flagged: {item['why']}",f"- Evidence: {r['evidence']}",f"- Employer: {e['employer']} ({e['source']}); {e.get('source_url','')}",f"- Public bio: {e.get('bio','') or 'Not listed'}",f"- Verification: {e.get('notes','')}",'']
    (output/'flagged-projects.md').write_text('\n'.join(flagged))
    print(json.dumps({'counts':counts,'totals':totals,'flagged':len(selected)},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args();generate(a.output)
