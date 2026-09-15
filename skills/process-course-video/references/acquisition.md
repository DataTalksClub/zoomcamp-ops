# Source acquisition and transcript recovery

Use this reference for the source-acquisition phase of
[`process-course-video`](../SKILL.md). The goal is a validated local source and
a timestamped transcript that can be used as evidence for lesson text, clip
boundaries, and frame selection.

## 1. Resolve and deduplicate video sources

Start from the course repository, not from a guessed playlist. Find every
frontmatter URL and module-level “original workshop recording” link:

```bash
rg -n "^video_url:|youtube\.com/watch|youtu\.be|Original workshop recording" \
  --glob '*.md' --glob '*.yaml' .
```

For each URL, record:

```text
video_id | source_url | title | module(s) | unit(s) | source kind | status
```

Use the video ID as the stable key. If a command is available, resolve a URL
without downloading it:

```bash
uvx yt-dlp --skip-download --print '%(id)s\t%(title)s\t%(duration)s' \
  '<youtube-url>'
```

Do not download the same ID once per unit. A shared workshop may feed many
units; its transcript and source video are acquired once and mapped to several
lesson ranges.

## 2. Create a bounded working area

Use a run-specific directory. A convenient layout is:

```bash
run_dir='.tmp/course-processing/<course-slug>/<run-id>'
mkdir -p "$run_dir"/{metadata,transcripts,videos,plans,clips,candidates,crops,finals,reports}
```

Keep the full source video in this run directory or in the repository's
gitignored `.tmp/videos/` cache. Do not put media in a tracked course folder.
When processing many videos on a nearly full disk, keep at most two source
videos at a time and delete each validated source only after its frames/clips
and source metadata have been preserved. The operational pipeline used this
rule because large media and unrelated build caches can fill the disk without
an obvious download error.

Before downloading, look for an existing file with the same recorded video ID.
Do not re-download an unchanged source merely to inspect metadata. Reuse it
only after running the validation in the next section.

## 3. Download the normal source

For chopping, use the best available source at or below 720p. The source's
quality is the ceiling - re-encoding cannot restore detail that YouTube did not
expose.

```bash
uvx yt-dlp \
  -f 'bv*[height<=720]+ba/b[height<=720]' \
  -S 'res:720,br' \
  --merge-output-format mkv \
  -o "$run_dir/videos/<video-slug>.%(ext)s" \
  '<youtube-url-or-id>'
```

For frame extraction only, a 360p progressive MP4 is usually enough for a
640×360 lesson frame and is much smaller. Download the whole file once rather
than using `--download-sections`; the documented proxy run produced truncated
files and `ffmpeg` error 187 with section downloads.

The existing repository skill
[`fetch-youtube-video`](../../fetch-youtube-video/SKILL.md) owns the short
standard recipe. Read it when the task is only to obtain a local video.

## 4. Validate the file before using it

Record the path and inspect its actual metadata:

```bash
video_path="$run_dir/videos/<video-file>"
test -s "$video_path"
video_bytes=$(stat -c%s "$video_path")
video_duration=$(ffprobe -v error -show_entries format=duration \
  -of csv=p=0 "$video_path")
video_streams=$(ffprobe -v error \
  -show_entries stream=codec_type,codec_name,width,height \
  -of default=noprint_wrappers=1 "$video_path")
printf 'bytes=%s\nduration=%s\n%s\n' \
  "$video_bytes" "$video_duration" "$video_streams"
```

A plausible download is larger than a tiny error page, `ffprobe` exits zero,
the duration is close to the platform duration, and a frame can be decoded:

```bash
ffmpeg -v error -ss 1 -i "$video_path" -frames:v 1 \
  "$run_dir/metadata/<video-id>-decode-test.jpg"
```

If the file is suspicious, delete only that bounded failed artifact and retry
from a fresh route. Do not accept a file because `yt-dlp` printed “done”.

## 5. When YouTube blocks direct access

Use the route that is already configured and authorized for the machine. Do
not add credentials to this repository or put a proxy URL in a log.

### Route A: an authorized sticky-session proxy

The September 2026 run required a new provider session per video. DataImpulse
uses a `__sessid` suffix; Oxylabs uses a `customer-...-sessid-...` username.
The critical details were:

- reuse one session ID for one video's metadata and stream requests;
- use `player_client=android`;
- provide a JavaScript runtime with `--js-runtimes node`;
- use progressive format 18 or another available format at 360p;
- download the full file and validate it with `ffprobe`.

If the machine has the documented environment file, load it without tracing or
printing it. The variable names below are examples only:

```bash
set -a
. /home/alexey/.config/youtube/.env
set +a

proxy_sid="$RANDOM$RANDOM"
proxy_password=$(python -c \
  'from urllib.parse import quote; import os; print(quote(os.environ["DATAIMPULSE_PASSWORD"], safe=""))')
proxy_user="${DATAIMPULSE_USER}__sessid.${proxy_sid}"
proxy_url="http://${proxy_user}:${proxy_password}@${DATAIMPULSE_ENDPOINT}"

yt-dlp --proxy "$proxy_url" --js-runtimes node \
  --extractor-args 'youtube:player_client=android' \
  -f '18/b[height<=360]' \
  -o "$run_dir/videos/<video-id>.mp4" \
  'https://www.youtube.com/watch?v=<video-id>'
```

If the configured provider is Oxylabs, build the provider-specific username
from `OXYLABS_USER`, `OXYLABS_PASSWORD`, and `OXYLABS_ENDPOINT` instead. The
password must be URL-encoded. Never use `set -x`, paste `proxy_url` into a
report, or echo the sourced environment.

Interpret HTTP failures before changing the recipe:

| Symptom | Likely meaning | Response |
| --- | --- | --- |
| 403 from YouTube/transcript API | IP or client blocked by YouTube | Use an authorized sticky session or the mirror route |
| 403 from a media stream | Rotating proxy IP does not match the stream session | Retry with a fresh per-video session |
| 407 from the proxy on every request | Provider quota/account problem | Stop retrying that account and use a mirror or wait for the account to recover |
| Formats missing or images only | Wrong player client or missing JS runtime | Use `player_client=android` and `--js-runtimes node` |

### Route B: Piped or Invidious metadata mirrors

Use a currently reachable instance; public instances are volatile, so do not
hard-code an old mirror as a permanent guarantee. The repository's
[`dl-daemon2.sh`](../../../scripts/video-screenshots/dl-daemon2.sh) contains the
known-good rotation logic and VTT/TTML parser from the 2026 run. Read it before
using it: it contains machine-specific scratch paths and is an operational
daemon, not a portable one-command skill.

The manual fallback is:

1. Fetch metadata from `https://<piped-host>/streams/<video-id>` or
   `https://<invidious-host>/api/v1/videos/<video-id>` into the run directory.
2. From Piped, prefer a progressive `MPEG_4` stream. If none exists, use a
   video-only 360p MP4. From Invidious, prefer a progressive `formatStreams`
   MP4, then a video-only adaptive MP4.
3. Validate the returned stream URL with a small ranged request. Reject a
   block page or `text/html` content type even when the metadata request was
   HTTP 200.
4. Download with a browser user-agent, a bounded timeout, and stall detection:

   ```bash
   curl -sL -m 1200 --speed-time 30 --speed-limit 10000 \
     -A "$user_agent" '<validated-stream-url>' \
     -o "$run_dir/videos/<video-id>.mp4"
   ```

5. Run the same size, decode, and `ffprobe` checks as the normal route. If the
   download fails, discard the saved stream URL and resolve fresh metadata
   from another instance. A dead URL remains dead even when retried.

The mirror route can also expose captions. Piped returns a `subtitles` list;
Invidious returns `captions`. Prefer English, save the raw response, and do not
assume the file extension identifies the format. Piped has served TTML with a
`.vtt` filename.

## 6. Fetch a timestamped transcript

Captions are preferred over speech-to-text because they are cheap, already
aligned to the recording, and usually close to the wording learners heard.

If the standalone `fetch-youtube` skill is available, read and use it for the
caption fetch. Its normal cache is idempotent; copy the resulting file into
`$run_dir/transcripts/<video-id>.txt` and retain the cache path in the report.

On the documented machine, the repository's proxy helper can be used after
checking its hard-coded credential path and adapting it if necessary:

```bash
uv run --with youtube-transcript-api --with requests \
  scripts/video-screenshots/fetch-transcript.py <video-id>
```

That helper reads the Oxylabs environment file, retries with fresh sticky
sessions, and writes the shared cache. It is not portable without changing the
credential loading. Do not make its absolute paths part of a course repo's
published instructions.

If the video has no usable YouTube captions, try the Piped `subtitles` or
Invidious `captions` response before transcribing locally. If local
transcription is required, read the available `openai-transcribe` skill first,
then extract a mono 16 kHz audio file if its instructions call for one:

```bash
ffmpeg -i "$video_path" -vn -ac 1 -ar 16000 -c:a pcm_s16le \
  "$run_dir/transcripts/<video-id>.wav"
```

Keep segment timestamps from the transcription output. A plain text transcript
without timestamps can support lesson prose, but it cannot reliably drive frame
selection or clip boundaries; record that limitation and use manual video
review for those steps.

## 7. Normalize captions without losing provenance

Keep both files:

```text
transcripts/<video-id>.raw.vtt or .raw.ttml   # untouched response
transcripts/<video-id>.txt                   # normalized working transcript
```

The normalized convention is one cue per line:

```text
M:SS text of cue
H:MM:SS text of cue
```

Normalization should:

- detect WebVTT versus TTML from the content, not the extension;
- convert cue starts to `M:SS` or `H:MM:SS`;
- strip markup and join wrapped lines;
- remove duplicate rolling-window cues while preserving real continuations;
- keep the original cue order and timestamps;
- retain the raw response so a questionable line can be checked later.

The parser in `scripts/video-screenshots/dl-daemon2.sh` implements the VTT and
TTML cases used by the 2026 run. If it is copied into a portable script, make
the input and output paths explicit and test it on both formats.

Run basic checks:

```bash
transcript_path="$run_dir/transcripts/<video-id>.txt"
test "$(wc -l < "$transcript_path")" -ge 5
sed -n '1,5p' "$transcript_path"
tail -n 5 "$transcript_path"
rg -n -i 'homework|exercise|diagram|show|see|question|error|failed' \
  "$transcript_path" | sed -n '1,80p'
```

Spot-check the beginning, middle, and end against the video. Check the
language, obvious repeated cues, missing long sections, and whether technical
names are transcribed plausibly. A transcript passes only when it is usable as
an evidence map, not merely because it contains text.

## 8. Record the source row

At minimum, each `sources.tsv` row should preserve:

```text
video_id  source_url  title  units  local_video  bytes  duration  dimensions  retrieval_route  raw_captions  normalized_transcript  status  notes
```

Use a short route label such as `youtube`, `sticky-proxy`, `piped`,
`invidious`, or `local-stt`. Put failures and limitations in `notes`, never
credentials. The source row is what lets a later illustration or lesson review
answer “which recording and which timestamp produced this text?”
