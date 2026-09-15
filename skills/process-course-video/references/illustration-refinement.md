# Illustration extraction, refinement, and review

Use this reference after the lesson text and a timestamped transcript exist.
The goal is the smallest set of clear visuals that adds teaching value to the
lesson. A recording frame is source evidence, not automatically a publishable
illustration.

## 1. Select moments, not screen changes

Read the lesson paragraph, transcript cue, and video together. For each
candidate moment, write one sentence:

```text
This image teaches <specific fact, relationship, result, or state change>.
```

If the sentence cannot be made specific, do not extract the frame. Good
signals include:

- a conceptual diagram or architecture relationship;
- a process or state transition that is difficult to explain in prose;
- a meaningful plot, metric, output, or application result;
- a notebook cell or UI state whose visible result is instructional;
- a whiteboard mapping of concepts, components, or data flow.

Use transcript phrases such as “here you can see”, “in this diagram”, “let me
open”, “let me show you”, and “the result is” to find likely timestamps. Choose
three to eight moments per unit as an initial search budget, not a publishing
quota. A unit can correctly end with no image.

Reject early when the frame is only:

- a presenter, webcam tile, chat panel, title card, or course promotion;
- browser tabs, Zoom controls, a cursor, watermark, popup, or unrelated window;
- an empty setup screen or a command being typed with no useful result;
- a transient dashboard or personal session that will not remain useful;
- a table or exact-value list that is clearer and more accessible as native
  Markdown/HTML.

## 2. Extract neighboring candidates

Create a bounded candidate directory for each unit:

```bash
candidate_dir="$run_dir/candidates/<module>/<unit-stem>"
mkdir -p "$candidate_dir"
```

For a timestamp in source seconds, extract three frames:

```bash
moment_seconds=<source-seconds>
for offset in -3 0 3; do
  candidate_seconds=$((moment_seconds + offset))
  if [ "$candidate_seconds" -lt 0 ]; then candidate_seconds=0; fi
  ffmpeg -loglevel error -ss "$candidate_seconds" \
    -i "$video_path" -frames:v 1 -q:v 3 \
    "$candidate_dir/<timestamp>-$(printf '%+d' "$offset").jpg" -y
done
```

`-ss` before `-i` gives fast seek. Exact frame accuracy is unnecessary for this
candidate pass because the ±3 second neighbors cover keyframe drift and slide
transitions. The repository helper
[`extract.sh`](../../../scripts/video-screenshots/extract.sh) automates the
same `t-3`, `t`, `t+3` pattern, but its scratch path is machine-specific. Use
the direct command or adapt the helper to the current run directory.

If there is no transcript, use the video duration to sample a small number of
evenly spaced frames, then inspect them manually. Do not present an evenly
sampled frame as transcript-aligned provenance.

## 3. Inspect every candidate visually

Open the actual files with the image viewer available to the worker. In Codex,
use `view_image` for local files. Inspect twice:

1. at the width used on the lesson page, to test whether the learner can read
   the relevant content;
2. at 100%, to see blur, compression, clipped edges, interpolation, or hidden
   overlays.

Choose the clearest complete state, not necessarily the middle timestamp. A
result after it renders is usually more useful than the empty prompt before
it. Reject fades, slide wipes, half-drawn diagrams, motion blur, occlusion, and
duplicates of an already selected frame.

Never accept a frame from its timestamp or filename without opening it.

## 4. Score and disposition candidates

Read the full [illustration rubric](../../../template/illustration-rubric.md).
For each candidate, score 0–2 for each criterion:

| Criterion | Question |
| --- | --- |
| Instructional contribution | What would the learner lose if this disappeared? |
| Relevance | Does it directly support this lesson's concept or action? |
| Readability and focus | Is the useful content clear at normal display size? |
| Complementarity | Does it add evidence beyond the prose, code, and other images? |
| Durability | Will it remain useful outside the presenter's live session? |
| Caption/accessibility | Does the caption/alt text say what to notice? |

Use the hard gates before considering the total (maximum 12):

- instructional contribution 0 means remove;
- unreadable content that cannot be safely improved means remove;
- personal information, credentials, tokens, or private chat must be removed
  or safely redacted;
- exact tables/lists should become native lesson markup unless their visual
  layout is itself the teaching point;
- near-identical frames collapse to the smallest useful set;
- a caption must match the actual image.

Record a row even for rejected candidates. The normal dispositions are
`keep`, `crop/replace`, and `remove`.

## 5. Choose the fidelity path

Decide from what the learner must learn, not from which tool produces the most
polished file.

| Source content | Safe final path |
| --- | --- |
| Exact code, shell command, URL, config, number, plot, table, metric, or UI state | Native Markdown/code/table, original source, deterministic crop, or deterministic re-render |
| Conceptual diagram, architecture, process, or relationship where exact pixels are not authoritative | Crop/merge the source, then imagegen redraw with explicit invariants |
| Mixed visual with exact labels and conceptual layout | Preserve exact text deterministically; use imagegen only if every required label and relationship can be independently checked |
| A table or comparison matrix needed for search/copy/compare | Markdown/HTML table; keep an image only when spatial layout carries meaning |

When uncertain, use the deterministic path. A blurry exact screenshot is better
handled by a native re-render or a transparent review blocker than by a model
guessing the source of truth.

## 6. Prepare a crop without destroying the source

Retain the original candidate under `candidates/`. Record its dimensions and
the useful rectangle as `x,y,width,height` in the manifest. Crop only to remove
unrelated recording frame, black borders, browser/Zoom chrome, a webcam tile,
or an irrelevant panel.

With ImageMagick:

```bash
magick "$candidate_path" \
  -crop '<width>x<height>+<x>+<y>' +repage \
  "$run_dir/crops/<unit-stem>-<timestamp>-crop.png"
```

With FFmpeg when ImageMagick is unavailable:

```bash
ffmpeg -v error -i "$candidate_path" \
  -vf 'crop=<width>:<height>:<x>:<y>' -frames:v 1 \
  "$run_dir/crops/<unit-stem>-<timestamp>-crop.png" -y
```

Inspect the crop. It is a preparation artifact, not automatically a crisp
final. Do not crop away a label, arrow, axis, result, or context needed to
interpret the teaching point. If adjacent frames are pieces of one canvas,
determine whether they join left/right or top/bottom from visible content;
record source order, join coordinates, and seam inspection. Never infer order
from filenames alone.

## 7. Regenerate conceptual visuals safely

If the imagegen skill is available, read its complete instructions before
calling it. Provide:

- every retained original source image unchanged;
- the clean crop or correctly merged reference;
- a description of the learner's teaching point;
- an explicit list of required labels, entities, values, ordering, arrows, and
  relationships;
- negative constraints: no face, webcam tile, browser/Zoom controls, cursor,
  watermark, unrelated panel, extra component, invented metric, or decorative
  UI.

A useful prompt shape is:

```text
Create a crisp, high-resolution educational illustration from the supplied
original source and clean reference. Preserve the reference's composition and
teaching meaning.

Required entities and relationships:
- <entity or label exactly as checked against the source>
- <arrow/direction/order>
- <value or state that must remain exact>

The learner should notice: <one teaching point>.
Do not add labels, values, components, arrows, metrics, people, camera tiles,
browser/Zoom chrome, cursors, watermarks, or unrelated decoration.
Make all required text legible at normal lesson-page size.
```

The original image(s) plus the clean reference must remain available for
comparison. A 2×/3× resize or sharpened crop may help the reviewer inspect the
source, but it must not be the only imagegen input. Save each generation as a
temporary sibling; never overwrite the original or call a prompt successful
without opening the actual output.

Reject and correct one issue at a time when the result changes a label, value,
arrow, ordering, relationship, or teaching meaning. A polished image with a
wrong `ND` label, invented result, or rearranged flow is a failed asset.

## 8. Re-render exact visuals deterministically

For code, commands, URLs, plots, numeric output, tables, or UI controls, use
the source notebook, code, browser state, vector data, or native export when
available. A deterministic crop is acceptable when the source is already
sharp. A simple presentation baseline for exact content is:

```bash
magick "$crop_path" \
  -filter Lanczos -resize 300% \
  -unsharp 0x0.5+0.5+0 \
  "$run_dir/finals/<unit-stem>-<slug>-crisp.png"
```

This can improve display size; it cannot recover detail that was absent in a
blurry recording frame. Do not call an enlarged or sharpened crop “regenerated”
when important text remains unreadable. Prefer native Markdown for exact tables
and lists, and compare every value against the source.

If an exact UI contains a face or overlay inside the useful pixels and it
cannot be removed without changing the state, leave the asset unpublished and
record the blocker. Do not paint over evidence.

## 9. Publish only reviewed assets

Use the target repository's module layout. In the shared Zoomcamp layout, an
accepted image belongs in the module's local `images/` directory. Use a
collision-resistant name such as:

```text
<unit-stem>-NN-<kebab-slug>.jpg       # accepted source-backed frame
<unit-stem>-NN-<kebab-slug>-crisp.png # accepted crisp replacement
```

Temporary names such as `*-crop`, `*-imagegen-pilot`, and rejected variants
stay under `.tmp/`. Before copying an asset:

1. inspect it at lesson display size and at 100%;
2. compare all exact invariants against the original/source;
3. confirm no face, private content, cursor, watermark, or recording chrome
   remains;
4. write an alt text that says what the learner should notice, with no trailing
   period under the shared conventions;
5. embed it on its own line immediately after the paragraph it illustrates;
6. keep the critical code, command, value, or conclusion in text as well.

Example reference:

```markdown
![The retriever combines keyword and vector results before reranking](images/02-search-01-hybrid-retrieval-crisp.png)
```

Do not commit a candidate directory, contact sheet, crop, prompt, rejected
generation, downloaded video, or unreviewed manifest unless the user
explicitly asks for an audit artifact in the repository.

## 10. Use independent review and record provenance

For every accepted replacement, separate implementation from review. The
reviewer must open the source and final files instead of trusting filenames or
the prompt. Check:

- source timestamp and lesson paragraph match;
- crop rectangle and adjacent-frame order are correct;
- the final is legible at normal size and not visibly interpolated or blocky;
- exact labels, numbers, code, URLs, plots, arrows, and relationships are
  unchanged where they are authoritative;
- faces, camera tiles, browser/Zoom controls, cursors, watermarks, and unrelated
  overlays are absent;
- the Markdown path, alt text, caption, and target file all resolve.

Record `accept`, `reject`, or `needs correction` with the checks performed. An
imagegen result without an independent verdict remains pending.

For a course-wide pass, regenerate the active inventory with
[`audit_illustrations.py`](../../../scripts/audit-illustrations/audit_illustrations.py)
and review both complete lists: every active unit and every active illustration
reference. Distinguish machine/reference status from independent visual status.

At minimum, each `illustrations.tsv` row should contain:

```text
lesson  source_url_or_id  source_timestamp  transcript_cue  candidate_path
source_dimensions  crop_coordinates  source_order  teaching_point  score
disposition  fidelity_path  final_path  required_invariants  reviewer  status
```

The provenance chain must remain reconstructable:

```text
YouTube URL/ID + timestamp
  → validated local video
  → candidate frame
  → rubric decision
  → deterministic crop/merge
  → imagegen redraw or deterministic re-render
  → reviewed module image + Markdown reference
```
