#!/usr/bin/env python3
"""Budget-guarded Treg calls with a durable micro-USD ledger (thread-safe).

Every call reserves its per-call ceiling before it starts. A call is refused when
spent + open reservations + this reservation would pass the stop threshold, so the
hard cap can never be crossed even with parallel workers. A call whose charge is
unknown (crash, timeout) stays unsettled and blocks new spend until reconciled.
"""
from decimal import Decimal
import json
import os
from pathlib import Path
import fcntl
import subprocess
import threading
import uuid

KEY_FILE = Path(os.environ.get('TREG_KEY_FILE', '/tmp/treg-api-key'))
CLI = os.environ.get('TREG_CLI', str(Path.home() / '.local/bin/treg'))


class BudgetExceeded(Exception):
    pass


class Ledger:
    def __init__(self, output, cap_usd=10.0, stop_usd=9.0):
        self.path = output / 'treg-ledger.json'
        self.cache = output / 'cache'
        self.cap = int(Decimal(str(cap_usd)) * 1_000_000)
        self.stop = min(int(Decimal(str(stop_usd)) * 1_000_000), self.cap)
        self.lock = threading.Lock()
        # One spending process per report directory: a second process would see the first one's
        # open reservations as unsettled and must never rewrite its ledger.
        self._flock = open(output / 'treg-ledger.lock', 'w')
        try:
            fcntl.flock(self._flock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise BudgetExceeded('Another Treg spending process holds the ledger lock')
        self.entries = json.loads(self.path.read_text()) if self.path.exists() else []
        self.open = {}

    def spent(self):
        return sum(x['charged_micro'] or 0 for x in self.entries)

    def _save(self):
        tmp = self.path.with_suffix('.tmp')
        tmp.write_text(json.dumps(self.entries, indent=1))
        tmp.replace(self.path)

    def reserve(self, tool, body, reserve_usd, label=''):
        reserve = int(Decimal(str(reserve_usd)) * 1_000_000)
        with self.lock:
            if any(x['charged_micro'] is None and x['request_id'] not in self.open for x in self.entries):
                raise BudgetExceeded('Unsettled call in ledger; reconcile before more spending')
            if self.spent() + sum(self.open.values()) + reserve > self.stop:
                raise BudgetExceeded(f'Stop threshold reached: spent {self.spent()/1e6:.4f} USD')
            ident = str(uuid.uuid4())
            self.entries.append(dict(tool=tool, request_id=ident, reserved_micro=reserve, charged_micro=None,
                                     label=label, body=body))
            self.open[ident] = reserve
            self._save()
            return ident

    def settle(self, ident, charged, call_id, status, result_file):
        with self.lock:
            e = next(x for x in self.entries if x['request_id'] == ident)
            e.update(charged_micro=charged, call_id=call_id, http_status=status, result_file=str(result_file))
            self.open.pop(ident, None)
            self._save()

    def reconcile(self):
        """Replay unsettled calls with their own Idempotency-Key (treg returns the stored answer, no new charge).
        A replay does not reveal the first charge, so it is recorded at the reserved ceiling (conservative)."""
        settled, pending = 0, 0
        env = os.environ.copy()
        env['TREG_TOKEN'] = KEY_FILE.read_text().strip()
        for e in [x for x in self.entries if x['charged_micro'] is None]:
            args = [CLI, '--json', 'call', e['tool'], '-H', 'Idempotency-Key: ' + e['request_id']]
            if e.get('body') is not None:
                args += ['--method', 'POST', '--data', json.dumps(e['body'])]
            p = subprocess.run(args, env=env, capture_output=True, text=True, timeout=240)
            try:
                data = json.loads(p.stdout)
            except ValueError:
                pending += 1
                continue
            meta = data.get('_treg', {})
            status = meta.get('http_status')
            if status == 409:
                pending += 1
                continue
            raw = self.cache / f"treg-result-{e['request_id']}.json"
            raw.write_text(p.stdout)
            raw.chmod(0o600)
            charged = e['reserved_micro'] if status and status < 400 else 0
            e['notes'] = 'reconciled by idempotent replay; charge recorded at reserved ceiling' if charged else 'reconciled: provider error, not billed'
            self.settle(e['request_id'], charged, meta.get('call_id'), status, raw)
            if e.get('label', '').startswith('li-search:') and status and status < 400:
                dest = self.cache / ('li-search-' + e['label'].split(':', 1)[1] + '.json')
                dest.write_text(json.dumps(data.get('result')))
                dest.chmod(0o600)
            settled += 1
        return {'settled': settled, 'pending': pending, 'spent_usd': self.spent() / 1e6}

    def call(self, tool, body, reserve_usd, label='', query=None):
        """Run one catalog call. Returns the provider body (dict) or None on failure."""
        ident = self.reserve(tool, body, reserve_usd, label)
        env = os.environ.copy()
        env['TREG_TOKEN'] = KEY_FILE.read_text().strip()
        args = [CLI, '--json', 'call', tool, '-H', f'X-Treg-Route-Max-Cost: {reserve_usd}', '-H', 'Idempotency-Key: ' + ident]
        if body is not None:
            args += ['--method', 'POST', '--data', json.dumps(body)]
        for k, v in (query or {}).items():
            args += ['--query', f'{k}={v}']
        raw = self.cache / f'treg-result-{ident}.json'
        try:
            p = subprocess.run(args, env=env, capture_output=True, text=True, timeout=240)
        except subprocess.TimeoutExpired:
            # Charge unknown: leave unsettled so spending stops until reconciled with the same key.
            with self.lock:
                self.open.pop(ident, None)
            raise BudgetExceeded('Timeout with unknown charge; reconcile call ' + ident)
        raw.write_text(p.stdout)
        raw.chmod(0o600)
        try:
            data = json.loads(p.stdout)
        except ValueError:
            # The CLI failed before a provider answer (refused/4xx without JSON): treg does not bill these.
            self.settle(ident, 0, None, None, raw)
            return None
        meta = data.get('_treg', {})
        charged = meta.get('charged_micro')
        self.settle(ident, int(charged or 0), meta.get('call_id'), meta.get('http_status'), raw)
        return data.get('result')
