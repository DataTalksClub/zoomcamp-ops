#!/usr/bin/env python3
"""Course-agnostic static scan of submitted project repositories against JSON tool sets.

Archives are fetched with authenticated `gh` at the submitted commit and read in memory;
no project code is extracted to disk or executed.
"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
import time
from urllib.parse import urlparse, unquote

# Vendored dbt packages and their CI/integration fixtures mention every warehouse; never count them.
SKIP = {'node_modules', '.venv', 'venv', '.git', 'site-packages', '__pycache__', 'dbt_packages', 'dbt_modules', 'integration_tests', 'jsonschemas'}
TEXT_EXT = {'.py', '.yaml', '.yml', '.toml', '.txt', '.cfg', '.ini', '.json', '.md', '.rst', '.sh', '.tf',
            '.sql', '.properties', '.xml', '.scala', '.ipynb', '.env.example', '.conf', '.hcl'}
DEP_FILES = ('requirements.txt', 'pyproject.toml', 'setup.py', 'setup.cfg', 'Pipfile', 'environment.yml')
DOC_RE = re.compile(r'(^|/)(?:notes|homework|homeworks|cohorts|tutorials)(/|$)', re.I)
EXCLUDE_RE = re.compile(r'(?:^|/)(?:hw(?:[0-9_-]|/)|homeworks?(?:/|[-_0-9])|(?:0[1-9]|[1-9])[ _-](?:docker|workflow|orchestrat|data|analytics|batch|stream|terraform)|cohorts/|tutorials/)', re.I)
LIMIT_FILE, LIMIT_TOTAL, LIMIT_ARCHIVE = 2_000_000, 60_000_000, 150_000_000


def repo_name(link):
    """Accept only GitHub repository URLs; remove tree/blob and other suffixes."""
    try:
        u = urlparse(str(link).strip())
        if u.hostname not in ('github.com', 'www.github.com'):
            return ''
        parts = u.path.strip('/').split('/')
        if len(parts) < 2 or not all(re.fullmatch(r'[\w.-]+', p) for p in parts[:2]):
            return ''
        return '/'.join(parts[:2]).removesuffix('.git')
    except ValueError:
        return ''


def safe(s):
    s = re.sub(r'https?://[^\s]+', '[URL]', s)
    s = re.sub(r'[\w.+-]+@[\w.-]+', '[email removed]', s)
    if re.search(r'(?:secret|password|token|api.key|private.key)\s*[:=]', s, re.I):
        return '[credential-like line omitted]'
    return ' '.join(s.split())[:200]


def load_toolsets(paths):
    sets = []
    for p in paths:
        d = json.loads(Path(p).read_text())
        d['_mention'] = re.compile(d['mention_regex'], re.I) if d.get('mention_regex') else None
        for t in d['tools'].values():
            t['_re'] = [re.compile(x, re.I | re.M) for x in t.get('patterns', [])]
        sets.append(d)
    return sets


def is_text(path):
    low = path.lower()
    return Path(path).suffix.lower() in TEXT_EXT or 'dockerfile' in low or 'crontab' in low or low.endswith('docker-compose.yml')


def detect(files, toolset):
    """Return ({label: [evidence]}, weak_mentions) for one tool set."""
    evidence, weak = defaultdict(list), []
    for path, content in files:
        if any(p in SKIP for p in Path(path).parts) or not is_text(path):
            continue
        if re.search(r'(^|/)(?:uv|poetry|package|Pipfile)\.lock$|package-lock.json', path):
            continue
        if Path(path).suffix.lower() in {'.md', '.rst'} or DOC_RE.search(path):
            if toolset['_mention']:
                for line in content.splitlines():
                    if toolset['_mention'].search(line) and len(weak) < 15:
                        weak.append(path + ': ' + safe(line))
            continue
        name = Path(path).name
        for label, t in toolset['tools'].items():
            if len(evidence[label]) >= 4:
                continue
            for rx in t['_re']:
                m = rx.search(content)
                if m:
                    evidence[label].append(f"{path}:{content[:m.start()].count(chr(10)) + 1}: " + safe(m.group(0)))
                    break
            if name in DEP_FILES:
                for pkg in t.get('packages', []):
                    if re.search(r'(?:^|[\s"\'\[,])' + re.escape(pkg) + r'(?:[\s"\'\],=<>~!\[;]|$)', content, re.M | re.I):
                        evidence[label].append(f'{path}: dependency {pkg}')
                        break
            for rule in t.get('file_rules', []):
                if re.search(rule['path'], path, re.I) and all(re.search(c, content, re.I | re.M) for c in rule.get('content_all', [])):
                    evidence[label].append(f"{path}: {rule['label']}")
    return {k: v for k, v in evidence.items() if v}, weak


def apply_implies(evidence, toolset):
    for label, implied in toolset.get('implies', {}).items():
        if label in evidence:
            for other in implied:
                evidence.setdefault(other, []).append(f'{label} implies {other}')
    return evidence


def read_archive(repo, ref):
    archive = tempfile.TemporaryFile()
    proc = subprocess.run(['gh', 'api', f'repos/{repo}/tarball' + ('/' + ref if re.fullmatch('[0-9a-fA-F]{7,40}', ref) else '')],
                          stdout=archive, stderr=subprocess.PIPE, timeout=180)
    size = archive.tell()
    archive.seek(0)
    if proc.returncode:
        raise OSError('GitHub archive inaccessible: ' + safe(proc.stderr.decode(errors='replace'))[:240])
    if size > LIMIT_ARCHIVE:
        raise ValueError('Archive exceeds 150 MB scan limit')
    files, total = [], 0
    with tarfile.open(fileobj=archive, mode='r|gz') as tar:
        for member in tar:
            if not member.isfile():
                continue
            path = member.name.split('/', 1)[-1]
            if member.size > LIMIT_FILE or any(p in SKIP for p in Path(path).parts) or not is_text(path):
                continue
            total += member.size
            if total > LIMIT_TOTAL:
                raise ValueError('Text scan exceeds 60 MB limit')
            data = tar.extractfile(member).read()
            if b'\0' not in data:
                files.append((path, data.decode('utf-8', errors='replace')))
    archive.close()
    return files


def scope_of(link):
    parts = urlparse(link).path.strip('/').split('/')
    scope = unquote('/'.join(parts[4:])).rstrip('/') if len(parts) > 4 and parts[2] in ('tree', 'blob') else ''
    if len(parts) > 4 and parts[2] == 'blob':
        scope = str(Path(scope).parent) if '/' in scope else ''
    return scope


def relevant(item, scope):
    path = item.split(':', 1)[0]
    if scope:
        return path == scope or path.startswith(scope + '/')
    return not EXCLUDE_RE.search(path)


def scan_one(output, rows, toolsets):
    rows = sorted(rows, key=lambda r: (r['project_slug'], r['id']))
    last = rows[-1]
    repo = repo_name(last['github_link'])
    ref = str(last.get('commit_id') or '').strip()
    key = hashlib.sha256((repo.lower() + '@' + ref + '@' + '+'.join(t['name'] + str(t.get('version', 1)) for t in toolsets)).encode()).hexdigest()[:20]
    cache = output / 'cache' / 'scans-v2'
    cache.mkdir(parents=True, exist_ok=True)
    dest = cache / (key + '.json')
    if dest.exists():
        result = json.loads(dest.read_text())
    else:
        result = {'status': 'unknown', 'sets': {}, 'files': [], 'notes': ''}
        if not repo:
            result['notes'] = 'No valid GitHub repository URL'
        else:
            try:
                for attempt in range(40):
                    try:
                        files = read_archive(repo, ref)
                        break
                    except OSError as e:
                        # Never cache a rate-limit failure: wait for the quota to reset and retry.
                        if 'rate limit' not in str(e).lower() or attempt == 39:
                            raise
                        time.sleep(60)
                for ts in toolsets:
                    ev, weak = detect(files, ts)
                    result['sets'][ts['name']] = {'evidence': ev, 'weak': weak}
                result.update(status='scanned', files=[p for p, _ in files])
            except (subprocess.TimeoutExpired, tarfile.TarError, ValueError, OSError) as e:
                result['notes'] = type(e).__name__ + ': ' + safe(str(e))
        dest.write_text(json.dumps(result))
    scope = scope_of(last['github_link'])
    status, notes = result['status'], result['notes']
    if scope:
        notes += ' Submitted project scope: ' + scope
        if status == 'scanned' and not any(p == scope or p.startswith(scope + '/') for p in result['files']):
            status, notes = 'unknown', notes + '; submitted directory has no scanned files at this commit'
    out = dict(repo=repo, year=last['year'], course_slug=last['course_slug'],
               project_slug=';'.join(sorted({r['project_slug'] for r in rows})), github_link=last['github_link'],
               commit_id=ref, submission_rows=len(rows), student_ids=';'.join(sorted({str(r['student_id']) for r in rows})),
               project_score=max((r.get('project_score') or 0 for r in rows)), status=status, notes=notes.strip(), scan_cache=key)
    for ts in toolsets:
        s = result['sets'].get(ts['name'], {'evidence': {}, 'weak': []})
        ev = {k: [e for e in v if relevant(e, scope)] for k, v in s['evidence'].items()}
        ev = apply_implies({k: v for k, v in ev.items() if v}, ts) if status == 'scanned' else {}
        labels = sorted(ev)
        out[ts['name']] = ';'.join(labels) if labels else ('none' if status == 'scanned' else 'unknown')
        out[ts['name'] + '_evidence'] = json.dumps(ev, ensure_ascii=False)
        out[ts['name'] + '_weak'] = json.dumps(s['weak'], ensure_ascii=False)
    return out


def project_groups(output):
    groups = defaultdict(list)
    for p in sorted((output / 'cache').glob('submissions-*.json')):
        _, year, slug = p.stem.split('-', 2)
        d = json.loads(p.read_text())
        for row in d['submissions']:
            row = dict(row, year=year, course_slug=d['course'], project_slug=slug)
            repo = repo_name(row['github_link'])
            groups[(year, repo.lower() if repo else 'invalid:' + str(row['id']))].append(row)
    return groups


def scan(output, toolset_paths, workers=6):
    toolsets = load_toolsets(toolset_paths)
    groups = project_groups(output)
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(scan_one, output, rows, toolsets) for rows in groups.values()]
        for i, f in enumerate(as_completed(futures), 1):
            results.append(f.result())
            if i % 50 == 0:
                print(f'Scanned {i}/{len(groups)}', flush=True)
    results.sort(key=lambda r: (r['year'], r['repo'].lower(), r['github_link']))
    years = sorted({r['year'] for r in results})
    counts = {}
    for ts in toolsets:
        cols = ['repo', 'year', 'course_slug', 'project_slug', 'github_link', 'commit_id', 'submission_rows',
                'project_score', 'status', 'notes', ts['name'], ts['name'] + '_evidence', ts['name'] + '_weak', 'scan_cache']
        with (output / f"{ts['name']}.csv").open('w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
            w.writeheader()
            w.writerows(results)
        counts[ts['name']] = {y: dict(Counter(t for r in results if r['year'] == y for t in r[ts['name']].split(';'))) for y in years}
    # Private join table repo -> student ids (no emails) for audience aggregates.
    priv = output / 'cache' / 'repo-students.json'
    priv.write_text(json.dumps([{k: r[k] for k in ('repo', 'year', 'student_ids', 'status')} | {ts['name']: r[ts['name']] for ts in toolsets} for r in results]))
    priv.chmod(0o600)
    (output / 'scan-counts.json').write_text(json.dumps(counts, indent=2))
    return counts
