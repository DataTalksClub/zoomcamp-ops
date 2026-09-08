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

## Provenance required for each completion

Record the source path, original dimensions, crop coordinates, imagegen input
paths, generated output path, prompt constraints, and independent visual verdict
before moving an item out of this queue. A reviewer must inspect the actual
asset; metadata, pixel dimensions, and filenames are not enough.
