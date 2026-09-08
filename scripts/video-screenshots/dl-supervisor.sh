#!/bin/bash
# Restart dl-daemon2.sh whenever it exits until every queue video is done-.
SCRATCH=/home/alexey/git/.tmp/notes-work/llm-zoomcamp
LOG=$SCRATCH/dl.log
while true; do
  total=$(wc -l < "$SCRATCH/queue.txt")
  done_n=$(ls "$SCRATCH/dl/" 2>/dev/null | grep -c '^done-')
  if [ "$done_n" -ge "$total" ]; then
    echo "[$(date +%H:%M:%S)] [supervisor] all $total videos downloaded, exiting" >> "$LOG"
    exit 0
  fi
  if ! pgrep -f 'dl-daemon2\.sh' >/dev/null 2>&1; then
    echo "[$(date +%H:%M:%S)] [supervisor] daemon not running - restarting" >> "$LOG"
    setsid nohup bash "$SCRATCH/dl-daemon2.sh" </dev/null >/dev/null 2>&1 &
  fi
  sleep 90
done
