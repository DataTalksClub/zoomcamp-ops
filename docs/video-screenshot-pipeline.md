# Video-to-lesson screenshot pipeline

The reusable workflow for turning workshop recordings into lesson text and
source-backed illustrations is [`process-course-video`](../skills/process-course-video/SKILL.md).
Read its acquisition, lesson-authoring, and illustration-refinement references
for the step-by-step procedure. This page keeps only the repository contract
and the small helper inventory.

## Pipeline

```text
unit/module video links
  → deduplicated source map
  → validated timestamped transcript
  → validated local video
  → lesson map and written unit
  → transcript-selected visual moments
  → neighboring candidate frames
  → rubric disposition
  → deterministic crop/re-render or reviewed conceptual redraw
  → lesson image reference and provenance record
```

The transcript is the timestamp map and a source for spoken explanations. The
recording, source repository, notebook, or native export is the authority for
exact code, commands, URLs, labels, values, plots, tables, and UI states.

## Working files

Use a run-specific, gitignored directory such as:

```text
.tmp/course-processing/<course>/<run>/
├── metadata/
├── transcripts/
├── videos/
├── plans/
├── candidates/
├── crops/
├── finals/
└── reports/
```

Never commit downloaded videos, raw candidates, crops, contact sheets, prompts,
rejected generations, signed stream URLs, or credentials. Keep the original
source frame unchanged when preparing a crop or regenerated image.

## Screenshot contract

- Choose a frame because it adds a specific teaching point, not because the
  recording changed screens.
- Use transcript cues and the surrounding lesson paragraph to locate moments.
  Extract neighboring frames around a timestamp and inspect every candidate.
- Keep only the minimum set of clear, durable visuals. A unit with no useful
  source visual may have no image.
- Exact code, numbers, URLs, plots, tables, and UI states use native or
  deterministic treatment. A conceptual diagram may use a reviewed redraw.
- Remove faces, webcam/Zoom/browser chrome, cursors, watermarks, private chat,
  blur, transitions, and unrelated panels unless they are the subject.
- Put critical exact information in lesson text as well as in any image.
- Embed an accepted asset immediately after the paragraph it supports, with
  descriptive alt text that says what the learner should notice.

## Helpers

These scripts support the workflow but are not a portable end-to-end command:

- [`fetch-transcript.py`](../scripts/video-screenshots/fetch-transcript.py)
  retries a proxy-backed transcript fetch. It reads a machine-specific
  credential file; inspect or adapt its paths before use.
- [`extract.sh`](../scripts/video-screenshots/extract.sh) extracts `t-3`, `t`,
  and `t+3` candidates. Its scratch directory is machine-specific; use the
  direct `ffmpeg` command in the skill for another run directory.
- [`dl-daemon2.sh`](../scripts/video-screenshots/dl-daemon2.sh) contains the
  mirror rotation and VTT/TTML parsing used for a large blocked-source run. It
  is an operational daemon with hard-coded scratch paths, not a default
  downloader for a course repository.

For chopping a long recording into lesson clips, use the separate
[video-lesson-chopping contract](video-lesson-chopping.md) and
[`scripts/chop-specs/`](../scripts/chop-specs/).
