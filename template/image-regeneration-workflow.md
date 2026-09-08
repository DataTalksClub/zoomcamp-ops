# Image regeneration workflow

Use this workflow when a useful Zoomcamp illustration is a blurry workshop
frame, includes a presenter or camera tile, or is difficult to read at the
size used on the lesson page.

The goal is to preserve the teaching content while producing a clean,
readable illustration. Do not regenerate an image simply because it is old or
visually imperfect.

## Choose the right tool

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
3. Crop away webcam tiles, faces, browser/Zoom chrome, cursors, and overlays
   with a deterministic tool before generation.
4. Use the built-in imagegen workflow with explicit labels, values, layout,
   and negative constraints.
5. Inspect the generated image and reject it when any instructional invariant
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

## Workflow

## The crisp-regeneration pattern

The standard imagegen workflow is deliberately two-stage:

```text
original recording frame
        │
        ▼
deterministic crop of the useful region
        │
        ▼
imagegen regeneration from that crop
        │
        ▼
high-resolution, crisp, camera-free lesson asset
```

Cropping and regeneration solve different problems. The crop removes the
webcam tile, face, browser/Zoom chrome, black borders, and unrelated panels so
the model receives only the teaching content. Imagegen then rebuilds that
bounded content as a clean, high-resolution raster with sharper edges and
readable labels. Do not send the full recording frame to imagegen when a crop
can isolate the lesson content first.

The crop is a reference input, not the final deliverable. A cropped screenshot
that is still soft, pixelated, or difficult to read should not be accepted
just because the distracting frame is gone. Regenerate it from the crop with
an explicit request for crisp, high-resolution output and inspect the result
at the size used on the lesson page.

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
   illustration, send the crop to imagegen and ask it to regenerate a crisp,
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
3. For a bounded conceptual visual, send that crop to imagegen and request a
   crisp, high-resolution sibling. Validate every required label, relationship,
   and overlay constraint.
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
calibration overlays, and black borders before sending the crop to imagegen.
Keep the crop in `.tmp/` and record its coordinates in the pilot report.

For example:

```bash
mkdir -p .tmp/imagegen-pilot
magick source.jpg -crop WIDTHxHEIGHT+X+Y +repage \
  .tmp/imagegen-pilot/source-crop.png
```

The crop is a preparation artifact, not a course asset.

### 4. Regenerate the crop at high resolution

Ask imagegen to regenerate the cropped reference as a clean, crisp,
high-resolution lesson illustration. The prompt should explicitly say that the
crop is the reference for composition and content, that the output must be
sharp and readable at normal lesson-page size, and that no camera tile, face,
recording controls, browser chrome, cursor, watermark, or unrelated overlay
may appear.

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
