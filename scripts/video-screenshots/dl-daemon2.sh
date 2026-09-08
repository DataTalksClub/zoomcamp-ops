#!/bin/bash
# Orchestrator for LLM-zoomcamp screenshot backfill downloads (v2, by worker_2).
# Changes vs dl-daemon.sh:
#  - subtitles: handles BOTH WebVTT and TTML (piped/invidious serve either);
#    previous version silently failed to cache TTML subs.
#  - instance lists expanded + ordered by tonight's probe results.
#  - downloads sent with a browser User-Agent (some piped-proxy hosts 403 curl's UA).
#  - on curl download failure the stored URL is dropped so the next round
#    re-fetches meta from a possibly different instance (rotates proxy hosts).
# Same conventions: dl/ state files (done-, meta-, dl-.url, subs-.vtt),
# <=2 mp4 on disk, flock on .daemon.lock, transcripts -> shared cache.
SCRATCH=/home/alexey/git/.tmp/notes-work/llm-zoomcamp
DL=$SCRATCH/dl
CACHE=/home/alexey/.cache/youtube_transcripts
LOG=$SCRATCH/dl.log
PIPEDED="api.piped.projectsegfau.lt api.piped.private.coffee pipedapi.ducks.party pipedapi.drgns.space piped-api.codespace.cz pipedapi.kavin.rocks api.piped.privacydev.net pipedapi.reallyaweso.me pipedapi.adminforge.de pipedapi.orangenet.cc pipedapi.nosebs.ru pipedapi.leptons.xyz piped-api.lunar.icu"
INVID="invidious.protokolla.fi invidious.privacydev.net invidious.projectsegfau.lt invidious.private.coffee invidious.adminforge.de invidious.reallyaweso.me invidious.drgns.space inv.nadeko.net yewtu.be invidious.nerdvpn.de iv.melmac.space invidious.f5.si invidious.privacyredirect.com iv.ggtyler.dev invidious.jing.rocks invidious.materialio.us inv.zzls.xyz iv.duti.dev invidious.dhusch.de invidious.perennialte.ch"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
cd "$DL" || exit 1
exec 9>"$SCRATCH/.daemon.lock"
flock -n 9 || { echo "daemon2 already running" >> "$LOG"; exit 0; }

log() { echo "[$(date +%H:%M:%S)] $*" >> "$LOG"; }

vids() { awk '{print $1}' "$SCRATCH/queue.txt"; }

mp4_count() { find "$SCRATCH" -name '*.mp4' -size +1M 2>/dev/null | wc -l; }

all_done() {
  local n=0
  while read -r v; do [ -f "done-$v" ] || return 1; done < <(vids)
  return 0
}

subs_to_cache() {
  # $1 = source file (webvtt or ttml), $2 = dest cache txt
  python3 - "$1" "$2" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
txt = open(src, encoding='utf-8', errors='replace').read()
out, seen_ts = [], set()

def emit(sec, text):
    if not text:
        return
    if sec in seen_ts:
        return
    seen_ts.add(sec)
    ts = f"{sec//60}:{sec%60:02}"
    out.append(f"{ts} {text}")

if re.search(r'<tt[\s>]', txt) or '<p begin=' in txt:
    # TTML (invidious captions): rolling windows, merge continuation lines
    for m in re.finditer(r'<p begin="(?:(\d+):)?(\d+):(\d+)\.(\d+)"[^>]*>(.*?)</p>', txt, re.S):
        h, mi, s, _ms, body = m.groups()
        h = int(h or 0)
        sec = h * 3600 + int(mi) * 60 + int(s)
        text = re.sub(r'<[^>]+>', ' ', body)
        text = re.sub(r'\s+', ' ', text).strip()
        if sec in seen_ts and out:
            # continuation of the rolling window: merge tail
            prev = out[-1].split(' ', 1)
            if len(prev) == 2:
                out[-1] = prev[0] + ' ' + (prev[1] + ' ' + text).strip()
            continue
        emit(sec, text)
else:
    # WebVTT (piped subtitles)
    for block in re.split(r'\n\s*\n', txt):
        lines = [l for l in block.splitlines() if l.strip()]
        ts_line = next((l for l in lines if '-->' in l), None)
        if not ts_line:
            continue
        start = ts_line.split('-->')[0].strip()
        m = re.match(r'(?:(\d+):)?(\d+):(\d+)\.', start)
        if not m:
            continue
        h, mi, s = (int(x or 0) for x in m.groups())
        sec = h * 3600 + mi * 60 + s
        text = ' '.join(
            re.sub(r'<[^>]+>', '', l).strip()
            for l in lines[lines.index(ts_line) + 1:]
        ).strip()
        emit(sec, text)

if len(out) < 5:
    sys.exit(1)
open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f"{dst}: {len(out)} lines")
PY
}

save_subs_piped() {
  local vid="$1"
  local suburl
  suburl=$(python3 -c "
import json
d = json.load(open('meta-$vid.json'))
subs = d.get('subtitles') or []
en = [x for x in subs if x.get('code', '').startswith('en')]
print(en[0]['url'] if en else (subs[0]['url'] if subs else ''))
" 2>/dev/null)
  [ -z "$suburl" ] && return 1
  curl -sL -m 40 -A "$UA" "$suburl" -o "subs-$vid.raw" || return 1
  if subs_to_cache "subs-$vid.raw" "$CACHE/$vid.txt" >/dev/null 2>&1; then
    mv "subs-$vid.raw" "subs-$vid.vtt"
    return 0
  fi
  return 1
}

# Validate a stream URL: small range GET must return 200/206 with a
# non-text content type (rejects dead piped-proxy hosts and block pages).
url_ok() {
  local url="$1" hdr code ctype
  hdr=$(curl -sL -m 20 -A "$UA" -r 0-16384 -o /dev/null -D - -w '\n%{http_code}' "$url" 2>/dev/null | tr -d '\r')
  code=$(printf '%s' "$hdr" | tail -n 1)
  ctype=$(printf '%s' "$hdr" | grep -i '^content-type:' | head -n 1 | cut -d' ' -f2)
  case "$code" in 200|206) ;; *) return 1 ;; esac
  case "$ctype" in text/*|*"text/html"*) return 1 ;; esac
  [ -n "$ctype" ] || return 1
  return 0
}

try_piped() {
  local vid="$1"
  for mirror in $PIPEDED; do
    local code
    code=$(curl -sL -m 20 -A "$UA" -o "meta-$vid.json" -w '%{http_code}' "https://$mirror/streams/$vid")
    if [ "$code" = "200" ] && python3 -c "
import json
d = json.load(open('meta-$vid.json'))
vs = [x for x in d.get('videoStreams', []) if x.get('format') == 'MPEG_4' and x.get('url')]
prog = [x for x in vs if not x.get('videoOnly')]
vo = [x for x in vs if x.get('videoOnly')]
pick = prog[0] if prog else (([x for x in vo if '360' in (x.get('quality') or '')] or vo or [None])[0])
assert pick
open('dl-$vid.url', 'w').write(pick['url'])
open('q-$vid', 'w').write((pick.get('quality') or '') + (' videoOnly' if pick.get('videoOnly') else ''))
" 2>/dev/null; then
      if url_ok "$(cat "dl-$vid.url")"; then
        log "$vid META via piped/$mirror q=$(cat "q-$vid" 2>/dev/null) (validated)"
        save_subs_piped "$vid" && log "$vid SUBS -> cache" || log "$vid no subs via piped"
        return 0
      fi
      rm -f "dl-$vid.url" "q-$vid"
      log "$vid piped/$mirror url failed validation"
    fi
  done
  return 1
}

try_invid() {
  local vid="$1"
  for inst in $INVID; do
    local code
    code=$(curl -sL -m 20 -A "$UA" -o "meta-$vid.json" -w '%{http_code}' "https://$inst/api/v1/videos/$vid")
    if [ "$code" = "200" ] && python3 -c "
import json
d = json.load(open('meta-$vid.json'))
def h(x): return x.get('url')
fs = [x for x in d.get('formatStreams', []) if x.get('container') == 'mp4' and h(x)]
pick = None
if fs: pick = fs[0]
else:
    ad = [x for x in d.get('adaptiveFormats', []) if 'video/mp4' in (x.get('type') or '') and h(x)]
    v360 = [x for x in ad if '360' in (x.get('qualityLabel') or '')]
    pick = (v360 or ad or [None])[0]
assert pick
open('dl-$vid.url', 'w').write(pick['url'])
open('q-$vid', 'w').write((pick.get('qualityLabel') or '') + ' inv')
" 2>/dev/null; then
      if url_ok "$(cat "dl-$vid.url")"; then
        log "$vid META via invidious/$inst q=$(cat "q-$vid" 2>/dev/null) (validated)"
        local capurl
        capurl=$(python3 -c "
import json
d = json.load(open('meta-$vid.json'))
caps = d.get('captions') or []
en = [x for x in caps if x.get('language_code', '').startswith('en')]
print('https://$inst' + (en[0]['url'] if en else (caps[0]['url'] if caps else '')))
" 2>/dev/null)
        if [ -n "$capurl" ]; then
          curl -sL -m 40 -A "$UA" "$capurl" -o "subs-$vid.raw"
          if subs_to_cache "subs-$vid.raw" "$CACHE/$vid.txt" >/dev/null 2>&1; then
            mv "subs-$vid.raw" "subs-$vid.vtt"
            log "$vid SUBS -> cache"
          fi
        fi
        return 0
      fi
      rm -f "dl-$vid.url" "q-$vid"
      log "$vid invidious/$inst url failed validation"
    fi
  done
  return 1
}

download_curl() {
  local vid="$1"
  local out="$vid.mp4"
  [ "$(mp4_count)" -ge 2 ] && return 1
  log "$vid download start (curl)"
  curl -sL -m 1200 --speed-time 30 --speed-limit 10000 -A "$UA" \
    "$(cat "dl-$vid.url")" -o "$out"
  if [ -f "$out" ] && [ "$(stat -c%s "$out")" -gt 1000000 ] \
     && ffprobe -v error -show_entries format=duration -of csv=p=0 "$out" >/dev/null 2>&1; then
    touch "done-$vid"
    log "$vid DL SUCCESS $(stat -c%s "$out")"
    return 0
  fi
  log "$vid DL FAILED (curl)"
  rm -f "$out"
  # drop the dead URL: next round re-fetches meta, likely from another instance
  rm -f "dl-$vid.url"
  echo $(( $(cat "fails-$vid" 2>/dev/null || echo 0) + 1 )) > "fails-$vid"
  return 1
}

download_ytdlp() {
  local vid="$1"
  [ "$(mp4_count)" -ge 2 ] && return 1
  set -a; . /home/alexey/.config/youtube/.env; set +a
  local sid=$(( (RANDOM * RANDOM + RANDOM) % 1000000000 ))
  local proxy="http://customer-${OXYLABS_USER}-sessid-${sid}:$(python3 -c 'from urllib.parse import quote; import os; print(quote(os.environ["OXYLABS_PASSWORD"], safe=""))')@${OXYLABS_ENDPOINT}"
  log "$vid download start (yt-dlp proxy sid=$sid)"
  yt-dlp --proxy "$proxy" --js-runtimes node \
    --extractor-args "youtube:player_client=android" \
    -f "18/b[height<=360]" -o "$vid.mp4" "https://www.youtube.com/watch?v=$vid" >> "$SCRATCH/ytdlp-$vid.log" 2>&1
  if [ -f "$vid.mp4" ] && [ "$(stat -c%s "$vid.mp4")" -gt 1000000 ] \
     && ffprobe -v error -show_entries format=duration -of csv=p=0 "$vid.mp4" >/dev/null 2>&1; then
    touch "done-$vid"
    log "$vid DL SUCCESS via proxy $(stat -c%s "$vid.mp4")"
    return 0
  fi
  log "$vid DL FAILED (yt-dlp)"
  rm -f "$vid.mp4"
  return 1
}

proxy_up() {
  set -a; . /home/alexey/.config/youtube/.env; set +a
  local sid=$(( (RANDOM * RANDOM + RANDOM) % 1000000000 ))
  local proxy="http://customer-${OXYLABS_USER}-sessid-${sid}:$(python3 -c 'from urllib.parse import quote; import os; print(quote(os.environ["OXYLABS_PASSWORD"], safe=""))')@${OXYLABS_ENDPOINT}"
  local code
  code=$(curl -s -x "$proxy" -o /dev/null -w "%{http_code}" --max-time 20 https://www.youtube.com/generate_204 2>/dev/null)
  [ "$code" = "204" ] || [ "$code" = "200" ]
}

missing_transcripts() {
  while read -r v; do
    [ -f "done-$v" ] || [ -f "$CACHE/$v.txt" ] || echo "$v"
  done < <(vids)
}

next_without_url() {
  while read -r v; do
    [ -f "done-$v" ] || [ -f "dl-$v.url" ] || {
      mf=$(cat "mf-$v" 2>/dev/null || echo 0)
      if [ "$mf" -lt 10 ] || [ $((round % 15)) -eq 0 ]; then echo "$v"; return; fi
    }
  done < <(vids)
}

next_with_url() {
  while read -r v; do
    if [ ! -f "done-$v" ] && [ -f "dl-$v.url" ]; then
      f=$(cat "fails-$v" 2>/dev/null || echo 0)
      if [ "$f" -lt 8 ] || [ $((round % 20)) -eq 0 ]; then echo "$v"; return; fi
    fi
  done < <(vids)
}

log "=== daemon2 start (v2: ttml subs, wider instances, url rotation) ==="
round=0
while [ $round -lt 1200 ]; do
  round=$((round + 1))
  if all_done; then
    log "ALL-VIDEOS-DONE at round $round"
    break
  fi

  proxied=0
  if [ $((round % 2)) -eq 1 ] && proxy_up; then
    proxied=1
    log "proxy UP"
    miss=$(missing_transcripts | head -3)
    [ -n "$miss" ] && HOME=/home/alexey uv run --with youtube-transcript-api --with requests \
      python3 "$SCRATCH/fetch-transcript.py" $miss >> "$SCRATCH/tx.log" 2>&1 || true
  fi

  # metadata for videos lacking a URL (one per round to stay polite)
  nv=$(next_without_url)
  if [ -n "$nv" ]; then
    if try_piped "$nv" || try_invid "$nv"; then
      rm -f "mf-$nv"
    else
      echo $(( $(cat "mf-$nv" 2>/dev/null || echo 0) + 1 )) > "mf-$nv"
      log "$nv no meta this round"
    fi
  fi

  # downloads: first video with a ready URL and mp4 slot free
  nw=$(next_with_url)
  if [ -n "$nw" ]; then
    download_curl "$nw" || { [ "$proxied" = 1 ] && download_ytdlp "$nw"; }
  elif [ "$proxied" = 1 ]; then
    # no piped/invidious URL anywhere; try proxy route for the first undone vid
    nv2=$(next_without_url)
    [ -n "$nv2" ] && download_ytdlp "$nv2"
  fi

  sleep 15
done
log "=== daemon2 exit ==="
