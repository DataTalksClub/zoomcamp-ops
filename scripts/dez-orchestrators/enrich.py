#!/usr/bin/env python3
"""Budget-guarded Treg calls, with a durable micro-USD cost ledger.

Catalog metadata must be reviewed before using this helper. Pass a conservative
reservation ceiling for each call; unresolved network outcomes block further spend.
"""
import argparse
from decimal import Decimal
import json
import os
from pathlib import Path
import subprocess
import uuid

CAP_MICRO = 10_000_000


def call(output, tool, body, reserve_usd, query=None):
    ledger_path = output / 'treg-ledger.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else []
    if any(x['charged_micro'] is None for x in ledger):
        raise ValueError('Unsettled call in ledger; reconcile before more spending')
    spent = sum(x['charged_micro'] for x in ledger)
    reserve = int(Decimal(str(reserve_usd)) * 1_000_000)
    if reserve < 0 or spent + reserve > CAP_MICRO:
        raise ValueError('Reservation would exceed $10 hard cap')
    ident = str(uuid.uuid4())
    entry = dict(tool=tool, request_id=ident, reserved_micro=reserve,
                 charged_micro=None, body=body, query=query)
    ledger.append(entry)
    ledger_path.write_text(json.dumps(ledger, indent=2))
    env = os.environ.copy()
    env['TREG_TOKEN'] = Path('/tmp/treg-api-key').read_text().strip()
    cli = str(Path.home() / '.local/bin/treg')
    args = [cli, '--json', 'call', tool, '-H',
            'X-Treg-Route-Max-Cost: ' + str(reserve_usd),
            '-H', 'Idempotency-Key: ' + ident]
    if body is not None:
        args += ['--method', 'POST', '--data', json.dumps(body)]
    for k, v in (query or {}).items():
        args += ['--query', str(k) + '=' + str(v)]
    p = subprocess.run(args, env=env, capture_output=True, text=True, timeout=180)
    raw = output / 'cache' / ('treg-result-' + ident + '.json')
    raw.write_text(p.stdout)
    raw.chmod(0o600)
    data = json.loads(p.stdout)
    cost = data.get('_treg', {}).get('charged_micro')
    entry.update(charged_micro=cost, result_file=str(raw),
                 call_id=data.get('_treg', {}).get('call_id'),
                 http_status=data.get('_treg', {}).get('http_status'))
    ledger_path.write_text(json.dumps(ledger, indent=2))
    print(json.dumps({'tool': tool, 'charged_micro': cost,
                      'total_micro': sum(x['charged_micro'] or 0 for x in ledger),
                      'result_file': str(raw)}))
    return data


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--tool', required=True)
    p.add_argument('--body', type=Path)
    p.add_argument('--query', type=Path)
    p.add_argument('--reserve-usd', type=Decimal, required=True)
    a = p.parse_args()
    call(a.output, a.tool, json.loads(a.body.read_text()) if a.body else None,
         a.reserve_usd, json.loads(a.query.read_text()) if a.query else None)
