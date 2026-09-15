# Chopping workshop recordings into lesson clips

The complete `video → transcript → lesson map → clip → review` workflow is
[`process-course-video`](../skills/process-course-video/SKILL.md). This page
defines the stable clip contract used by the repository. It does not contain a
course-specific module map or a one-off review log.

## Working area

Keep source masters, transcripts, plans, and generated clips in a gitignored
run directory:

```text
.tmp/course-processing/<course>/<run>/
├── videos/       # source masters
├── transcripts/  # normalized source-relative captions
├── plans/        # human chop plans and machine specs
└── clips/        # reviewable per-lesson output
```

Do not commit the source recording or generated clips unless the course
maintainer explicitly requests a published media change.

## Build the plan

Read the lesson pages and timestamped transcript side by side. Map each lesson
to source ranges at clean sentence boundaries. Keep the topic's explanation,
demo, result, and useful subject-matter Q&A. Remove promotion, logistics, dead
air, repeated filler, and irrelevant tangents. A useful failure stays when it
teaches debugging or a limitation.

Write two synchronized files per module:

1. A human-readable `<module>-chop-plan.md` with the lesson, source range(s),
   opening and closing words, removed material, and review notes.
2. A machine-readable `<module>.spec` with one non-comment line per clip:

   ```text
   clipname|start1-end1[,start2-end2,...]
   ```

Times are source seconds. Multiple comma-separated ranges are concatenated in
order, which removes the gap between them. Fractional seconds are allowed by
the format; use integer seconds when a downstream helper requires them. Lines
starting with `#` are comments.

The spec and the human plan are the source of truth for reruns. If a boundary
is wrong, edit the spec and regenerate the affected clip.

## Render and normalize

Use [`scripts/chop-specs/chop.sh`](../scripts/chop-specs/chop.sh), or an adapted
copy when its local `ffmpeg` path does not exist:

```bash
bash scripts/chop-specs/chop.sh \
  '<source-video>' '<run-dir>/clips' '<module>.spec' '<filename-prefix>'
```

The established output settings are:

- H.264 video, `libx264 -preset faster -crf 23 -pix_fmt yuv420p`;
- AAC audio at 192 kb/s;
- YouTube-oriented loudness normalization:
  `loudnorm=I=-14:TP=-1.5:LRA=11`.

Keep source resolution; re-encoding cannot restore source detail. Validate each
clip with `ffprobe`, then inspect the first and last seconds for clipped speech,
missing context, abrupt audio, or an unintended overlap/gap. Do not edit the
chop script while a batch is running. Edit the spec after the batch finishes,
then rerun the affected output.

## Captions for chopped clips

Source transcript cues are source-relative. For a kept range `[start, end)` and
cue time `t`, map the cue to:

```text
clip time = duration of earlier kept ranges + (t - start)
```

[`scripts/youtube-upload/clip_transcript.py`](../scripts/youtube-upload/clip_transcript.py)
implements this mapping for its integer-second spec format. Review captions
against the rendered clip, especially at multi-range joins.

## Acceptance checklist

- [ ] Every lesson has a source range and opening/closing words.
- [ ] Boundaries do not cut sentences or remove required context.
- [ ] The spec and human plan agree.
- [ ] Every output parses with `ffprobe` and has usable audio.
- [ ] Every clip's start and end were visually or audibly reviewed.
- [ ] Source files and generated clips remain in the run's gitignored area.
- [ ] The run record identifies the source URL/ID and the exact spec used.
