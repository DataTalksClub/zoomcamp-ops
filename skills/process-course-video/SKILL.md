---
name: process-course-video
description: Turn a Zoomcamp workshop recording into lesson-ready text, optional per-lesson clips, and reviewed source-backed illustrations. Use when processing a course or module from video; do not use for transcript-only retrieval, decorative image generation, or publishing media without review.
---

# Process a course video into lesson material

Use this skill to run the complete `video → transcript → lesson text → clips /
illustrations → review` workflow for one workshop or an entire course. The
transcript is evidence and a timestamp map; it is not automatically publishable
lesson prose. Keep the work reproducible so every paragraph, clip, and image can
be traced back to the recording.

## Choose the scope first

Use the smallest mode that satisfies the request:

- `transcript`: acquire or cache a timestamped transcript and validate it.
- `lessons`: turn the transcript and recording into new or revised Markdown
  units.
- `clips`: map lesson boundaries to a human plan and machine-readable chop
  spec, then create reviewable per-lesson videos.
- `illustrations`: find content-bearing moments, extract candidates, score
  them, and refine only the accepted visuals.
- `full`: run the modes in order: transcript, lessons, clips, illustrations,
  then final QA.

If the user asks to “process the course” without narrowing the deliverable,
use `full` and report each mode separately. Do not infer a cohort, a target
module, or permission to publish from the calendar year or from the video URL.

## Non-negotiable operating rules

- Read the target repository's instructions, `git status`, and curriculum
  layout before editing. Preserve unrelated user changes.
- Work in a run-specific `.tmp/course-processing/<course>/<run>/` directory.
  Downloaded videos, raw captions, candidates, crops, contact sheets, prompts,
  rejected generations, and reports are working material, not course assets.
- Never commit a downloaded recording. Never print, copy, or commit proxy/API
  credentials. Use only a video the user is allowed to access; do not bypass a
  private video or an access control.
- Keep the original video, original frame, and original image source unchanged.
  Derived crops and regenerated images are parallel artifacts, not replacements
  for provenance.
- Treat spoken code, URLs, commands, labels, numbers, plots, tables, and UI
  states as exact evidence. Verify them against the screen, source repository,
  notebook, or native export before putting them in lesson text or an image.
  Mark uncertainty for review instead of guessing.
- A visual is optional. Publish zero illustrations when the recording has no
  defensible, durable teaching visual. Never add filler screenshots to meet a
  count.
- Do not commit or push automatically. Publishing a final image, changing an
  existing lesson, and uploading a clip are separate review decisions.

## Phase 0: discover the course and make a run folder

1. Inspect the target repository and its local guidance:

   ```bash
   git status --short
   rg -n "^video_url:|youtube\.com/watch|youtu\.be|Original workshop recording" \
     --glob '*.md' --glob '*.yaml' .
   ```

   Read the relevant `README.md`, module README, unit pages, `STRUCTURE.md`,
   `docs/conventions.md`, and `docs/curriculum-contract.md`. For a new unit,
   also read `templates/unit.md`. For workshop prose, read
   `docs/workshop-best-practices.md`.

2. Build a source map before downloading anything. For every unit, record its
   module, lesson path, video URL or ID, whether the video is shared with other
   units, and the intended source range if one is already known. Deduplicate by
   video ID so a shared recording is downloaded and transcribed once.

3. Create a run-specific working area and an initial status file:

   ```bash
   run_dir='.tmp/course-processing/<course-slug>/<run-id>'
   mkdir -p "$run_dir"/{metadata,transcripts,videos,plans,clips,candidates,crops,finals,reports}
   touch "$run_dir/STATUS.md" "$run_dir/sources.tsv" "$run_dir/illustrations.tsv"
   ```

   Replace the placeholders with a stable slug and run ID. Do not use a broad
   directory such as the repository root for media. Use the format and columns
   in [run-record.md](references/run-record.md).

## Phase 1: acquire and validate the source

Read [acquisition.md](references/acquisition.md) before fetching a video or
caption. It covers the normal YouTube route, the proxy and mirror fallbacks,
caption normalization, disk limits, and validation commands.

The short decision sequence is:

1. Check the run folder and the normal `.tmp/videos/` cache for an existing
   source with the same video ID. Reuse it after validation.
2. Prefer the best available source at or below 720p for chopping. If the
   output is only for frame extraction, 360p is usually enough for a 640×360
   lesson frame. Download the entire file once; section downloads through a
   proxy have produced truncated files.
3. Fetch the platform captions before using speech-to-text. Keep the raw
   caption response and a normalized, timestamped text copy under the run
   folder. If captions do not exist, use the available local transcription
   workflow only after reading its skill instructions, and preserve timestamps.
4. Validate both artifacts. `ffprobe` must parse the video and return a useful
   duration. A transcript must have the expected language, more than a few
   cues, and plausible coverage from the beginning, middle, and end.
5. Record the source URL/ID, title, local path, duration, dimensions, retrieval
   route, transcript path, and any limitation in `sources.tsv`.

Do not start lesson writing or frame selection from an unvalidated download or
from a transcript whose timestamps have not been spot-checked.

## Phase 2: turn the transcript into lesson text

Read [lesson-authoring.md](references/lesson-authoring.md) for the full writing
and chopping procedure. The essential sequence is:

1. Read the transcript beside the target unit or module outline. Find topic
   transitions, demonstrations, explanations, and useful Q&A. Do not split at
   arbitrary minute marks.
2. Make a lesson map with source start/end times, transcript cues, the concept
   being taught, and the paragraph or code block that will carry it. A shared
   video may map to several units; each unit gets only its own topic range.
3. Draft the lesson around the learner's path: what problem is being solved,
   the simplest working approach, what the result shows, why the next step is
   needed, and the final takeaway. Remove promotion, logistics, dead air,
   repeated filler, and irrelevant tangents. Keep a Q&A answer when it teaches
   the subject.
4. Reconstruct exact technical material from the source. Copy commands, code,
   URLs, labels, parameter names, and values only after checking them against
   the recording or the source code. Put searchable exact content in Markdown
   or code blocks, not only in an image.
5. Apply the target course's page contract and style. For the shared Zoomcamp
   layout this means one unnumbered H1, a short opening, `##` sections, local
   relative asset paths, and the video's frontmatter field for a new unit. Do
   not alter existing published video placement merely to match a new-unit
   convention without checking the site caveat in `docs/conventions.md`.
6. Review the draft against the recording and transcript. Resolve every
   uncertainty, preserve meaningful failures when they teach a debugging
   lesson, and remove claims that cannot be supported. Run the repository's
   checker and `git diff --check` after edits.

The lesson page is the learner-facing result. Keep the raw transcript and
source timestamps in the run report unless the user explicitly wants them
published.

## Phase 3: make per-lesson clips when requested

1. Write a human-readable `<module>-chop-plan.md` with one row per unit:
   lesson, source range(s), opening/closing words, removed material, and review
   notes.
2. Write the matching machine-readable spec. Each non-comment line is:

   ```text
   clipname|start-end[,start-end,...]
   ```

   Times are source seconds. Multiple ranges are concatenated to remove a gap
   or tangent from the middle of a lesson. Land boundaries at clean sentence
   ends, not mid-word. Keep genuinely instructional Q&A; remove course promo,
   logistics, dead air, and irrelevant failed demos.
3. Use the repository's `scripts/chop-specs/chop.sh` or an adapted copy after
   reading its README. It re-encodes frame-accurate clips with H.264/AAC and
   applies the established `-14 LUFS`, `-1.5 dBTP` loudness target. Confirm the
   script points to an available `ffmpeg`; the checked-in script contains a
   machine-specific path and may need a local adjustment.
4. Keep clips under the run folder, validate duration and audio with `ffprobe`,
   and watch or inspect every boundary. If a cut is wrong, edit the spec and
   regenerate the affected clip. Never edit a running batch script; wait for
   it to finish or generate an individual clip with standalone `ffmpeg`.
5. If captions are needed for the chopped clips, use the source transcript and
   map each cue into clip-relative time. For multi-range clips, add the
   cumulative duration of earlier kept ranges. Review the generated captions
   against the actual clip.

## Phase 4: extract and refine illustrations

Read [illustration-refinement.md](references/illustration-refinement.md),
[`template/illustration-rubric.md`](../../template/illustration-rubric.md), and
[`template/image-regeneration-workflow.md`](../../template/image-regeneration-workflow.md)
before selecting final assets. The short sequence is:

1. From each finished lesson, identify only content-bearing moments: a diagram,
   architecture relationship, meaningful result, plot, notebook state, or
   durable UI state. Three to eight candidates per unit is a starting point,
   not a quota.
2. Use transcript cues such as “here you can see”, “in this diagram”, and “let
   me show you” to locate timestamps. Extract around each timestamp at `t-3`,
   `t`, and `t+3` seconds. Fast seek is acceptable because the neighboring
   candidates cover keyframe drift.
3. Open every candidate at normal lesson display size. Reject talking heads,
   title cards, transitions, blur, duplicate states, browser/Zoom chrome,
   cursors, popups, watermarks, private chat, and content that is not legible.
4. Score the remaining candidates with the six rubric criteria and record one
   disposition: `keep`, `crop/replace`, or `remove`. The image must teach a
   specific thing that prose or code alone does not already convey.
5. Choose the fidelity path. Preserve or deterministically crop/re-render
   exact code, commands, URLs, numbers, plots, tables, and UI. Use imagegen
   only for a bounded conceptual diagram or relationship where exact pixels
   are not the source of truth. If a table or exact-value list is better as
   searchable lesson markup, convert it to Markdown/HTML instead.
6. Retain the original frame. Crop useful content deterministically; if
   adjacent frames form one canvas, determine the content-side join from what
   is visible and record the order and coordinates. For an imagegen-eligible
   visual, pass the original source image(s) plus the clean crop/merge
   reference to imagegen and inspect the output. A resized or sharpened crop
   alone is not a regeneration.
7. Independently review each proposed final image for content fidelity,
   crispness, overlays, caption/alt text, and lesson context. A generated image
   is not accepted on the implementer's judgment alone.
8. Copy only accepted assets into the target module's `images/` directory,
   embed them immediately after the paragraph they illustrate, and use a
   descriptive alt text that says what the learner should notice. Record the
   full provenance chain in `illustrations.tsv`.

## Phase 5: final QA and handoff

Before declaring the run complete:

- every requested unit has a source map and a transcript or an explicit
  blocked/missing-caption note;
- lesson text agrees with the transcript, recording, source code, and course
  contract;
- every clip has clean boundaries and valid media metadata;
- every candidate has a rubric disposition, and every published image has
  provenance, invariants, a resolved Markdown reference, and review status;
- exact information was not entrusted to a generated approximation;
- no faces, private information, credentials, recording chrome, or disposable
  artifacts entered the tracked course tree;
- the conformance checker, missing-image scan where relevant, and
  `git diff --check` pass;
- `STATUS.md` lists completed modes, changed files, validation commands, and
  remaining human decisions.

Report paths and evidence, not just “done”. Separate `source validated`,
`transcript validated`, `lesson drafted`, `clip reviewed`, `image accepted`,
and `published` states so a later worker can resume without treating a partial
run as complete.
