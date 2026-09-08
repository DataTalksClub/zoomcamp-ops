# Screenshot crispness re-audit — 2026-09-08

The earlier visual-review report is reopened. Its `PASS` entries confirmed
reference resolution and visual intent, but several assets described as
“deterministic crop/sharpen” are still visibly soft at normal lesson size.
That evidence is not sufficient for a crispness acceptance.

The live scanner was rerun after the cleanup commits at ML `85f83bb` and DE
`4bf778d`. It found **493 active image-reference occurrences** across the four
repositories; **345 still require direct visual review**. The old report's
repository-wide `PASS` claims are withdrawn. A filename, pixel dimension, or
worker implementation report is not an acceptance result.

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
| `machine-learning-zoomcamp` | current cohorts 2026/01–10 | implementation is partly regenerated, but the live audit still has 345 visual reviews required across all four repos | independently inspect every active screenshot-derived target; regenerate from the original plus a bounded crop, or replace exact code/table/output with native content |
| `llm-zoomcamp` | current cohort | 38 local active refs; no crispness acceptance | independently inspect every retained image and remove or regenerate unsupported/soft screenshots |
| `mlops-zoomcamp` | current lesson set | 38 refs, including one remote; no crispness acceptance | independently inspect every retained image and repair exact UI/code assets without guessing |

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
  the SQL natively. An independent reviewer accepted all four regenerated
  targets; the commits still do not establish a repository-wide crispness
  PASS.
- DE `aa152cf` and `f66a710`: regenerated the sort-merge and broadcast-join
  UI visuals from their original JPGs plus crops. The first sort-merge output
  was corrected in `64d18b2` to restore `WholeStageCodegen (5)`; both final
  targets were initially reviewed, but the broadcast target later failed a
  direct text check because imagegen rendered the leading `$` in
  `$anonfun$withThreadLocalCaptured$1` as `S`. DE `eeb478e` and `bdacd32`
  corrected that label deterministically; the target is pending fresh
  independent review.
- DE `0806220`, `e8e2868`, `16b4254`, and `d2432e1`: regenerated the worker
  status, GCS upload completion, Dataproc submit form, and Dataproc report
  folder visuals from original JPGs plus crops. The worker UI, submit form,
  and report-folder outputs were independently accepted; the GCS screenshot
  was rejected for text drift and replaced natively in `4bf778d`.
- DE `63927e9` and `aff59ee`: regenerated the RDD DAG and mapPartitions feature
  output from original JPGs plus crops; an independent reviewer accepted both.
- DE `c3e895c` was rejected after the reviewer found changed path years,
  prefixes, and a missing `.crc` line despite the output being sharp. DE
  `4bf778d` replaced that deterministic terminal transcript with a native
  output block containing the exact source values.
- DE `bfb7bc9`, `4bd583f`, `2526fa4`, `a769f39`, `b3ac8b5`, `c0abf49`, and
  `c3b003f`, and `72c2419`: removed code-only, table-only, duplicate, or exact-value
  screenshots where the lesson already contains the information as native
  code, prose, or Markdown tables.
- ML `095d0dc`: regenerated the two user-flagged regression-vector visuals from
  their original sources plus crops.
- ML `0c46398`, `0bb2678`, `4984fd4`, and `85f83bb`: regenerated the retained
  intro and regression visuals with imagegen from original JPGs plus crops and
  removed redundant references. The two user-fixed vector assets remain
  excluded from those worker commits because they were already handled in
  `095d0dc` and `b72735e`.
- ML `93b6448`, `961e365`, `3623daa`, `a34123c`, `915a377`, `1d4e1df`,
  `eec4bc3`, `712c684`, `26246f3`, `84b96f8`, `0740877`, and `9b479a4`:
  regenerated classification/evaluation visuals, removed redundant screenshot
  references, and removed unreferenced crop intermediates.
- ML `05b5cb8` and `39016f2`: regenerated deployment and tree visuals. Worker
  audits reported all owned assets passing and all references resolving.
- ML `10bae47`, `212beaa`, `7e6620c`, `bc52fcb`, and `31049ba`: added a small
  batch of imagegen replacements for ImageNet, checkpointing, k-fold, serverless,
  and SavedModel screenshots. These are implementation commits only; the
  independent review queue remains open, and the serverless preprocessing image
  still needs an aspect-ratio check.

The active DE warehouse scope is now 16 illustration references after the
native-content removals. The active DE batch scope currently contains 51
illustration references and is still open for asset-by-asset acceptance. The
ML implementation workers reported 160 active references in their owned
01–06 slices, but the current live scanner covers 353 ML refs across cohorts
01–10 and still marks 345 references across all scopes for visual review. The
partial independent reviews also found a live green Jupyter selection border
in `06-linear-regression-vector-05-prepend-one-crisp.png`; the regression
vector pair is therefore not accepted yet. No repository-wide ML crispness
PASS is claimed here.

## Inventory results from the independent audits

The implementation queue is now evidence-based rather than inferred from
filenames:

- ML 2026: the earlier 578-reference classification was a pre-cleanup queue
  and is superseded for the current cohorts. The live scanner now reports 353
  ML refs, 350 local and three remote/non-local references, with 15 units
  lacking an active illustration. Earlier worker reports cover only their
  implementation slices and are not independent acceptance. The visual queue
  remains open until every active target is checked at native resolution and
  lesson display size.
- DE 2027 batch: the earlier audit found 74 active references. After the
  native-content cleanup and duplicate removal commits above, the current
  active reference count is 51. The remaining assets are still an open
  asset-by-asset queue; regenerated files are not a repository-wide PASS until
  their direct and independent checks are recorded.
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
