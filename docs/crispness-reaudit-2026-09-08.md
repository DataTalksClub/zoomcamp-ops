# Screenshot crispness re-audit — 2026-09-08

The earlier visual-review report is reopened. Its `PASS` entries confirmed
reference resolution and visual intent, but several assets described as
“deterministic crop/sharpen” are still visibly soft at normal lesson size.
That evidence is not sufficient for a crispness acceptance.

## Corrected acceptance rule

For every screenshot-derived lesson asset:

- a `*-crisp.png` filename, larger dimensions, sharpening, or interpolation is
  not evidence of regeneration;
- retain the original non-crisp source unchanged;
- if the asset was already regenerated with imagegen and passes a direct visual
  check, leave it in place;
- otherwise crop only to isolate the teaching region, send the original source
  and the crop/reference to imagegen, inspect the result at lesson size and
  100%, and replace the published asset only after checking labels, values,
  relationships, overlays, and camera removal;
- if the content is only a table, comparison matrix, or exact-value list,
  convert it to native Markdown/HTML instead of generating a screenshot.

## Open repair queue

This is a queue, not a completion claim.

| Repository | Scope | Initial status | Required action |
| --- | --- | --- | --- |
| `data-engineering-zoomcamp` | `cohorts/2027/03-data-warehouse` screenshot-derived `*-crisp.png` assets | reopened; prior crop/sharpen PASS invalid | regenerate with imagegen, except assets proven to have already used imagegen; remove/native-render table/list content |
| `data-engineering-zoomcamp` | `cohorts/2027/06-batch` screenshot-derived `*-crisp.png` assets | reopened; prior crop/sharpen PASS invalid | regenerate with imagegen, preserving exact code/UI invariants or replace with a deterministic source rendering when imagegen cannot preserve them |
| `machine-learning-zoomcamp` | `cohorts/2026/02-regression/06-linear-regression-vector-04-fake-feature-crisp.png` | user-reported soft | inspect original and regenerate; do not trust the filename |
| `machine-learning-zoomcamp` | `cohorts/2026/02-regression/06-linear-regression-vector-05-prepend-one-crisp.png` | user-reported soft | inspect original and regenerate; do not trust the filename |

The linked external-table screenshot was regenerated with imagegen in DE commit
`cc8ee1f`. The BigQuery-cost slide was removed in DE commit `c9295b4` because
the lesson already expresses the exact values as native text and the screenshot
added no information beyond that text.

## Corrections already pushed

These commits are real corrections, not evidence that the remaining queue is
complete:

- DE `86b8bf0`: replaced the OLTP/OLAP comparison screenshot with a native
  Markdown table.
- DE `ba549cb`: removed eight redundant partitioning/clustering and best-
  practices list slides; the lesson text already carries their content.
- DE `5fb5839`: removed seven redundant BigQuery ML output/table screenshots.
- DE `bb57249`: regenerated the BigQuery ML model-choice diagram with imagegen
  from the retained original and crop; the generated result was inspected at
  full resolution.
- DE `eb0bc99` and `e043b33`: regenerated the partitioning, clustering, and
  pruning visuals from original sources plus crops; these still require the
  committed provenance/reviewer ledger below before they can be called fully
  accepted.
- DE `0904e57`, `fae367c`, and `d58916e`: regenerated four Spark notebook/UI
  screenshots from their original JPGs plus crops. The redundant group-by
  query screenshot was removed in `379f6cc` because the lesson already shows
  the SQL natively. These assets remain pending independent visual review;
  the commits do not establish a repository-wide crispness PASS.
- DE `aa152cf` and `f66a710`: regenerated the sort-merge and broadcast-join
  UI visuals from their original JPGs plus crops. They are pending the same
  independent visual review gate.
- ML `095d0dc`: regenerated the two user-flagged regression-vector visuals from
  their original sources plus crops.

The active DE warehouse scope is now 16 illustration references after the
native-content removals. The active DE batch scope still contains many
`*-crisp.png` screenshot derivatives and is not complete. The ML repository
also contains a much larger active illustration set; no repository-wide ML
crispness PASS is being claimed until its complete inventory is reviewed.

## Inventory results from the independent audits

The implementation queue is now evidence-based rather than inferred from
filenames:

- ML 2026: 578 active local image references; 368 native-content removals or
  conversions, 110 already-supported imagegen reconstructions, 91
  screenshot-derived assets requiring regeneration, and 12 deterministic or
  external exceptions. One combined TensorFlow Lite asset needs its two
  component originals as the regeneration input.
- DE 2027 batch: 74 active references; 17 source-backed imagegen assets, 57
  crop/upscale/re-export screenshot derivatives, and 3 imagegen list slides
  that were removed because nearby prose already contains the same content.
- DE 2027 streaming: 0 active illustration references. The unsupported
  generated streaming set was removed; no replacement should be invented.
- DE 2027 warehouse: 16 active references after table/list cleanup; the six
  deployment screenshots were regenerated from their original JPGs plus crops
  in commits `73b1eff` and `7bc4aed`.

These counts are queues and classifications, not completion claims. The
repository-specific audit agents found no broken active references in these
scopes.

## Provenance required for each completion

Record the source path, original dimensions, crop coordinates, imagegen input
paths, generated output path, prompt constraints, and independent visual verdict
before moving an item out of this queue. A reviewer must inspect the actual
asset; metadata, pixel dimensions, and filenames are not enough.
