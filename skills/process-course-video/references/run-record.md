# Run record and handoff format

Use this reference to keep a course-video processing run resumable. All files
below belong under the run-specific `.tmp/course-processing/<course>/<run>/`
directory unless the user explicitly asks for a committed audit report.

## Directory layout

```text
<run>/
├── STATUS.md
├── sources.tsv
├── illustrations.tsv
├── metadata/              # platform metadata and decode checks
├── transcripts/           # raw captions, normalized transcripts, audio for STT
├── videos/                # validated source masters; disposable after processing
├── plans/                 # lesson maps, chop plans, machine specs
├── clips/                 # reviewable per-lesson clips
├── candidates/            # unreviewed frame candidates
├── crops/                 # deterministic crop/merge preparation artifacts
├── finals/                # temporary accepted-image candidates
└── reports/               # review notes and validation output
```

Keep source, transcript, and illustration work keyed by video ID and lesson
stem. Do not use a generic `latest` directory when several runs may coexist.

## `STATUS.md` template

```markdown
# Course video processing: <course> / <run>

Scope: <course, cohort/module, and requested modes>
Started: <date>

## Source summary

| Video ID | Units | Video | Transcript | Route | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `<id>` | `<units>` | `validated` | `validated` | `youtube` | `complete` | |

## Lesson status

| Unit | Source range | Text | Exact items | Clip | Illustrations | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| `<path>` | `<start>-<end>` | `drafted` | `checked` | `pending` | `none` | `<action>` |

## Validation

- [ ] source files pass `ffprobe`
- [ ] transcript begins, ends, and covers the expected recording
- [ ] lesson text reviewed against transcript and recording
- [ ] clip boundaries reviewed
- [ ] illustration candidates have dispositions
- [ ] final images have independent visual verdicts
- [ ] course checker passes
- [ ] `git diff --check` passes

## Changed tracked files

- `<path>` - <why>

## Remaining human decisions

- <decision or `none`>
```

Use state words consistently: `mapped`, `validated`, `drafted`, `checked`,
`rendered`, `reviewed`, `accepted`, `published`, `blocked`, or `not requested`.

## `sources.tsv` columns

Write a header row and one row per unique video ID:

```text
video_id  source_url  title  units  local_video  bytes  duration  dimensions  retrieval_route  raw_captions  normalized_transcript  status  notes
```

Use tabs, keep paths relative to the run directory where possible, and do not
put credentials or signed stream URLs in this file. A signed URL is temporary
and may contain access material; record only the mirror/provider label.

## `illustrations.tsv` columns

Write a header row and one row per candidate, including rejected candidates:

```text
lesson  source_url_or_id  source_timestamp  transcript_cue  candidate_path  source_dimensions  crop_coordinates  source_order  teaching_point  score  disposition  fidelity_path  final_path  required_invariants  reviewer  status
```

Use `remove`, `crop/replace`, or `keep` for `disposition`. Use `pending`,
`needs correction`, `accept`, or `reject` for review `status`; do not collapse a
machine reference check and a visual review into one “done” value.

## Source map and lesson map

Keep a human-readable map in `plans/source-map.md` or the module's plan:

```markdown
| Unit | Video ID | Start | End | Topic | Transcript cue | Asset candidates |
| --- | --- | ---: | ---: | --- | --- | --- |
| `01-topic.md` | `<id>` | `12:40` | `24:10` | `<concept>` | `<cue>` | `12:55, 18:20` |
```

For every range, also note the opening and closing words. This makes an
off-by-one-second correction possible without replaying the entire recording.

## Required provenance chain

For every published lesson image or clip, the record must answer:

```text
Which source URL/ID?
Which local file and source timestamp/range?
Which transcript cue or lesson paragraph?
Which crop/merge or chop operation?
Which exact/source invariants were checked?
Who or what independently reviewed it?
Which tracked file and Markdown reference were published?
```

If one answer is missing, leave the asset in the run folder and mark the item
pending rather than publishing an untraceable result.
