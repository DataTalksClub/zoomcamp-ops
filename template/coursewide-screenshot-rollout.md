# Course-wide screenshot rollout

Use this plan when cleaning every screenshot referenced by a course, rather
than only a small pilot set. The current ML Zoomcamp scope is every image
reference under `cohorts/2026/**` whose source is a screenshot, recording
frame, screen capture, or workshop slide. A screenshot with a useful teaching
point is still in scope even when it is not a diagram.

## Scope and inventory

Build an inventory from lesson references, not from the image directory alone:

```bash
rg -n -o 'images/[^) ]+\.(png|jpe?g|webp|gif)' cohorts/2026 --glob '*.md'
```

For each reference, record the unit, lesson, caption, source dimensions, file
type, and whether it contains a face, webcam tile, browser/Zoom chrome,
cursor, watermark, or other overlay. Also record whether the asset is an
exact-fidelity asset (code, command, URL, plot, numeric table, or live UI).

Every screenshot gets a disposition. Do not silently skip an asset because it
is inconvenient, and do not delete a useful screenshot only because its frame
is ugly.

## Two safe processing paths

### Imagegen path

Use this path when the screenshot communicates a bounded illustration,
conceptual diagram, process, architecture, or simple teaching UI whose exact
pixels are not the lesson's source of truth.

1. Read the imagegen skill if the worker has it.
2. Inspect the source with `view_image` and read the surrounding lesson text.
3. Crop the meaningful content first with a deterministic tool. Exclude
   webcam tiles, faces, browser/Zoom chrome, cursors, watermarks, and black
   borders from the reference input.
4. Prompt with exact required labels, values, order, arrows, and layout. State
   that no faces, camera tiles, controls, overlays, or extra components may
   remain.
5. Inspect the output at lesson size and reject any changed label, value,
   relationship, or teaching meaning. Make one targeted correction at a time.

### Deterministic path

Use this path when exact fidelity matters: source code, shell commands, URLs,
configuration, plots, numeric tables, evaluation results, or a live UI whose
controls/labels are the lesson. Crop away the recording frame, then prefer the
original source, a notebook/code re-render, a native export, or a deterministic
high-quality raster conversion. Do not use imagegen to guess exact text or
numbers. If the unwanted face or overlay is inside the exact content and
cannot be removed safely, record the blocker and hand it to the parent agent
instead of painting over it.

The two paths together cover all screenshots: every asset is inspected and
given a disposition, but generation is not forced where it can corrupt the
lesson.

## Worker batching and ownership

Partition by disjoint lesson directories. A worker owns its source files,
generated siblings, report, and Markdown references for that batch. It must not
edit another worker's files, rewrite shared navigation, or push. Keep batches
small enough to review (one lesson or a related group of up to five assets),
and make one focused commit per accepted batch.

Workers with the `imagegen` skill may execute the imagegen path. Workers
without it must follow the deterministic path or prepare an evidence report for
a capable worker; they must not claim to have generated an image. The parent
agent performs the final visual review, updates any shared index, runs broken
reference checks, and pushes only after the batch is accepted.

## Naming and review records

During review, keep the original source and use a sibling name such as
`*-imagegen-pilot.png` or `*-cropped.png`. Store crop coordinates, disposition,
prompt iterations, invariants checked, and rejection reasons in a short report
under `.tmp/`. Do not stage disposable crops or rejected generations.

Before accepting a batch, verify:

- every source in the batch was inspected and has a disposition;
- all face/camera/recording/browser overlays are gone when they are not part
  of the teaching point;
- exact text, values, code, URLs, axes, and relationships are unchanged on
  the deterministic path;
- generated labels and relationships pass visual review on the imagegen path;
- every Markdown reference resolves and `git diff --check` passes;
- the commit contains only the batch's assets, report, and references.

## Rollout order

Process modules in dependency order so the visual conventions stabilize early:

1. `01-intro` through `04-evaluation`;
2. `05-deployment` through `06-trees`;
3. `08-deep-learning`;
4. `09-serverless` and `10-kubernetes`.

After each module group, review a contact sheet and record exceptions before
starting the next group. A clean commit is a checkpoint; do not squash away a
rejected-generation correction because the history explains why the final
asset was accepted.
