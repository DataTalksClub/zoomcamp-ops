# Video screenshot pipeline for lesson notes

How the per-unit screenshots embedded in the Zoomcamp lesson notes were
produced in the September 2026 run (data-engineering-zoomcamp cohorts/2027
modules 3+6, machine-learning-zoomcamp cohorts/2026, llm-zoomcamp
cohorts/2026 — roughly 150 units, 900+ screenshots, done by three aplexer
zcodex agent sessions working in parallel).

This documents what was actually done and verified to work on this machine,
including the failure modes. The general rubric-driven workflow for reviewing
frames is in [`../skills/extract-youtube-illustrations`](../skills/extract-youtube-illustrations/SKILL.md);
this page is the concrete acquire → find → extract → embed pipeline, with the
mirror fallback that kept it running through a proxy outage.

## The pipeline at a glance

```
unit page (video_url in frontmatter)
  → transcript (timestamped, cached)         # what happens when
  → pick 3–8 content moments per unit        # which moments carry content
  → download the video (360p is enough)       # proxy, or mirrors when it is down
  → ffmpeg single-frame extraction ±3s        # candidates around each moment
  → view candidates, keep the sharpest        # discard blur, fades, talking heads
  → rename + embed after the matching paragraph
```

Full frames were used, un-cropped, at 640×360. See "Cropping" below.

---

## 1. Transcripts

Everything starts from a timestamped transcript — it is both the source of
truth for the lesson text and the map for choosing frame timestamps.

The standard tool is the fetch-youtube skill:

```bash
HOME=/home/alexey uv run --with youtube-transcript-api --with python-dotenv \
  /home/alexey/git/.agents/skills/fetch-youtube/youtube.py <video-id> --path
```

- Output: `~/.cache/youtube_transcripts/<id>.txt`, one `M:SS text` line per
  cue. Fetch once, then grep/read the file; it is a cache, idempotent.
- YouTube is bot-blocked from this box, so the script routes through the
  Oxylabs proxy configured in `/home/alexey/.config/youtube/.env`
  (`OXYLABS_USER` / `OXYLABS_ENDPOINT` / `OXYLABS_PASSWORD` — never print or
  commit these).
- Direct fetch without the proxy fails. With the proxy, rotating IPs work for
  transcript API calls; sticky sessions are only required for video streams.

When the proxy is down (see below), transcripts were scraped from the same
mirror APIs used for downloads: Piped's `/streams/<id>` metadata carries a
`subtitles` list and Invidious `/api/v1/videos/<id>` carries `captions`. The
served file is VTT or TTML depending on the instance; it is parsed into the
same `M:SS text` format and written into the shared cache
(`vtt_to_cache` in `scripts/video-screenshots/dl-daemon.sh`). One quirk:
Piped sometimes serves TTML with a `.vtt` name — detect by content, not
extension.

## 2. Getting the videos

Direct YouTube access is blocked ("Sign in to confirm you're not a bot").
Two working routes exist; the run used A until the account hit its traffic
limit, then B carried the rest.

### Route A — yt-dlp through the Oxylabs proxy (primary)

```bash
set -a; . /home/alexey/.config/youtube/.env; set +a
SID=$RANDOM$RANDOM   # ONE sticky session per video, reused for all requests
PROXY="http://customer-${OXYLABS_USER}-sessid-${SID}:$(python3 -c 'from urllib.parse import quote; import os; print(quote(os.environ["OXYLABS_PASSWORD"], safe=""))')@${OXYLABS_ENDPOINT}"
yt-dlp --proxy "$PROXY" --js-runtimes node \
  --extractor-args "youtube:player_client=android" \
  -f "18/b[height<=360]" -o "<video-id>.mp4" \
  "https://www.youtube.com/watch?v=<video-id>"
```

The load-bearing details, each of which was individually required:

- **Sticky session (`-sessid-<SID>`).** Rotating IPs get 403 on the
  googlevideo stream even when the metadata requests succeed. One SID per
  video, reused for that video's requests; on failure, pick a fresh SID and
  retry.
- **`player_client=android`.** The only client that reliably returns a
  downloadable stream here. `tv`, `ios`, `mweb`, `web_embedded` either 403 or
  return images only.
- **Format `18` (360p progressive mp4).** YouTube's SABR experiment strips
  higher resolutions and separate audio/video URLs unless a PO token is
  provided. 360p is plenty for an embedded 640×360 lesson image.
- **`--js-runtimes node`** (node is installed via nvm). Without a JS runtime
  yt-dlp warns and may miss formats.
- **Download the whole file.** `--download-sections` is unreliable through
  the proxy (truncated files, ffmpeg error 187). A full video is ~10–30 MB
  per 15 minutes at 360p; cheaper to download once and extract many frames.
- **Validate the result** before trusting it: file > 1 MB and
  `ffprobe -v error -show_entries format=duration -of csv=p=0 out.mp4`
  succeeds. Truncated downloads otherwise look "done".

### Route B — Piped/Invidious mirrors (when the proxy is down)

The Oxylabs account ran out of traffic mid-run (every authenticated request
returned **407 account-wide**, for hours — distinguishable from a 403, which
would be YouTube blocking). The ML session discovered Piped mirrors still
worked; the LLM session industrialized it into a daemon
(`scripts/video-screenshots/dl-daemon.sh`, keep-alive wrapper
`dl-supervisor.sh`):

1. Get metadata: `curl https://<mirror>/streams/<video-id>` (Piped) or
   `https://<instance>/api/v1/videos/<video-id>` (Invidious). Lists of 18+
   Piped mirrors and 16 Invidious instances are in the daemon; a per-video
   rotation offset makes retries try different instances instead of
   hammering the same one.
2. Extract a stream URL from the metadata JSON: prefer a progressive
   `MPEG_4` stream, else a video-only 360p mp4. Video-only is fine — frames
   need no audio.
3. Download with curl, with stall detection
   (`--speed-time 30 --speed-limit 10000` aborts if throughput drops below
   10 KB/s for 30 s) and the same size + ffprobe validation as Route A.
4. **Unstick rule:** on failure, delete the banked URL so the next round
   resolves fresh metadata from a different mirror. A dead mirror's URLs
   keep failing; a fresh one works. Individual mirrors are flaky — the
   rotation plus retry loop is what makes this route dependable in
   aggregate (it sustained 40+ videos over several hours).

The daemon tries the proxy again every round (`/generate_204` probe) and
prefers Route A whenever it is back up.

### Disk discipline

The disk ran at 88–98% full during the run, so downloads only went to
`~/git/.tmp/notes-work/<camp>/` (never inside a course repo — `.tmp` is not
gitignored there), at most 2 videos on disk at a time, and each mp4 was
deleted immediately after its frames were extracted and committed. The
enforcement lives in the daemon (`mp4_count` check) and in the worker
playbook.

## 3. Finding the frames

Timestamps came from the transcript, matched against the unit's text:

1. Read the finished unit page and its transcript side by side.
2. Pick **3–8 moments that carry content**: slides, diagrams, architecture
   sketches, notebook cells, terminal output, dashboards. Not the instructor
   talking, not title cards.
3. Find each moment's timestamp from the transcript — the paragraph that
   discusses a diagram sits next to the transcript lines where it is drawn
   or shown, and `M:SS` lines convert directly to seek positions.
4. When a video fed two units (chopped lesson videos do), each unit got its
   own frames from different parts of the video, split by topic.
5. Fallback when no transcript exists: sample frames evenly across the
   duration (it is in the mirror metadata JSON) and keep the content-bearing
   ones.

## 4. Extracting the frames

Single-frame extraction with fast seek, three candidates per moment:

```bash
ffmpeg -ss <seconds> -i <video-id>.mp4 -frames:v 1 -q:v 3 out.jpg
```

- `-ss` **before** `-i` = fast seek (keyframe-accurate is unnecessary;
  ±3 s sampling covers the drift).
- `-q:v 3` = high-quality JPEG for a 360p source; higher numbers shrink the
  file but the source resolution is the real ceiling (~25–30 KB/frame).
- Three candidates per moment — `t-3s`, `t`, `t+3s` — because the exact
  second is rarely the cleanest view of a slide or terminal. This is what
  `scripts/video-screenshots/extract.sh` automates:
  `extract.sh <video-id> <mm:ss> [more...]` writes `<ts>-a.jpg`, `<ts>-b.jpg`,
  `<ts>-c.jpg` per timestamp.

## 5. Selecting keepers

Every candidate was viewed (Read tool on the image) before being kept:

- keep the sharpest, most representative frame of the moment;
- discard motion blur, fade transitions, half-drawn diagrams, and frames
  where the content is off-screen;
- 3–8 embedded per unit is the target; fewer is acceptable only when the
  video genuinely shows less.

## 6. Cropping

**No cropping was done in this run.** Committed screenshots are full frames
at 640×360 (a few 598×360 from streams with baked-in letterboxing). At
embedded size this is legible for slides, notebooks, and terminal output.

The crop-and-regenerate second pass — crop out the useful region
deterministically, then either regenerate with imagegen (conceptual
diagrams only) or re-export exactly (code, plots, UI) — is a separate,
later workflow, already documented in
[`../template/image-regeneration-workflow.md`](../template/image-regeneration-workflow.md)
and scaled up in
[`../template/coursewide-screenshot-rollout.md`](../template/coursewide-screenshot-rollout.md).
Treat this pipeline's output as the raw material for that pass, not as the
final polish.

## 7. Naming and embedding

- File: `cohorts/<year>/<module>/images/<unit-stem>-NN-<kebab-slug>.jpg`
  — the unit-stem prefix keeps the module's flat `images/` directory
  collision-free; `NN` is zero-padded order of appearance in the video; the
  slug is 2–4 kebab words describing the content
  (e.g. `05-search-01-index-creation.jpg`).
- Embed: `![Descriptive alt text](images/<file>.jpg)` on its own line,
  immediately after the paragraph the frame illustrates. Alt text is a short
  phrase, no trailing period.
- Unit page rules still apply: images are relative paths inside the module
  directory; exactly one H1; nothing else in the page changes. For published
  cohorts the screenshot pass is embed-only — no prose edits.

## 8. Coordination at scale

The LLM run (55 videos, ~11 h) parallelized with a claim-based queue so
several workers could share one download daemon without collisions
(`scripts/video-screenshots/dl-daemon2.sh` + the playbook it served):

- The daemon owns downloads exclusively; workers never download.
- Workers claim a finished video under `flock` (`claim-<vid>/` directory),
  process all units on its queue line, log a row to a shared
  `status.tsv`, delete the mp4, then mark `proc-<vid>`.
- Stale-claim takeover: a claim older than 25 min with no unit edits and no
  log activity can be taken over (with a re-check before editing, so a
  finisher never gets double-processed).

## 9. Orchestration context

The whole job ran as aplexer sessions (engine `codex`, profile `zcodex`),
one per course repo, each fanning out to at most 3 sub-agents, module by
module, with the conformance checker baseline recorded before and after and
small per-module commits. See `~/.zcode/cli/memories/` project memory
(`zoomcamp-notes-workflow`, `youtube-proxy-recipe`, `aplexer-zcodex-usage`)
for the operational quirks of driving those sessions.

## Gotchas

| Symptom | Cause | Fix |
|---|---|---|
| 403 on transcript API | no proxy / rotating IP blocked | route through Oxylabs |
| 403 on video stream | rotating proxy IP on googlevideo | sticky `sessid` per video |
| 407 on everything, account-wide | Oxylabs traffic quota exhausted | switch to mirror route (Route B), retry proxy periodically |
| formats missing / "images only" | wrong player client or no JS runtime | `player_client=android`, `--js-runtimes node` |
| truncated mp4, ffmpeg error 187 | `--download-sections` through proxy | download whole file, validate with ffprobe |
| proxy 403 vs 403 | 403 = YouTube blocking; 407 = proxy quota | read the code before changing recipes |
| disk full mid-run | cargo incremental caches regrow ~50 GB | clear `codex-rs/target/*/incremental` (pure cache), keep ≤2 mp4 |

## Reusable scripts

Copied verbatim from the run's scratch (the originals under
`~/git/.tmp/notes-work/llm-zoomcamp/` are ephemeral):

- `scripts/video-screenshots/dl-daemon.sh` — the routing download daemon
  (proxy → Piped → Invidious), transcript scraping included.
- `scripts/video-screenshots/dl-supervisor.sh` — keep-alive wrapper.
- `scripts/video-screenshots/extract.sh` — ±3 s candidate extraction.
- `scripts/video-screenshots/fetch-transcript.py` — proxy transcript fetch
  with fresh-sticky-session retries.
- `scripts/video-screenshots/dl-daemon2.sh` — the variant actually running
  during the LLM backfill.

All credentials come from `/home/alexey/.config/youtube/.env` at runtime;
nothing here embeds them.
