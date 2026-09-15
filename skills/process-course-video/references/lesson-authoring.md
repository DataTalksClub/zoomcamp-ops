# Transcript-to-lesson authoring and video chopping

Use this reference after a timestamped transcript and validated source video
exist. It explains how to turn spoken workshop material into useful course
pages and, when requested, per-lesson clips.

## 1. Establish the lesson boundary from content

Read the module README, the target unit files, and the transcript together.
Build a map before writing prose:

| Lesson | Source start | Source end | Topic | Transcript cues | Planned evidence |
| --- | ---: | ---: | --- | --- | --- |
| `NN-unit.md` | `M:SS` | `M:SS` | one concept | cue phrases | code/result/visual |

Use topic transitions, not equal-length slices. Strong transition signals are
the instructor naming a new problem, opening a new tool or file, beginning a
diagram, showing a result, summarizing a tradeoff, or answering a subject
question. Keep a shared recording's ranges disjoint unless a repeated opening
is intentionally useful.

If there is an existing unit, use its headings and code as a starting point,
but verify them against the source. If the unit is new, decide its one-sentence
learning objective before drafting. A useful objective names what a learner can
explain or do after the unit, not merely the topic mentioned in the video.

## 2. Separate evidence layers

Use each source for what it can establish:

1. The transcript establishes spoken sequence, terminology, explanations, and
   approximate timestamps.
2. The video establishes what was actually shown, exact visible commands and
   values, UI state, and the result of a live demonstration.
3. The course repository, notebook, or linked source establishes exact code,
   configuration, URLs, and durable implementation details when the recording
   is blurry or speech recognition is uncertain.
4. Existing lesson text establishes the course's intended structure and what
   has already been explained, but it is not proof that a new claim was said or
   shown in the recording.

When these disagree, investigate the source and record the decision. Do not
silently “correct” the transcript by inventing a likely command or value.

## 3. Extract the teaching sequence

For each lesson, make a short outline in the run report before writing final
Markdown:

```text
problem → simplest working idea → implementation/demo → observed result
→ limitation or question → next idea → takeaway
```

This is a guide, not a requirement to force every lesson into the same shape.
Preserve a conceptual explanation when there is no demo, and preserve a useful
failure when debugging is part of the lesson.

Keep:

- definitions, mental models, architecture relationships, and tradeoffs;
- commands and code that the learner must run or understand;
- outputs, plots, metrics, and state changes that support a conclusion;
- warnings about an approach that failed and the reason it failed;
- Q&A that answers the subject or explains a production decision.

Remove or move to a short note:

- opening promotion, “star the repo”, registration, and schedule reminders;
- logistics, repeated setup narration, dead air, and “I will answer later”
  filler;
- unrelated tangents and failed demos whose failure does not teach anything;
- conversational repetition that adds no new explanation.

Do not remove a Q&A answer only because it occurred after the main demo. A
production deployment answer or a clarification can be the most durable part
of a workshop.

## 4. Draft the Markdown unit

For the shared Zoomcamp layout, follow the contract in `STRUCTURE.md` and the
wording rules in `docs/conventions.md`. The usual new-unit skeleton is:

```markdown
---
video_url: https://www.youtube.com/watch?v=<id>
---

# <Unnumbered lesson title>

<One or two sentences describing what the learner will understand or build.>

## <First concept>

<Explanation, then a focused code block or native table when needed.>

## <Demo or result>

<What happened and what the learner should notice.>
```

Apply these writing rules:

- keep one H1, unnumbered; the filename supplies the unit's order;
- open with the purpose before the first `##` heading;
- use short, focused sections and code blocks rather than a transcript dump;
- explain why a command or abstraction is introduced before relying on it;
- put exact commands, code, URLs, tables, and values in searchable native
  Markdown or code blocks;
- write image alt text and captions around what the learner should notice;
- link assets locally inside the module and keep the module self-contained;
- match the course's established syntax and vocabulary, including `uv run`
  conventions where they apply;
- in the shared conventions, avoid bold formatting and em dashes in course
  prose.

The `video_url` frontmatter rule is for new units. Before changing an existing
published unit's video placement, reread the caveat in `docs/conventions.md`:
the website's current consumer may not yet read the field, so an apparently
clean conversion can remove a visible video from a live page.

## 5. Verify every technical statement

Use a verification table for material that could be misheard:

| Item | Spoken/transcribed form | Source checked | Final form | Status |
| --- | --- | --- | --- | --- |
| command | uncertain cue | source file / video timestamp | exact code block | verified |
| metric | `...` | rendered output | prose + value | verified |
| URL | partial speech | source repository | link | verified |

Pay special attention to:

- package and module names that sound alike;
- underscores, hyphens, capitalization, and pluralization;
- port numbers, model names, dimensions, thresholds, and metric values;
- command flags and environment variable names;
- code shown on a screen but not read aloud;
- negative statements such as “do not”, “without”, or “this fails”.

If the recording is not sufficient, inspect the linked source. If neither is
available, leave a clear review marker in the working draft and report it.
Never turn a best guess into course instructions.

## 6. Review the text against the source

Read the draft once for learner flow and once against the evidence. Check:

1. The opening says what the unit teaches.
2. Every heading covers one coherent block from the source map.
3. The sequence of code, result, and explanation matches the recording.
4. No unsupported claim, accidental live-only detail, or hidden credential was
   introduced.
5. Exact values and commands are copyable and agree with the source.
6. A learner can understand the takeaway without watching the video.
7. Images, if any, appear beside the paragraph they support and are not the
   only place critical information is documented.

Then run the course checker appropriate to the target repository and:

```bash
git diff --check
```

Do not treat a clean Markdown parse as evidence that the lesson is technically
correct. Source review is the correctness gate.

## 7. Create the chop plan

When the requested output includes per-lesson video, keep the source of truth
in two files under the run folder:

1. A human plan, for example `<module>-chop-plan.md`, with lesson, source
   range, opening/closing words, material removed, and review notes.
2. A machine spec with one line per clip:

   ```text
   clipname|start1-end1[,start2-end2,...]
   ```

Times are in source seconds. Fractional seconds are useful when a caption cue
ends between whole seconds, but use integer seconds if the downstream helper
requires them. Lines beginning with `#` are comments. Multiple ranges are
concatenated in order, so the output clip time after a cut is not the original
source time.

Choose boundaries at clean verbal endings. Review the few seconds before and
after every boundary for:

- half-spoken words or clipped sentences;
- a promised result that was left outside the clip;
- an opening teaser that belongs to the next lesson;
- a source-range overlap or accidental gap;
- a lesson that starts with context missing from the prior clip.

The repository's format is documented in
[`scripts/chop-specs/README.md`](../../scripts/chop-specs/README.md).

## 8. Render and review clips

Use the checked-in `scripts/chop-specs/chop.sh` or a portable adapted copy. Its
established output is H.264 video, AAC audio, and loudness normalization at
`I=-14:TP=-1.5:LRA=11`. Keep output in the run folder:

```bash
bash scripts/chop-specs/chop.sh \
  "$run_dir/videos/<source>.mkv" \
  "$run_dir/clips" \
  "$run_dir/plans/<module>.spec" \
  '<module-prefix>'
```

The checked-in script currently contains a machine-specific `ffmpeg` path.
Confirm or adapt that path before running. Do not edit the script while a batch
is running; the batch can reread the file by byte offset and corrupt the run.
Edit the spec safely, wait for the batch to finish, then rerun the affected
clip or module.

For each clip, check:

```bash
ffprobe -v error -show_entries format=duration \
  -show_entries stream=codec_type,codec_name,width,height \
  -of default=noprint_wrappers=1 "$run_dir/clips/<clip>.mp4"
```

Inspect the first and last 10–20 seconds, not just the metadata. If the clip
has multiple kept ranges, verify that the join is intelligible and that the
audio does not jump unexpectedly.

## 9. Make clip-relative captions when needed

The original transcript uses source-relative timestamps. For each kept range
`[start, end)` and cue time `t`, keep the cue when `start ≤ t < end` and map it
to:

```text
clip_time = cumulative_duration_of_prior_ranges + (t - start)
```

The repository helper
[`scripts/youtube-upload/clip_transcript.py`](../../scripts/youtube-upload/clip_transcript.py)
implements this mapping for its integer-second spec format. Review its output
against the rendered clip, especially when a cue starts just before a cut or a
multi-range clip has a short join.

## 10. Handoff state

Mark each lesson separately in `STATUS.md`:

```text
source mapped | transcript validated | lesson drafted | exact items checked
| clip rendered | clip reviewed | illustrations reviewed | published
```

An unfinished lesson, a missing transcript, a source range that still clips a
word, or a technical item marked “verify” is not complete. Leave the evidence
and the next action in the run report so another worker can continue without
repeating acquisition.
