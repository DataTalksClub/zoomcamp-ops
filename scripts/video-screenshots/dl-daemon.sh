#!/bin/bash
# Orchestrator for LLM-zoomcamp screenshot backfill downloads (v2).
# Routes: DataImpulse proxy (yt-dlp + transcript API) preferred when up,
# then Oxylabs, then Piped mirrors, then Invidious instances
# (format OR adaptive).
# Video-only streams are fine (frames only, no audio needed).
# Unstick rule: a URL whose download fails is deleted so the next round
# tries a different mirror. Keeps <=2 mp4 on disk globally.
# State dir: dl/  (done-<vid>, meta-<vid>.json, dl-<vid>.url, subs-<vid>.vtt)
SCRATCH=/home/alexey/git/.tmp/notes-work/llm-zoomcamp
DL=$SCRATCH/dl
CACHE=/home/alexey/.cache/youtube_transcripts
LOG=$SCRATCH/dl.log
PROXY_ENV=/home/alexey/.config/youtube/.env
ROUNDS=${ROUNDS:-1600}
PIPEDED="api.piped.private.coffee api.piped.projectsegfau.lt pipedapi.ducks.party api.piped.privacydev.net pipedapi.reallyaweso.me pipedapi.adminforge.de pipedapi.orangenet.cc pipedapi.nosebs.ru pipedapi.leptons.xyz pipedapi.kavin.rocks piped-api.lunar.icu pipedapi.mha.fi watchapi.whatever.social pipedapi.astartes.nl piped-api.codespace.cz pipedapi.duti.dev pipedapi.drgns.space pipedapi.phoenixthrush.com"
INVID="inv.nadeko.net yewtu.be invidious.nerdvpn.de iv.melmac.space invidious.f5.si invidious.privacyredirect.com invidious.jing.rocks inv.tux.pizza invidious.protokolla.fi iv.duti.dev invidious.privacydev.net invidious.materialio.us iv.ggtyler.dev invidious.dhusch.de inv.zzls.xyz invidious.perennialte.ch"
cd "$DL" || exit 1
exec 9>"$SCRATCH/.daemon.lock"
flock -n 9 || { echo "daemon already running" >> "$LOG"; exit 0; }

log() { echo "[$(date +%H:%M:%S)] $*" >> "$LOG"; }

load_proxy_env() {
  [ -r "$PROXY_ENV" ] || return 1
  # shellcheck disable=SC1090
  . "$PROXY_ENV"
}

urlencode() {
  printf '%s' "$1" |
    python3 -c 'from urllib.parse import quote; import sys; print(quote(sys.stdin.read(), safe=""))'
}

normalize_endpoint() {
  local endpoint="$1"
  endpoint="${endpoint#http://}"
  endpoint="${endpoint#https://}"
  endpoint="${endpoint%/}"
  printf '%s\n' "$endpoint"
}

new_session_id() { printf '%s%s%s\n' "$RANDOM" "$RANDOM" "$RANDOM"; }

dataimpulse_session_user() {
  local user="$1" sid="$2"
  # DataImpulse supports sessid in the username; its syntax differs from Oxylabs.
  if [[ "$user" == *__* ]]; then
    printf '%s;sessid.%s\n' "$user" "$sid"
  else
    printf '%s__sessid.%s\n' "$user" "$sid"
  fi
}

proxy_configured() {
  case "$1" in
    dataimpulse)
      [ -n "${DATAIMPULSE_USER:-}" ] &&
        [ -n "${DATAIMPULSE_PASSWORD:-}" ] &&
        [ -n "${DATAIMPULSE_ENDPOINT:-}" ]
      ;;
    oxylabs)
      [ -n "${OXYLABS_USER:-}" ] &&
        [ -n "${OXYLABS_PASSWORD:-}" ] &&
        [ -n "${OXYLABS_ENDPOINT:-}" ]
      ;;
    *) return 1 ;;
  esac
}

build_proxy_url() {
  local provider="$1" sid="$2"
  local user password endpoint
  case "$provider" in
    dataimpulse)
      user=$(dataimpulse_session_user "${DATAIMPULSE_USER:-}" "$sid")
      password="${DATAIMPULSE_PASSWORD:-}"
      endpoint=$(normalize_endpoint "${DATAIMPULSE_ENDPOINT:-}")
      ;;
    oxylabs)
      user="customer-${OXYLABS_USER:-}-sessid-${sid}"
      password="${OXYLABS_PASSWORD:-}"
      endpoint=$(normalize_endpoint "${OXYLABS_ENDPOINT:-}")
      ;;
    *) return 1 ;;
  esac
  [ -n "$user" ] && [ -n "$password" ] && [ -n "$endpoint" ] || return 1
  printf 'http://%s:%s@%s\n' "$(urlencode "$user")" "$(urlencode "$password")" "$endpoint"
}

video_session_id() {
  local vid="$1"
  local sidfile="proxy-sid-$vid"
  if [ ! -s "$sidfile" ]; then
    new_session_id > "$sidfile"
  fi
  cat "$sidfile"
}

valid_mp4() {
  local file="$1" duration
  [ -f "$file" ] && [ "$(stat -c%s "$file" 2>/dev/null || echo 0)" -gt 1000000 ] || return 1
  duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$file" 2>/dev/null) || return 1
  [ -n "$duration" ]
}

vids() { awk '{print $1}' "$SCRATCH/queue.txt"; }

mp4_count() { find "$SCRATCH" -name '*.mp4' -size +1M 2>/dev/null | wc -l; }

all_done() {
  local n=0
  while read -r v; do [ -f "done-$v" ] || return 1; done < <(vids)
  return 0
}

vtt_to_cache() {
  python3 - "$1" "$2" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
txt = open(src, encoding='utf-8', errors='replace').read()
out, seen_ts = [], set()
for block in re.split(r'\n\s*\n', txt):
    lines = [l for l in block.splitlines() if l.strip()]
    ts_line = next((l for l in lines if '-->' in l), None)
    if not ts_line:
        continue
    start = ts_line.split('-->')[0].strip()
    m = re.match(r'(\d+):(\d+):(\d+)\.', start)
    if not m:
        continue
    h, mi, s = (int(x) for x in m.groups())
    sec = h * 3600 + mi * 60 + s
    text = ' '.join(
        re.sub(r'<[^>]+>', '', l).strip()
        for l in lines[lines.index(ts_line) + 1:]
    ).strip()
    if not text:
        continue
    if sec in seen_ts:
        continue
    seen_ts.add(sec)
    ts = f"{h}:{mi:02}:{s:02}" if h else f"{mi}:{s:02}"
    out.append(f"{ts} {text}")
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
  curl -sL -m 40 "$suburl" -o "subs-$vid.vtt" || return 1
  grep -q -- '-->' "subs-$vid.vtt" || return 1
  vtt_to_cache "subs-$vid.vtt" "$CACHE/$vid.txt" >/dev/null 2>&1 || return 1
  return 0
}

save_subs_inv() {
  local vid="$1" inst="$2"
  local capurl
  capurl=$(python3 -c "
import json
d = json.load(open('meta-$vid.json'))
caps = d.get('captions') or []
en = [x for x in caps if x.get('language_code', '').startswith('en')]
print('https://$inst' + (en[0]['url'] if en else (caps[0]['url'] if caps else '')))
" 2>/dev/null)
  [ -z "$capurl" ] && return 1
  curl -sL -m 40 "$capurl" -o "subs-$vid.vtt" || return 1
  grep -q -- '-->' "subs-$vid.vtt" || return 1
  vtt_to_cache "subs-$vid.vtt" "$CACHE/$vid.txt" >/dev/null 2>&1 || return 1
  return 0
}

# rotate a list by n: elements n+1..end then 1..n
rot() { local n=$1; shift; local cnt=0; for x in "$@"; do cnt=$((cnt+1)); [ $cnt -gt $n ] && echo "$x"; done; cnt=0; for x in "$@"; do cnt=$((cnt+1)); [ $cnt -le $n ] && echo "$x"; done; }

try_piped() {
  local vid="$1"
  local off=$(( ($(cat "rot-$vid" 2>/dev/null || echo 0)) % 9 ))
  local mirror
  for mirror in $(rot "$off" $PIPEDED); do
    local code
    code=$(curl -sL -m 25 -o "meta-$vid.json" -w '%{http_code}' "https://$mirror/streams/$vid" 2>/dev/null)
    if [ "$code" = "200" ] && python3 -c "
import json
d = json.load(open('meta-$vid.json'))
vs = [x for x in d.get('videoStreams', []) if x.get('format') == 'MPEG_4' and x.get('url')]
prog = [x for x in vs if not x.get('videoOnly')]
vo = [x for x in vs if x.get('videoOnly')]
pick = None
if prog: pick = prog[0]
else:
    vo360 = [x for x in vo if '360' in (x.get('quality') or '')]
    pick = (vo360 or vo or [None])[0]
assert pick
open('dl-$vid.url', 'w').write(pick['url'])
open('q-$vid', 'w').write((pick.get('quality') or '') + (' videoOnly' if pick.get('videoOnly') else ''))
" 2>/dev/null; then
      log "$vid META via piped/$mirror q=$(cat q-$vid 2>/dev/null)"
      save_subs_piped "$vid" && log "$vid SUBS -> cache" || log "$vid no subs via piped"
      return 0
    fi
  done
  return 1
}

try_invid() {
  local vid="$1"
  local off=$(( ($(cat "rot-$vid" 2>/dev/null || echo 0)) % 8 ))
  local inst
  for inst in $(rot "$off" $INVID); do
    local code
    code=$(curl -sL -m 25 -o "meta-$vid.json" -w '%{http_code}' "https://$inst/api/v1/videos/$vid" 2>/dev/null)
    if [ "$code" = "200" ] && python3 -c "
import json
d = json.load(open('meta-$vid.json'))
def h(x):
    return x.get('url')
fs = [x for x in d.get('formatStreams', []) if x.get('container') == 'mp4' and h(x)]
pick = None
if fs: pick = fs[0]
else:
    ad = [x for x in d.get('adaptiveFormats', []) if 'video/mp4' in (x.get('type') or '') and h(x)]
    v360 = [x for x in ad if '360' in (x.get('qualityLabel') or '')]
    pick = (v360 or ad or [None])[0]
assert pick
open('dl-$vid.url', 'w').write(pick['url'])
open('q-$vid', 'w').write((pick.get('qualityLabel') or pick.get('quality') or '') + ' inv')
" 2>/dev/null; then
      log "$vid META via invidious/$inst q=$(cat q-$vid 2>/dev/null)"
      save_subs_inv "$vid" "$inst" && log "$vid SUBS -> cache" || log "$vid no subs via invidious"
      return 0
    fi
  done
  return 1
}

download_curl() {
  local vid="$1"
  local out="$vid.mp4"
  [ "$(mp4_count)" -ge 2 ] && return 1
  log "$vid download start (curl q=$(cat "q-$vid" 2>/dev/null))"
  curl -sL -m 1800 --speed-time 30 --speed-limit 10000 "$(cat "dl-$vid.url")" -o "$out"
  if valid_mp4 "$out"; then
    touch "done-$vid"
    log "$vid DL SUCCESS $(stat -c%s "$out")"
    return 0
  fi
  log "$vid DL FAILED (curl) - dropping URL for re-route"
  rm -f "$out" "dl-$vid.url" "q-$vid"
  echo $(( $(cat "fails-$vid" 2>/dev/null || echo 0) + 1 )) > "fails-$vid"
  return 1
}

download_ytdlp() {
  local vid="$1"
  [ "$(mp4_count)" -ge 2 ] && return 1
  load_proxy_env || return 1
  local provider="${PROXY_PROVIDER:-}"
  proxy_configured "$provider" || return 1
  local sid proxy
  sid=$(video_session_id "$vid")
  proxy=$(build_proxy_url "$provider" "$sid") || return 1
  log "$vid download start (yt-dlp proxy provider=$provider)"
  yt-dlp --proxy "$proxy" --js-runtimes node \
    --extractor-args "youtube:player_client=android" \
    -f "18/b[height<=360]" -o "$vid.mp4" "https://www.youtube.com/watch?v=$vid" >> "$SCRATCH/ytdlp-$vid.log" 2>&1
  if valid_mp4 "$vid.mp4"; then
    touch "done-$vid"
    log "$vid DL SUCCESS via proxy $(stat -c%s "$vid.mp4")"
    return 0
  fi
  log "$vid DL FAILED (yt-dlp)"
  rm -f "$vid.mp4" "proxy-sid-$vid"
  return 1
}

fetch_tx_proxy() {
  load_proxy_env || return 1
  local provider="${PROXY_PROVIDER:-}" sid proxy data_user oxy_user
  proxy_configured "$provider" || return 1
  sid=$(new_session_id)
  proxy=$(build_proxy_url "$provider" "$sid") || return 1
  local -a proxy_env
  if [ "$provider" = "dataimpulse" ]; then
    data_user=$(dataimpulse_session_user "$DATAIMPULSE_USER" "$sid")
    proxy_env=(
      "DATAIMPULSE_USER=$data_user"
      "DATAIMPULSE_PASSWORD=$DATAIMPULSE_PASSWORD"
      "DATAIMPULSE_ENDPOINT=$DATAIMPULSE_ENDPOINT"
      DATAIMPULSE_HOST=
      DATAIMPULSE_PORT=
      OXYLABS_USER=
      OXYLABS_PASSWORD=
      OXYLABS_ENDPOINT=
    )
  else
    oxy_user="${OXYLABS_USER}-sessid-${sid}"
    proxy_env=(
      DATAIMPULSE_USER=
      DATAIMPULSE_PASSWORD=
      DATAIMPULSE_ENDPOINT=
      DATAIMPULSE_HOST=
      DATAIMPULSE_PORT=
      "OXYLABS_USER=$oxy_user"
      "OXYLABS_PASSWORD=$OXYLABS_PASSWORD"
      "OXYLABS_ENDPOINT=$OXYLABS_ENDPOINT"
    )
  fi
  env "${proxy_env[@]}" HOME=/home/alexey HTTPS_PROXY="$proxy" HTTP_PROXY="$proxy" \
    uv run --with youtube-transcript-api --with python-dotenv \
    /home/alexey/git/.agents/skills/fetch-youtube/youtube.py "$@" >> "$SCRATCH/tx.log" 2>&1
}

proxy_up() {
  PROXY_PROVIDER=
  load_proxy_env || return 1
  local provider sid proxy code
  for provider in dataimpulse oxylabs; do
    proxy_configured "$provider" || continue
    sid=$(new_session_id)
    proxy=$(build_proxy_url "$provider" "$sid") || continue
    code=$(curl -s -x "$proxy" -o /dev/null -w "%{http_code}" --max-time 15 https://www.youtube.com/generate_204 2>/dev/null)
    if [ "$code" = "204" ] || [ "$code" = "200" ]; then
      PROXY_PROVIDER="$provider"
      return 0
    fi
  done
  return 1
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
      if [ "$mf" -lt 25 ] || [ $((round % 12)) -eq 0 ]; then echo "$v"; return; fi
    }
  done < <(vids)
}

next_with_url() {
  while read -r v; do
    if [ ! -f "done-$v" ] && [ -f "dl-$v.url" ]; then
      f=$(cat "fails-$v" 2>/dev/null || echo 0)
      if [ "$f" -lt 4 ]; then echo "$v"; return; fi
    fi
  done < <(vids)
}

log "=== daemon v2 start ==="
round=0
while [ $round -lt "$ROUNDS" ]; do
  round=$((round + 1))
  if all_done; then
    log "ALL-VIDEOS-DONE at round $round"
    break
  fi

  proxied=0
  if proxy_up; then
    proxied=1
    [ $((round % 10)) -eq 1 ] && log "proxy UP ($PROXY_PROVIDER)"
    miss=$(missing_transcripts | head -3)
    [ -n "$miss" ] && fetch_tx_proxy $miss
  fi

  # metadata: up to 3 videos lacking a URL per round
  for i in 1 2 3; do
    nv=$(next_without_url)
    [ -z "$nv" ] && break
    if try_piped "$nv" || try_invid "$nv"; then
      rm -f "mf-$nv"
    else
      echo $(( $(cat "mf-$nv" 2>/dev/null || echo 0) + 1 )) > "mf-$nv"
      echo $(( ($(cat "rot-$nv" 2>/dev/null || echo 0) + 3) )) > "rot-$nv"
      [ $((round % 6)) -eq 0 ] && log "$nv no meta this round"
    fi
  done

  # downloads: prefer proxy route when it is up, else curl the banked URL
  nw=$(next_with_url)
  if [ -n "$nw" ]; then
    if [ "$proxied" = 1 ]; then
      download_ytdlp "$nw" || download_curl "$nw"
    else
      download_curl "$nw"
    fi
  elif [ "$proxied" = 1 ]; then
    nv2=$(next_without_url)
    [ -n "$nv2" ] && download_ytdlp "$nv2"
  fi

  sleep 15
done
log "=== daemon exit ==="
