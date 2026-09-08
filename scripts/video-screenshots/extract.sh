#!/bin/bash
# Extract candidate frames around content moments.
# Usage: extract.sh <video-id> <mm:ss|seconds> [more timestamps...]
# For each timestamp t, writes w4-frames/<vid>/<t>-a.jpg (t-3s),
# <t>-b.jpg (t), <t>-c.jpg (t+3s).
SCRATCH=/home/alexey/git/.tmp/notes-work/llm-zoomcamp
DL=$SCRATCH/dl
vid="$1"; shift
outdir="$SCRATCH/w4-frames/$vid"
mkdir -p "$outdir"
to_sec() {
  case "$1" in
    *:*) h=0; IFS=: read -ra p <<< "$1"; [ ${#p[@]} -eq 3 ] && h=${p[0]} || true
         if [ ${#p[@]} -eq 3 ]; then echo $(( ${p[0]}*3600 + ${p[1]}*60 + ${p[2]} ));
         else echo $(( ${p[0]}*60 + ${p[1]} )); fi ;;
    *) echo "$1" ;;
  esac
}
for ts in "$@"; do
  s=$(to_sec "$ts")
  for off in a:-3 b:0 c:3; do
    key=${off%%:*}; d=${off##*:}
    t=$(( s + d ))
    [ $t -lt 0 ] && t=0
    ffmpeg -loglevel error -ss "$t" -i "$DL/$vid.mp4" -frames:v 1 -q:v 3 \
      "$outdir/${ts}-${key}.jpg" -y 2>/dev/null
  done
  echo "extracted $ts (a=-3s b=on-time c=+3s)"
done
ls "$outdir" | wc -l
