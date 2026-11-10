#!/usr/bin/env python3
"""Recover oversized archives using GitHub's tree and raw-file APIs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, urlparse, unquote
from analyze import detect, repo_name, submissions, SKIP


def request(endpoint,raw=False):
    args=['gh','api',endpoint]
    if raw:args+=['-H','Accept: application/vnd.github.raw+json']
    p=subprocess.run(args,capture_output=True,timeout=60)
    if p.returncode:return None
    return p.stdout.decode(errors='replace') if raw else json.loads(p.stdout)


def recover(output,rows):
    last=sorted(rows,key=lambda r:(r['project_slug'],r['id']))[-1]
    repo=repo_name(last['github_link']);ref=str(last.get('commit_id') or '').strip()
    key=hashlib.sha256((repo.lower()+'@'+ref).encode()).hexdigest()[:20]
    dest=output/'cache/scans'/(key+'.json');old=json.loads(dest.read_text())
    if old['status']=='scanned' or not re.search('150 MB|60 MB',old['notes']):return
    tree=request(f'repos/{repo}/git/trees/{ref or "HEAD"}?recursive=1')
    if not tree or tree.get('truncated'):return
    parts=urlparse(last['github_link']).path.strip('/').split('/')
    scope=unquote('/'.join(parts[4:])).rstrip('/') if len(parts)>4 and parts[2]=='tree' else ''
    nodes=[n for n in tree['tree'] if n['type']=='blob' and n.get('size',0)<=500_000 and not any(p in SKIP for p in Path(n['path']).parts) and (not scope or n['path'].startswith(scope+'/')) and (Path(n['path']).suffix.lower() in {'.py','.yml','.yaml','.toml','.txt','.sh','.tf','.md','.xml'} or 'dockerfile' in n['path'].lower() or 'crontab' in n['path'].lower())]
    if len(nodes)>250:return
    files=[]
    for n in nodes:
        text=request(f'repos/{repo}/contents/{quote(n["path"])}?ref={quote(ref or "HEAD")}',raw=True)
        if text is None:return
        files.append((n['path'],text))
    ev,weak,inventory=detect(files)
    old.update(status='scanned',evidence=ev,weak=weak,files=inventory,readme='\n'.join(t[:18000] for p,t in files if Path(p).name.lower()=='readme.md')[:35000],notes=f'Recovered oversized archive via recursive tree and {len(files)} source/config files <=500 KB; SQL/data files excluded')
    dest.write_text(json.dumps(old));print(repo,len(files),list(ev),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(lambda rows:recover(a.output,rows),submissions(a.output).values()))
