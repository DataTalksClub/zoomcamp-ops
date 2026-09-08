# Image regeneration workflow

Use this workflow when a useful Zoomcamp illustration is a blurry workshop
frame, includes a presenter or camera tile, or is difficult to read at the
size used on the lesson page.

The goal is to preserve the teaching content while producing a clean,
readable illustration. Do not regenerate an image simply because it is old or
visually imperfect.

## Choose the output style before editing

Choose the output style from the lesson's teaching point, not from the
source's file extension or how polished a generated image might look.

1. **Preserve, or crop and crispify, the screenshot** when the screenshot is
   instructional evidence: an exact UI state, notebook output, plot, table,
   code, command, or result. Crop only when needed to isolate useful content;
   then keep the original source and use a deterministic crop/export or a
   deterministic re-render. The source pixels, labels, values, and state are
   the authority.
2. **Use imagegen for a clean iconographic or diagrammatic redraw** when the
   lesson teaches a conceptual relationship or process and exact pixels are
   not the source of truth. It may improve composition and legibility, but it
   must preserve the intended entities, relationships, direction, and meaning.
3. **Use deterministic re-rendering** for exact code, numbers, plots, tables,
   URLs, or UI. Render from the original source, notebook, browser state,
   vector data, or code. Do not ask imagegen to recreate source-of-truth text
   or numeric content.

### Decision tree

```text
What does the learner need to learn from the image?
            │
            ├─ Exact evidence: UI state, notebook output, plot, table,
            │  code, command, URL, number, or result?
            │       └─ Preserve, crop only if useful-content isolation is needed,
            │          then deterministic crop/export or deterministic re-render.
            │
            └─ Conceptual relationship or process; exact pixels are not truth?
                    └─ Imagegen redraw from the retained original source and
                       the clean/merged reference, then independently review.
```

If the answer is uncertain, use the deterministic path and record the reason.
The cost of retaining an exact screenshot is lower than the cost of silently
changing the learner's evidence.

Imagegen is a good fit for:

- architecture and process diagrams;
- conceptual whiteboards;
- simple matrices or mappings with a bounded set of exact labels;
- diagrams where the relationships matter more than the original pixels.

Do not use imagegen for:

- source code, shell commands, URLs, or configuration that must be exact;
- plots, tables, or evaluation results whose numeric values matter;
- screenshots of a live UI where exact labels or controls are the lesson;
- any image where a generated approximation could change the learner's
  conclusion.

For those cases, use the original source, a deterministic crop, or a
deterministically rendered replacement from the notebook or code.

## Capability gate for delegated workers

Before starting, check whether the worker has access to the `imagegen` skill.

If you have access to the `imagegen` skill, do this:

1. Read the skill instructions completely.
2. Inspect the local source with `view_image`.
3. Retain the original non-crisp source image(s) unchanged. Crop only when a
   crop is needed to isolate useful teaching content; never treat the crop as
   a replacement for the source.
4. If adjacent source screenshots make one teaching surface, join them on the
   correct content side and orientation before regeneration. Determine left/
   right or top/bottom from the content, not filenames; record the join order
   and coordinates.
5. Pass the original source image(s) and the merged source reference (when a
   merge was needed) to imagegen. A 2×/3× resized, sharpened, or otherwise
   derived image must never be the only imagegen input.
6. Use the built-in imagegen workflow with explicit labels, values, layout,
   and negative constraints.
7. Inspect the generated image and reject it when any instructional invariant
   is wrong.

If you do not have access to the `imagegen` skill, do not claim to have
regenerated the image and do not invent an image-generation command. Instead:

- use a deterministic crop when it cleanly removes the unwanted frame;
- use the original asset, a source notebook, or a code/vector rendering when
  exact text, numbers, code, or UI controls must be preserved;
- do not paint over a face, camera tile, or overlay when doing so could damage
  the teaching content;
- record the source path, crop coordinates, remaining problem, and required
  invariants in the worker report; then hand the asset to a worker with the
  `imagegen` skill or to the parent agent.

The capability check is part of the acceptance record. A worker without the
skill may prepare inputs and evidence, but cannot mark an imagegen replacement
as complete.

## Source, crop, and merge gates

These gates apply before either generation or deterministic replacement:

- **Original-source gate:** retain every original non-crisp source image in its
  original form and record its repository path, dimensions, and provenance.
  Never overwrite, delete, or replace it with a resized derivative.
- **Useful-content gate:** crop only when it isolates the useful content or
  removes unrelated recording frame, chrome, borders, cursor, face, or panel.
  Record crop coordinates and keep the crop as a preparation artifact.
- **Adjacent-source gate:** when neighboring screenshots are pieces of one
  canvas, identify the content-side join and orientation from visible content,
  merge them deterministically, inspect the seam, and record the ordered source
  paths. Do not regenerate separately arranged fragments and hope imagegen
  infers their order.
- **Imagegen-input gate:** provide imagegen with all original source image(s)
  plus the merged source reference when applicable. A 2×/3× resized derivative
  may be a supplemental readability aid, never the sole or authoritative
  input. Keep all source and merge references available for reviewer comparison.

## Two-agent implementation and review gate

Use two distinct roles for every accepted change:

1. An **implementation agent** inspects the lesson and source, selects the
   output style, makes the crop/merge/regeneration or deterministic render,
   updates the Markdown reference, and records provenance and invariants.
2. After the implementation agent stops, launch an **independent reviewer agent**
   with the implementation evidence and source paths. The reviewer must
   inspect, rather than trust the prompt or filename:

   - crop direction, adjacent-source order, join seam, and orientation;
   - visual crispness at normal lesson-page size and at 100% inspection;
   - exact text, labels, values, code, URLs, plots, and semantic relationships;
   - faces, webcam/camera tiles, browser/Zoom chrome, cursors, watermarks, and
     unrelated overlays;
   - every Markdown reference, alt text/caption, and absence of broken or
     stale references.

The reviewer records `accept`, `reject`, or `needs correction`, with the
checks and remaining defects. The implementation agent cannot self-approve a
generation. A polished image without this independent verdict is still
pending.

## Required audit lists

Keep one committed, dated audit report for each active scope. It must contain
both of these complete lists:

1. **Active units:** every active unit and whether an instructional illustration
   is present or missing.
2. **Active illustrations:** every active illustration reference, its resolved
   target, machine-check result, and quality status (`accepted`, `review
   required`, or `action required`). The quality status must distinguish
   filesystem/reference checks from the independent visual verdict.

The reusable generator is
[`scripts/audit-illustrations/audit_illustrations.py`](../scripts/audit-illustrations/audit_illustrations.py);
the current committed snapshot is
[`docs/current-illustration-audit.md`](../docs/current-illustration-audit.md).
Regenerate the report after scope or reference changes, then have the reviewer
check the report's missing-reference and review queues before acceptance.

## Workflow

## The crisp-regeneration pattern

The standard imagegen workflow is deliberately two-stage, with provenance
preserved as a parallel input:

```text
original non-crisp source image(s) ───────────────┐
        │                                         │
        ├─ retain unchanged                       │
        ▼                                         │
deterministic crop and, when needed,              │
content-side merge/orientation reference ────────┤
                                                  ▼
                                  imagegen receives original(s)
                                  plus the clean/merged reference
                                                  │
                                                  ▼
high-resolution, crisp, camera-free lesson asset
```

Cropping and regeneration solve different problems. The crop removes the
webcam tile, face, browser/Zoom chrome, black borders, and unrelated panels so
the clean reference isolates the teaching content. Imagegen receives that
reference together with the retained original source image(s), then rebuilds
the bounded content as a clean, high-resolution raster with sharper edges and
readable labels. The original is provenance/context, not permission to discard
the crop or let a resized derivative become the sole input.

The crop is a reference input, not the final deliverable. A cropped screenshot
that is still soft, pixelated, or difficult to read should not be accepted
just because the distracting frame is gone. Regenerate it from the crop with
an explicit request for crisp, high-resolution output and inspect the result
at the size used on the lesson page.

## What counts as a crisp replacement

“Crisp” describes the visible result, not the filename, file format, or pixel
dimensions. A replacement is acceptable only when it passes both the visual
quality gate and the content-fidelity gate.

### Acceptable improvements

- **Imagegen regeneration:** for a bounded diagram, conceptual illustration,
  matrix, or process visual, use the clean crop as a reference and have
  imagegen redraw it at high resolution. The regenerated image must have clean
  edges, legible typography, and no recording artifacts.
- **Deterministic re-rendering:** for exact code, commands, URLs, plots,
  numeric results, or UI states, render from the original source, notebook,
  browser state, or vector data. This is acceptable because it preserves the
  source of truth, not because it makes a blurry screenshot larger.
- **A crop followed by regeneration:** cropping is acceptable preparation when
  it removes a face, camera tile, browser/Zoom chrome, cursor, or unrelated
  panel. The crop itself is not the crisp replacement unless the source was
  already sharp and remains readable at lesson size.
- **Visible improvement:** at normal lesson-page width, important text is easy
  to read, straight lines and shapes have clean boundaries, and fine details
  are not smeared or blocky. At 100% inspection, the asset must not reveal
  obvious interpolation blur or compression damage.
- **Verified fidelity:** every required label, value, line break, arrow,
  relationship, and ordering is checked against the source and the lesson.
  Imagegen output is accepted only after this comparison.

### Not acceptable as a final fix

- enlarging a blurry crop with 2×, 3×, or any other interpolation and calling
  the result regenerated;
- applying sharpening, unsharp masking, denoising, or contrast changes to a
  soft screenshot without rebuilding the missing detail;
- changing JPG to PNG, increasing the DPI metadata, or changing the filename
  to `*-crisp.png` without a visible quality improvement;
- removing only the camera frame while leaving the instructional text
  pixelated or unreadable;
- using imagegen output that invents, misspells, drops, or rearranges labels,
  code, URLs, numbers, table values, arrows, or UI controls;
- accepting a polished image that changes the teaching meaning, even if it
  looks sharper;
- leaving a face, webcam tile, browser/Zoom controls, cursor, watermark, or
  unrelated overlay in the published asset;
- judging only from image dimensions, file size, a thumbnail, or the generation
  prompt. The actual output must be opened and reviewed at lesson display size.

An enlarged or sharpened image may be kept as a temporary diagnostic or as a
fallback when the original is already sufficiently sharp. It must not be
reported as a successful crisp regeneration when the source itself is soft.
If imagegen is unavailable, record the candidate and the missing capability;
do not silently substitute a cosmetic upscale.

This pattern applies only when generation can preserve the teaching meaning.
For exact code, URLs, numbers, plots, and UI states, use the crop as a guide
and produce the crisp replacement deterministically from the original source,
not by asking imagegen to redraw exact text.

## End-to-end path: YouTube recording to lesson image

Course images commonly begin as frames from a workshop recording. Treat the
recording as a traceable source, not as a folder of ready-to-publish assets:

1. **Resolve the lesson and recording.** Read the lesson, its caption, and the
   timestamped transcript or chop plan. Identify the moment that demonstrates
   the concept. Record the YouTube URL/ID and timestamp.
2. **Fetch the source locally.** Use the YouTube-video workflow to keep the
   video under the repository's gitignored `.tmp/videos/` directory. Prefer the
   best available stream; YouTube may be limited to 720p, and re-encoding cannot
   recover detail that is absent from the source.
3. **Extract candidate frames.** Use `ffmpeg` around the timestamp and keep
   the unreviewed frames under `.tmp/illustrations/<module>/candidates/`.
   Extract only a small set of plausible teaching moments; do not turn every
   video frame into an image.
4. **Score and select.** Read the surrounding lesson text and apply the
   illustration rubric. Keep a frame only when it adds information beyond the
   prose/code. Record the timestamp, score, decision, and proposed alt text.
5. **Cut the useful region.** For a retained frame, crop the source
   deterministically to the meaningful screen/diagram area. Remove the face,
   webcam tile, browser/Zoom chrome, controls, cursor, black borders, and
   unrelated panels. Keep the crop in `.tmp/` and record its coordinates.
6. **Make the crop crisp.** For an imagegen-eligible diagram or bounded
   illustration, pass the original source image(s) plus the clean crop or
   content-side merged reference to imagegen and ask it to regenerate a crisp,
   high-resolution, camera-free lesson asset. For exact code, URLs, plots,
   values, and UI states, create a deterministic high-quality replacement from
   the original source instead; imagegen must not redraw the source of truth.
7. **Review at lesson size.** Compare the generated/re-exported image with the
   crop and the lesson. Reject blur, clipping, invented labels, altered
   numbers, changed relationships, remaining overlays, or any loss of teaching
   meaning. Keep the original frame for auditability.
8. **Publish the accepted asset.** Copy only the accepted sibling asset into
   the module `images/` directory, update the Markdown reference and alt text,
   and write the source timestamp, crop coordinates, disposition, prompt
   iterations, and validation result in the rollout report.
9. **Commit and validate.** Make one focused commit for the accepted image and
   its reference/report entry. Run the missing-reference scan and
   `git diff --check`; never commit videos, candidate frames, crops, prompts,
   contact sheets, or rejected generations.

The final course asset therefore has this provenance:

```text
YouTube URL + timestamp
        → local candidate frame
        → rubric decision
        → deterministic crop
        → imagegen crisp regeneration or deterministic re-export
        → reviewed module image + Markdown reference
```

## Second pass: make existing crops crisp

The first cleanup pass may remove the camera frame without improving the
source resolution. Treat every active `*-cropped.png` reference as a candidate
for a second pass; do not assume that a cleanly framed crop is readable.

For each active crop:

1. Find the original recording frame or native source. Do not enlarge a crop
   of a crop when the original is available.
2. Reproduce the useful-region crop from that original and inspect it at the
   lesson-page display size.
3. For a bounded conceptual visual, pass the original source image(s) plus the
   clean crop or merged reference to imagegen and request a crisp,
   high-resolution sibling. Validate every required label, relationship, and
   overlay constraint.
4. For exact code, commands, URLs, plots, tables, numeric output, or live UI,
   use a deterministic replacement. A reliable baseline is a 3× Lanczos
   resize followed by mild sharpening, for example:

   ```bash
   magick source-crop.png \
     -filter Lanczos -resize 300% \
     -unsharp 0x0.5+0.5+0 \
     final-crisp.png
   ```

   This improves presentation without changing source-of-truth pixels. Never
   use imagegen to guess exact text or values.
5. Save the accepted result as `*-crisp.png`, update the Markdown reference,
   and keep the old source and `*-cropped.png` file for auditability.

The second-pass acceptance gate is stronger than “the file exists”:

- every active replaceable crop has a crisp sibling or an explicit native
  high-resolution exception;
- no active replaceable `*-cropped.png` reference remains;
- every Markdown reference resolves;
- the crisp asset is legible at normal lesson size and has no accidental face,
  camera, cursor, browser/Zoom chrome, or generation artifact;
- exact content matches the original source;
- the worktree is clean, `git diff --check` passes, and focused commits are
  pushed.

### 1. Confirm the instructional target

Read the unit text and the image caption. Write down one sentence describing
what the learner should notice. Apply the [illustration rubric](illustration-rubric.md)
first. A regeneration is justified only when the underlying image has a clear
teaching point.

### 2. Inspect the source

Load the original image before editing. Record its dimensions and list every
invariant that must survive:

- exact labels, values, and ordering;
- arrows, relationships, and direction of flow;
- the intended visual hierarchy;
- the unit and Markdown reference that consume the image.

Do not rely on the filename to infer the content. A caption and a frame can
disagree.

### 3. Crop before generation

If the useful content occupies only part of the frame, crop it first with a
deterministic tool. Remove webcam tiles, Zoom controls, browser tabs, color
calibration overlays, and black borders before preparing the clean reference.
Send the retained original source image(s) together with that reference to
imagegen. Keep the crop in `.tmp/` and record its coordinates in the pilot
report.

For example:

```bash
mkdir -p .tmp/imagegen-pilot
magick source.jpg -crop WIDTHxHEIGHT+X+Y +repage \
  .tmp/imagegen-pilot/source-crop.png
```

The crop is a preparation artifact, not a course asset.

### 4. Regenerate the crop at high resolution

Ask imagegen to regenerate the clean crop or merged reference as a clean,
crisp, high-resolution lesson illustration while also providing the retained
original source image(s). The prompt should explicitly say that the clean
reference controls composition and content, that the output must be sharp and
readable at normal lesson-page size, and that no camera tile, face, recording
controls, browser chrome, cursor, watermark, or unrelated overlay may appear.

Use imagegen's edit/generation workflow according to the available skill. Save
the generated result as a sibling candidate; never overwrite the original
source during iteration. If the result is still soft, clipped, or contains an
overlay, reject it and make one targeted prompt correction.

### 5. Prompt with explicit invariants

Use the `scientific-educational` or `infographic-diagram` imagegen use case.
Describe the intended layout, then state the exact text and values verbatim.
Repeat the non-negotiable constraints:

- preserve the listed labels, values, row order, and arrow directions;
- remove people, webcam/camera tiles, Zoom/browser chrome, cursors,
  watermarks, and unrelated overlays;
- add no labels, components, metrics, or decorative UI;
- make the result crisp and readable at normal lesson-page size.

For text-heavy or numeric images, imagegen must not be treated as a source of
truth. Compare every generated label and number against the source.

### 6. Inspect and reject aggressively

Inspect the generated output, not just the prompt or tool response. Reject it
if it:

- changes a value, label, ordering, or relationship;
- invents a metric, component, legend, or caption;
- leaves a face, camera tile, recording control, or watermark;
- makes important text less readable than the source;
- changes the visual meaning while looking more polished.

Make one targeted prompt correction at a time. In the ML pilot, the first
cross-validation generation hallucinated `ND` labels and changed the diagram;
it was rejected. The second prompt listed every required label and explicitly
forbade extra labels and numeric results, and it passed review.

### 7. Integrate non-destructively

During experimentation, save the result under a sibling filename such as
`*-imagegen-pilot.png`. After review, use a stable `*-crisp.png` filename for
the final asset and update the one Markdown reference. Keep the source and
first-pass crop until the replacement has passed visual and lesson-context
review. Update the alt text or caption so it says what the learner should
notice.

### 8. Commit by focused area

For delegated course-wide rollout, treat one accepted screenshot as one batch:
commit immediately after that screenshot passes review. The commit should
contain only the image, its Markdown reference, and its report entry; a
correction gets a new focused commit. Keep crops, prompts, and rejected
variants in `.tmp/` unless a review record is intentionally being preserved.
Run `git diff --check` and a missing-image-reference scan before every commit.
Push only when explicitly requested.

## Pilot results

The first ML Zoomcamp pilot validated the approach on three diagram types:

- one-hot encoding matrix in `02-regression`;
- K-fold cross-validation flow in `04-evaluation`;
- model deployment architecture in `05-deployment`.

All three retained their instructional relationships and removed the
webcam/recording frame. The K-fold example demonstrated the most important
debugging rule: a polished image is still invalid if generation changes a
label or invents a value.

## Acceptance checklist

- [ ] The image has a specific teaching point under the illustration rubric.
- [ ] The source was inspected and cropped before generation when necessary.
- [ ] For imagegen-eligible assets, the crop was regenerated as a crisp,
  high-resolution output rather than accepted as the final asset.
- [ ] Exact labels, values, row order, and arrows were checked against the source.
- [ ] Face, webcam, Zoom/browser chrome, cursors, and watermarks are absent.
- [ ] The output is readable at normal lesson-page size.
- [ ] The worker had the `imagegen` skill, or the task was handed off rather
  than falsely marked complete.
- [ ] The Markdown reference, filename, and caption/alt text are correct.
- [ ] The final screenshot uses a `*-crisp.png` sibling, or its native
  high-resolution exception is recorded explicitly.
- [ ] No code, URL, plot value, or configuration was entrusted to a generated approximation.
- [ ] The change has a focused commit and no disposable intermediates are staged.
