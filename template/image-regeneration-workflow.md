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

### 4. Prompt with explicit invariants

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

### 5. Inspect and reject aggressively

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

### 6. Integrate non-destructively

During experimentation, save the result under a sibling filename such as
`*-imagegen-pilot.png` and update the one Markdown reference. Keep the source
until the replacement has passed visual and lesson-context review. Use a
stable descriptive filename for the final asset, and update its alt text or
caption so it says what the learner should notice.

### 7. Commit by focused area

Each accepted batch should have a focused commit scoped to one course module
or one clearly related lesson group. Include the image and its Markdown
reference, and keep crops, prompts, and rejected variants in `.tmp/` unless a
review record is intentionally being preserved. Run `git diff --check` and a
missing-image-reference scan before committing. Push only when explicitly
requested.

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
- [ ] Exact labels, values, row order, and arrows were checked against the source.
- [ ] Face, webcam, Zoom/browser chrome, cursors, and watermarks are absent.
- [ ] The output is readable at normal lesson-page size.
- [ ] The worker had the `imagegen` skill, or the task was handed off rather
  than falsely marked complete.
- [ ] The Markdown reference, filename, and caption/alt text are correct.
- [ ] No code, URL, plot value, or configuration was entrusted to a generated approximation.
- [ ] The change has a focused commit and no disposable intermediates are staged.
