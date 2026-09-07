---
name: extract-youtube-illustrations
description: Extract and evaluate candidate instructional illustrations from a Zoomcamp recording. Use when a local workshop video needs useful frames for lesson pages; do not use for decorative image generation.
---

# Extract YouTube illustrations

Turn a local workshop recording into a small, reviewable set of candidate
frames. The goal is not to capture every screen change. The goal is to find
images that add instructional value to the written lesson.

Read [`template/illustration-rubric.md`](../../template/illustration-rubric.md)
before selecting final images.

## Inputs and working area

- A local video, normally under `.tmp/videos/`.
- Lesson text, a chop plan, or timestamped transcript to identify teaching
  moments.
- A target module directory when an accepted image will eventually be copied
  into `cohorts/<year>/<module>/images/`.

Keep unreviewed frames under `.tmp/illustrations/<module>/candidates/`. They
are working files, not course assets.

## Workflow

1. Read the lesson text around the proposed timestamp. Identify the exact
   concept, result, relationship, or state transition the frame is meant to
   support.
2. Reject recording chrome early: presenter webcam, chat, browser tabs,
   controls, title cards, and unrelated windows are noise unless they are the
   subject of the lesson.
3. Extract a small number of frames around each useful timestamp. For example:

   ```bash
   mkdir -p .tmp/illustrations/<module>/candidates
   ffmpeg -ss <HH:MM:SS> -i .tmp/videos/<source>.mkv \
     -frames:v 1 -q:v 2 \
     .tmp/illustrations/<module>/candidates/<timestamp>.jpg
   ```

4. Inspect the frames at normal rendered size. Crop or replace a frame when
   the underlying evidence is useful but the capture is cluttered or hard to
   read.
5. Score every candidate with the six criteria in the illustration rubric.
   Record the timestamp, lesson, intended teaching point, score, decision, and
   proposed alt text in a manifest next to the candidates.
6. Copy only accepted frames into the course module's `images/` directory,
   using a descriptive filename and a caption that says what the learner
   should notice.

## Selection rules

- Keep the minimum set of images that adds information beyond the lesson's
  prose and code.
- Prefer a meaningful result, diagram, relationship, or user-visible state
  over a setup screen or a command being typed.
- Do not preserve a frame merely because it appeared in the recording.
- Do not use an image as the only place where critical code, commands, or
  values are documented; put those in text as well.
- If a candidate cannot pass the rubric after cropping, remove it.

Do not commit the source video, candidate directory, contact sheets, or
manifest unless a course workflow explicitly calls for them. Do not commit or
push accepted images automatically; let the course maintainer review the
lesson context and the final filenames and captions first.
