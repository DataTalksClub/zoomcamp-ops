#!/usr/bin/env python3
"""Audit CMP final-project repositories without executing untrusted repository code."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import urllib.request
from urllib.parse import urlparse, unquote

BASE = 'https://courses.datatalks.club/api'
TOOLS = {
 'Kestra': r'io\.kestra\.|kestra/(?:kestra|kestra-ee)|image:\s*kestra',
 'Airflow': r'\bfrom\s+airflow\b|\bimport\s+airflow\b|apache-airflow|apache/airflow|airflow standalone',
 'Astronomer': r'astrocrpublic\.azurecr\.io|quay\.io/astronomer|astronomer/astro-runtime|FROM\s+astro',
 'Dagster': r'\bfrom\s+dagster\b|\bimport\s+dagster\b|dagster-webserver|dagster dev|dagster/api',
 'Prefect': r'\bfrom\s+prefect\b|\bimport\s+prefect\b|prefecthq/prefect|prefect deploy|prefect server',
 'Mage': r'\bfrom\s+mage_ai\b|\bimport\s+mage_ai\b|mageai/mageai|mage_ai start',
 'Luigi': r'\bimport\s+luigi\b|\bfrom\s+luigi\b',
 'Argo Workflows': r'argoproj.io/v1alpha1[\s\S]*?kind:\s*(?:Workflow|CronWorkflow)',
 'AWS Step Functions': r'aws_sfn_state_machine|aws-stepfunctions|aws_stepfunctions|"StartAt"\s*:',
 'Azure Data Factory': r'Microsoft.DataFactory/factories|azurerm_data_factory_pipeline',
 'Flyte': r'\bfrom\s+flytekit\b|\bimport\s+flytekit\b',
 'Temporal': r'\bfrom\s+temporalio\b|\bimport\s+temporalio\b',
 'Hamilton': r'\bfrom\s+hamilton\b|\bimport\s+hamilton\b',
 'Databricks Workflows': r'databricks_job|\bjob_clusters:',
}
MENTIONS = re.compile(r'\b(kestra|airflow|astronomer|dagster|prefect|mage|luigi|orchestrat\w*|cron|nifi|windmill|azkaban|oozie|step functions|data factory)\b', re.I)
SKIP = {'node_modules','.venv','venv','.git','site-packages','__pycache__'}
TEXT_EXT = {'.py','.yaml','.yml','.toml','.txt','.cfg','.ini','.json','.md','.rst','.sh','.tf','.sql','.properties','.xml','.scala'}


def repo_name(link):
    """Accept only GitHub repository URLs; remove tree/blob and other suffixes."""
    try:
        u=urlparse(str(link).strip())
        if u.hostname not in ('github.com','www.github.com'): return ''
        parts=u.path.strip('/').split('/')
        if len(parts)<2 or not all(re.fullmatch(r'[\w.-]+', p) for p in parts[:2]): return ''
        return '/'.join(parts[:2]).removesuffix('.git')
    except ValueError: return ''


def gh(args, **kwargs):
    return subprocess.run(['gh',*args], env=os.environ.copy(), capture_output=True, timeout=150, **kwargs)


def cmp_get(path):
    req=urllib.request.Request(BASE+path,headers={'Authorization':'Token '+os.environ['AUTH_TOKEN']})
    with urllib.request.urlopen(req,timeout=60) as r: return json.load(r)


def fetch(output):
    cache=output/'cache';cache.mkdir(parents=True,exist_ok=True)
    for year in (2025,2026):
        course=cmp_get(f'/courses/de-zoomcamp-{year}/')
        (cache/f'course-{year}.json').write_text(json.dumps(course))
        for project in course['projects']:
            if not re.search(r'project|capstone|final',project['title'],re.I) or re.search('midterm',project['title'],re.I): continue
            slug=project['slug']
            data=cmp_get(f'/courses/de-zoomcamp-{year}/projects/{slug}/submissions')
            if not isinstance(data,dict) or not isinstance(data.get('submissions'),list):
                raise ValueError('Unexpected CMP envelope; inspect pagination before proceeding')
            # Deduplication identifiers stay only in the private cache. Never persist emails.
            clean={'course':data['course'],'project':data['project'],'submissions':[
                {k:r.get(k) for k in ('id','student_id','github_link','commit_id','project_score','total_score','passed')} for r in data['submissions']]}
            p=cache/f'submissions-{year}-{slug}.json';p.write_text(json.dumps(clean));p.chmod(0o600)


def submissions(output):
    groups=defaultdict(list)
    for p in sorted((output/'cache').glob('submissions-*.json')):
        _,year,slug=p.stem.split('-',2)
        for row in json.loads(p.read_text())['submissions']:
            row=dict(row,year=year,course_slug='de-zoomcamp-'+year,project_slug=slug)
            repo=repo_name(row['github_link'])
            groups[(year,repo.lower() if repo else 'invalid:'+str(row['id']))].append(row)
    return groups


def detect(files):
    evidence=defaultdict(list); weak=[]; inventory=[]
    for path,content in files:
        inventory.append(path)
        if any(p in SKIP for p in Path(path).parts): continue
        if Path(path).suffix.lower() not in TEXT_EXT and 'dockerfile' not in path.lower() and 'crontab' not in path.lower(): continue
        if re.search(r'(^|/)(?:uv|poetry|package)\.lock$|package-lock.json',path): continue
        # README and notebooks/course notes cannot establish executable use.
        docs=Path(path).suffix.lower() in {'.md','.rst'} or bool(re.search(r'(^|/)(?:notes|homework|homeworks|cohorts|tutorials)(/|$)',path,re.I))
        if docs:
            for line in content.splitlines():
                if MENTIONS.search(line) and len(weak)<15: weak.append(path+': '+safe(line))
            continue
        for tool,pattern in TOOLS.items():
            m=re.search(pattern,content,re.I)
            if m and len(evidence[tool])<4:
                line=content[:m.start()].count('\n')+1
                evidence[tool].append(f'{path}:{line}: '+safe(m.group(0)))
        if Path(path).name in ('prefect.yaml','prefect.yml') and re.search(r'^deployments:',content,re.M): evidence['Prefect'].append(path+': deployments config')
        if Path(path).name=='dagster.yaml': evidence['Dagster'].append(path+': instance config')
        if Path(path).name=='metadata.yaml' and 'blocks:' in content and 'executor_type:' in content: evidence['Mage'].append(path+': pipeline blocks/executor config')
        if Path(path).name in ('requirements.txt','pyproject.toml','setup.py','setup.cfg'):
            for tool,pkg in [('Airflow','apache-airflow'),('Dagster','dagster'),('Prefect','prefect'),('Mage','mage-ai'),('Luigi','luigi')]:
                if re.search(r'(?:^|[\s"\'\[])'+re.escape(pkg)+r'(?:[\s"\'\]=<>~!\[]|$)',content,re.M|re.I): evidence[tool].append(path+': dependency '+pkg)
    if 'Astronomer' in evidence: evidence.setdefault('Airflow',[]).append('Astronomer runtime implies Airflow')
    return dict(evidence),weak,inventory


def safe(s):
    # Store the matched technology signal, never adjacent credential values.
    s=re.sub(r'https?://[^\s]+','[URL]',s)
    s=re.sub(r'[\w.+-]+@[\w.-]+','[email removed]',s)
    if re.search(r'(?:secret|password|token|api.key|private.key)\s*[:=]',s,re.I): return '[credential-like line omitted]'
    return ' '.join(s.split())[:200]


def scan_one(output,items):
    rows=sorted(items,key=lambda r:(r['project_slug'],r['id']));last=rows[-1]
    repo=repo_name(last['github_link']); ref=str(last.get('commit_id') or '').strip()
    key=hashlib.sha256((repo.lower()+'@'+ref).encode()).hexdigest()[:20]
    cache=output/'cache'/'scans';cache.mkdir(exist_ok=True)
    dest=cache/(key+'.json')
    if dest.exists(): result=json.loads(dest.read_text())
    else:
        result={'status':'unknown','evidence':{},'weak':[],'files':[],'notes':'','ref':ref}
        if not repo: result['notes']='No valid GitHub repository URL'
        else:
            try:
                # gh handles host auth and follows the archive redirect. No untrusted files extracted.
                proc=gh(['api',f'repos/{repo}/tarball'+('/'+ref if re.fullmatch('[0-9a-fA-F]{7,40}',ref) else '')])
                if proc.returncode:
                    result['notes']='GitHub archive inaccessible: '+safe(proc.stderr.decode(errors='replace'))[:240]
                elif len(proc.stdout)>150_000_000: result['notes']='Archive exceeds 150 MB scan limit'
                else:
                    files=[];total=0
                    with tarfile.open(fileobj=io.BytesIO(proc.stdout),mode='r:gz') as tar:
                        for member in tar:
                            if not member.isfile(): continue
                            path=member.name.split('/',1)[-1]
                            if member.size>2_000_000 or any(p in SKIP for p in Path(path).parts): continue
                            if Path(path).suffix.lower() not in TEXT_EXT and 'dockerfile' not in path.lower() and 'crontab' not in path.lower(): continue
                            total+=member.size
                            if total>60_000_000: raise ValueError('Text scan exceeds 60 MB limit')
                            data=tar.extractfile(member).read()
                            if b'\0' not in data: files.append((path,data.decode('utf-8',errors='replace')))
                    ev,weak,inventory=detect(files)
                    result.update(status='scanned',evidence=ev,weak=weak,files=inventory,notes='',readme='\n'.join(t[:18000] for p,t in files if Path(p).name.lower()=='readme.md')[:35000])
            except (subprocess.TimeoutExpired,tarfile.TarError,ValueError,OSError) as e: result['notes']=type(e).__name__+': '+safe(str(e))
        dest.write_text(json.dumps(result))
    # Ignore teaching modules and respect a submitted tree/blob project directory.
    result=json.loads(json.dumps(result))
    parts=urlparse(last['github_link']).path.strip('/').split('/')
    scope=unquote('/'.join(parts[4:])).rstrip('/') if len(parts)>4 and parts[2] in ('tree','blob') else ''
    def relevant(item):
        path=item.split(':',1)[0]
        if item=='Astronomer runtime implies Airflow': return True
        if scope: return path==scope or path.startswith(scope+'/')
        return not re.search(r'(?:^|/)(?:hw(?:[0-9_-]|/)|homeworks?(?:/|[-_0-9])|(?:0[1-9]|[1-9])[ _-](?:docker|workflow|orchestrat|data|analytics|batch|stream|terraform)|cohorts/|tutorials/)',path,re.I)
    filtered={tool:[e for e in entries if relevant(e)] for tool,entries in result['evidence'].items()}
    result['evidence']={tool:entries for tool,entries in filtered.items() if entries}
    if 'Astronomer' not in result['evidence'] and result['evidence'].get('Airflow')==['Astronomer runtime implies Airflow']:
        del result['evidence']['Airflow']
    if scope: result['notes']+=' Submitted project scope: '+scope
    tools=sorted(result['evidence'])
    return dict(repo=repo,year=last['year'],course_slug=last['course_slug'],project_slug=';'.join(sorted({r['project_slug'] for r in rows})),github_link=last['github_link'],**{'orchestrator(s)':';'.join(tools) if tools else ('none' if result['status']=='scanned' else 'unknown')},evidence=json.dumps(result['evidence'],ensure_ascii=False),notes=result['notes'],weak_mentions=json.dumps(result['weak'],ensure_ascii=False),commit_id=ref,submission_rows=len(rows),project_score=max((r.get('project_score') or 0 for r in rows)),scan_cache=key,status=result['status'])


def scan(output,workers):
    groups=submissions(output);results=[]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(scan_one,output,rows) for rows in groups.values()]
        for i,f in enumerate(as_completed(futures),1):
            results.append(f.result())
            if i%25==0: print(f'Scanned {i}/{len(groups)}',flush=True)
    results.sort(key=lambda r:(r['year'],r['repo'].lower(),r['github_link']))
    with (output/'orchestrators.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    counts={y:Counter(t for r in results if r['year']==y for t in r['orchestrator(s)'].split(';')) for y in ('2025','2026')}
    (output/'counts.json').write_text(json.dumps(counts,indent=2));print(json.dumps(counts,indent=2))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['fetch','scan']);p.add_argument('--output',type=Path,required=True);p.add_argument('--workers',type=int,default=4);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    if a.action=='fetch': fetch(a.output)
    else: scan(a.output,a.workers)

if __name__=='__main__':main()
