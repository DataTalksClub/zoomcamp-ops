#!/usr/bin/env python3
"""Supplement cached scans with newly discovered configuration families.

Fetch candidate files at the same submitted commit, add conservative evidence to
cache, then rerun analyze.py scan to apply project scope and rebuild the CSV.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote
from analyze import detect, repo_name, submissions


def review(output, rows):
    last=sorted(rows,key=lambda r:(r['project_slug'],r['id']))[-1]
    repo=repo_name(last['github_link']);ref=str(last.get('commit_id') or '').strip()
    key=hashlib.sha256((repo.lower()+'@'+ref).encode()).hexdigest()[:20]
    path=output/'cache/scans'/(key+'.json')
    if not path.exists():return
    data=json.loads(path.read_text())
    if data['status']!='scanned':return
    files=data['files']
    candidates=[p for p in files if Path(p).name in ('.bruin.yml','.bruin.yaml','pipeline.yml','pipeline.yaml')]
    if any(re.search('nifi',w,re.I) for w in data['weak']):
        candidates += [p for p in files if 'nifi' in p.lower() and p.endswith(('.xml','.json','.yml','.yaml'))]
        candidates += [p for p in files if Path(p).name in ('docker-compose.yml','docker-compose.yaml','compose.yml','compose.yaml')]
    if not data['evidence'] or any(re.search(r'Cloud Scheduler|EventBridge|dbt Cloud|GitHub Actions|\bcron\b',w,re.I) for w in data['weak']):
        candidates += [p for p in files if (p.endswith('.tf') or p.startswith('.github/workflows/') or 'crontab' in Path(p).name.lower())]
    fresh=[]
    for filename in sorted(set(candidates)):
        url=f'repos/{repo}/contents/{quote(filename)}'
        if re.fullmatch('[0-9a-fA-F]{7,40}',ref):url+='?ref='+ref
        proc=subprocess.run(['gh','api',url,'-H','Accept: application/vnd.github.raw+json'],capture_output=True,timeout=45)
        if proc.returncode==0:
            ev,_,_=detect([(filename,proc.stdout.decode(errors='replace'))])
            for tool,signals in ev.items():
                for signal in signals:
                    if signal not in data['evidence'].setdefault(tool,[]):
                        data['evidence'][tool].append(signal);fresh.append((tool,signal))
    if fresh:
        path.write_text(json.dumps(data));print(repo,json.dumps(fresh),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda rows:review(a.output,rows),submissions(a.output).values()))
