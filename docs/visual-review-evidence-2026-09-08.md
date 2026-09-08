# Visual review evidence — 2026-09-08

This is the human/agent visual-review companion to
[`current-illustration-audit.md`](current-illustration-audit.md). The scanner
proves scope, reference resolution, and basic decodability; the reviews below
opened the retained images at native resolution and at lesson display size.

> **Reopened:** on 2026-09-08 the user identified multiple retained
> screenshot-derived assets that are still soft. The prior `PASS` rows below
> must not be read as a crispness approval. See the
> [crispness re-audit](crispness-reaudit-2026-09-08.md); screenshot-derived
> assets are being regenerated or removed/native-rendered and will receive a
> fresh independent review.

## Decision framework

Choose the output style from the teaching point:

- Keep or crop-and-crispify a screenshot when the screenshot is the evidence:
  an exact UI state, notebook output, plot, table, code result, command result,
  or configuration state.
- Use a clean imagegen redraw when the lesson teaches a conceptual relationship
  or process and exact pixels are not the source of truth.
- Use deterministic rendering for exact code, numbers, plots, tables, URLs, and
  UI. Imagegen must not guess source-of-truth text or values.
- Remove an image when it is unsupported, redundant, invented, or cannot be
  made readable without changing its meaning.

For every regeneration, the original non-crisp source is retained unchanged.
When useful, a deterministic crop isolates the teaching region; when adjacent
screenshots form one surface, the crop/merge order is determined from the
content and recorded. Imagegen receives the original source image(s) and the
merged/cropped reference—not only a resized or sharpened derivative.

## Previous audit status — withdrawn

| Scope | Repository head | Retained active references reviewed | Result | Units without illustrations |
| --- | --- | ---: | --- | ---: |
| ML 2026 | `ff3733f` | 317 current active refs | **OPEN**; 307 ML reviews remain in the live queue | 19/105 currently missing active refs |
| LLM 2026 | `c557a0a` | 38 current local refs | **OPEN**; no crispness acceptance | 36/72 |
| MLOps current lesson set | `42a1b0d` | 38 current-scope refs | **OPEN**; no crispness acceptance | 2/7 |
| DE 2027 draft | `bdacd32` | 61 current refs | **OPEN**; no repository-wide acceptance | 69/88 |

“Units without illustrations” is intentionally not hidden: those units lost
unsupported or invented visuals during the distrust audit. They should receive
a source-backed illustration only when one can be found; do not fill the gap
with made-up content merely to reach 100% coverage. The table above is a
current queue, not evidence that the remaining images are crisp.

## Per-image lists and evidence

The generated [`current-illustration-audit.md`](current-illustration-audit.md)
contains the complete active-unit list and every active image-reference
occurrence. The full distrust reports preserve the per-occurrence decisions for
the largest audits:

- [ML full audit TSV](audits/ml-2026-full-distrust-audit.tsv) and
  [ML summary](audits/ml-2026-full-distrust-audit-summary.md)
- [DE full audit](audits/de-2027-full-distrust-audit.md)

The LLM reviewer inspected all 38 retained local references individually. The
MLOps reviewer inspected the current lesson visuals, exact AWS screenshots,
shared diagrams, and the official badge; the implementation pass also removed
historical thumbnail embeds and stale broken references.

The Astra style review found three semantic defects and no broad style
outliers. They were corrected and independently reviewed:

- ML correlation strength cards: `bfafbbb` corrected the LOW/STRONG spatial
  ordering.
- LLM agent flow: `c557a0a` restored `Olama` (failed search) versus `Ollama`
  (corrected retry).
- DE Spark reshuffling: `21b6693` removed the extra route so the three
  `(h₁,z₁)` records go only to P1 and the two `(h₁,z₂)` records only to P2.

## Review gates

An image is accepted only when the reviewer confirms all of the following:

1. The image contributes a specific teaching point and its caption/alt text
   matches.
2. The source-side crop/merge direction and reading order are correct.
3. Text, values, arrows, relationships, and UI state are faithful to the
   source.
4. The image is readable at lesson size and does not show interpolation blur,
   browser/Zoom chrome, faces, cameras, cursors, or unrelated overlays.
5. The Markdown reference resolves and the corresponding unit/reference is in
   the committed audit list.

The implementation agent cannot self-approve a generated replacement; an
independent reviewer must record the result.

## Fresh independent review batch

The following decisions were made after opening the published pixels at native
resolution and lesson display size. They are asset-level decisions only; they
do not imply a repository-wide PASS.

| Repository target | Decision | Evidence |
| --- | --- | --- |
| ML `08-deep-learning/...03-pretrained-models-01-keras-applications-crisp.png` | ACCEPT | Sharp redraw; visible heading, prose, table headings, and values match; no chrome, cursor, or selection artifacts |
| ML `08-deep-learning/...03-pretrained-models-02-imagenet-crisp.png` from `10bae47` | NEEDS-CORRECTION | Text/statistics were sharp, but the logo and `Download` heading were clipped, explanatory lines were cut, and a green browser strip remained; replaced in `4e56d95`, pending fresh review |
| ML `08-deep-learning/...11-large-model-05-training-output-crisp.png` | ACCEPT | Epochs 15–21 and visible loss/accuracy values match; clean terminal redraw with no notebook/camera chrome |
| ML `08-deep-learning/...07-checkpointing-01-oscillation-crisp.png` | ACCEPT | Graph-only crop is readable; legend, axes, curves, epoch-8 annotation, and relationships match |
| ML `02-regression/...06-linear-regression-vector-04-fake-feature-crisp.png` | ACCEPT | Symbols, subscripts, `n+1 dim`, equality, and blue annotation match; no camera/borders |
| ML `02-regression/...06-linear-regression-vector-05-prepend-one-crisp.png` | ACCEPT | Code and `[7.17, 0.01, 0.04, 0.002]` match; no browser/camera/cursor/selection artifacts |
| ML `04-evaluation/...07-cross-validation-01-kfold-diagram-pilot.png` | UNRESOLVED | Redraw is clear and semantically matching, but no separate bounded crop exists for provenance/aspect verification |
| ML `09-serverless/...01-intro-04-module-plan-crisp.png` | ACCEPT | Lines, wording, colors, and numbering match; editor/cursor/selection artifacts removed |
| ML `09-serverless/...01-intro-05-module-plan-lambda-gateway-crisp.png` | ACCEPT | Headings/items match; clean crop without editor chrome or clipping |
| ML `09-serverless/...03-tensorflow-lite-06-keras-preprocess-source-crisp.png` | ACCEPT | Code, line numbers, `127.5`, `1.`, and mean/std arrays match; selection/browser artifacts removed |
| ML `10-kubernetes/...02-tensorflow-serving-01-saved-model-crisp.png` | ACCEPT | Terminal output/tree and `saved_model.pb`/variables details match; no GitHub/camera/selection artifacts |

## Follow-up review: corrected and newly published assets

| Repository target | Decision | Evidence |
| --- | --- | --- |
| ML `08-deep-learning/...03-pretrained-models-02-imagenet-crisp.png` from `4e56d95` | ACCEPT | Complete logo, heading, statistics, and terms box; no clipped margins or browser/camera/cursor artifacts |
| ML `08-deep-learning/...03-pretrained-models-03-sagemaker-gpu-crisp.png` from `ca6dd36` | ACCEPT | Complete centered settings card; exact `ml.p2.xlarge`, ARN, status, platform, volume, and timestamp; no sidebar/browser/camera/handwriting |
| ML `08-deep-learning/...03-pretrained-models-04-xception-model-crisp.png` | ACCEPT | Complete code/UUID/299×299 context and links; sharp and unclipped |
| ML `08-deep-learning/...03-pretrained-models-05-xception-weights-download-crisp.png` | ACCEPT | Exact download URL/progress and follow-up cells; sharp and unclipped |
| ML `08-deep-learning/...03-pretrained-models-06-batch-shape-crisp.png` | ACCEPT | Exact `(1, 299, 299, 3)` output and surrounding context; sharp and unclipped |
| ML `08-deep-learning/...03-pretrained-models-07-preprocess-input-crisp.png` | ACCEPT | Exact preprocessing output and annotation context; no notebook chrome artifacts |
| ML `08-deep-learning/...03-pretrained-models-08-decode-predictions-crisp.png` | ACCEPT | Exact ImageNet labels/values and clean notebook redraw; no unrelated UI |
| ML `08-deep-learning/...08-more-layers-02-activation-functions-crisp.png` | ACCEPT | ReLU/convergence plots preserve axes, values, curves, and useful lesson context |
| ML `08-deep-learning/...08-more-layers-06-val-accuracy-plot-crisp.png` | ACCEPT | Three series, legend, ticks, and relative performance match; clean and unclipped |
| ML `08-deep-learning/...09-dropout-06-val-accuracy-dropout-imagegen.png` | NEEDS-CORRECTION | An unlabeled fifth blue trajectory was introduced from a handwritten highlight; regeneration is required |
| ML `08-deep-learning/...09-dropout-07-dropout-02-vs-train-imagegen.png` | ACCEPT | Clean curve with matching oscillation and caption context |
| ML `08-deep-learning/...09-dropout-08-no-regularization-overfit-imagegen.png` | NEEDS-CORRECTION | A handwritten `100%` guide became an extra high curve; regeneration is required |
| ML `04-evaluation/...06-auc-05-auc-interpretation-imagegen-v2.png` | ACCEPT | Correct score sets/class assignments and selected pair; no extra score or overlays |

## Dropout follow-up review

The follow-up reviewer accepted the regenerated dropout assets at native and
lesson size. The reviewer also found a lesson-code mismatch for the
train/validation image; commit `521d8d2` corrected the code before acceptance.

| Repository target | Decision | Evidence |
| --- | --- | --- |
| ML `08-deep-learning/...09-dropout-03-frozen-neuron-imagegen-v2.png` | ACCEPT | One crossed-out inner-layer neuron, de-emphasized connections, and `NOT UPDATED DURING TRAINING`; no camera/recording overlay |
| ML `08-deep-learning/...09-dropout-06-val-accuracy-dropout-imagegen.png` | ACCEPT | Exactly four legend-matched validation curves; y-axis `0.78–0.86`; no extra training curve or handwritten guide |
| ML `08-deep-learning/...09-dropout-08-no-regularization-overfit-imagegen.png` | ACCEPT after `521d8d2` | Image has exactly train/validation curves, and the lesson now plots `hist['val_accuracy']` plus `hist['accuracy']` for `scores[0.0]` |

## Independent MLOps review

Feynman independently inspected all 38 active README references at native
resolution and at a max-1000px lesson render. This is an asset-level result,
not a repository-wide crispness approval. The 11 additional AWS walkthrough
screenshots in `mlflow_on_aws.md` were also checked separately.

| Scope | Accepted | Needs correction | Removed/unresolved | Repair |
| --- | ---: | ---: | ---: | --- |
| MLOps active README refs | 37 | 1 | 0 | Regenerate `06-best-practices/AWS-stream-pipeline-redrawn.png` with complete horizontal margins; preserve labels and relationships |
| MLOps additional AWS screenshots | 11 | 0 | 0 | Exact UI screenshots were accepted as source evidence; they are not imagegen illustrations |

The reviewer found OpenAI Media Service C2PA/JUMD metadata on the 34 generated
or redrawn PNGs and rejected no active image as a mere upscale. The one repair
is intentionally kept open until a fresh independent check confirms the new
image at native and lesson size.

## Independent LLM review

Avicenna independently inspected all 38 active LLM references at native
resolution and at a 608px desktop lesson render. Dimensions were not used as
a crispness proxy.

| Scope | Accepted | Needs correction | Remove | Unresolved | Repair |
| --- | ---: | ---: | ---: | ---: | --- |
| LLM active refs | 28 | 9 | 1 | 0 | Repair the nine relationship errors and remove the unsupported partial evaluation intro visual |

The nine repair targets are: Agentic RAG refs `01-intro-01`, `03-rag-08`, and
`16-other-frameworks`; evaluation refs `01-intro-01`, `11-evaluation-intro-01`,
and `14-agent-evaluation-01`; and project refs `02-evaluating-retrieval-01`,
`03-evaluating-rag-01`, and `07-chunking-01`. The removed target is
`04-evaluation/01-intro-02-interact-or-generate-imagegen.png`. A focused repair
worker is handling the first Agentic RAG batch and the removal; no LLM
repository-wide approval is claimed.

## Independent ML regression review

Pauli independently inspected all 22 active references in
`cohorts/2026/02-regression` at native resolution and simulated lesson size.
The result exposed the exact evidence gap behind the earlier overclaim:

| Scope | Accepted | Needs correction | Remove/native | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| ML regression active refs | 4 | 0 confirmed visually | 0 | 18 |

The four accepted assets are the three conceptual imagegen illustrations and
`06-linear-regression-vector-04-fake-feature-crisp.png`, whose source, bounded
crop, imagegen output ID, and target are recorded. The other 18 are visually
legible but remain unaccepted because no durable record proves that the
original non-crisp source and bounded crop were supplied to imagegen. A focused
worker is reprocessing the first ten; the remaining eight stay open. This is
not a crispness or repository-wide completion claim.

### MLOps repair follow-up

`d47085f` regenerated `06-best-practices/AWS-stream-pipeline-redrawn.png`
from the original reference and current target. Epicurus independently checked
the original, the new native output, and a 1000×650 lesson-size render:

| Target | Decision | Evidence |
| --- | --- | --- |
| MLOps `06-best-practices/AWS-stream-pipeline-redrawn.png` | ACCEPT | Labels and relationships preserved; both connectors have approximately 90–100px interior margins; no camera/browser/editor/selection artifacts; crisp and legible at lesson size |

The MLOps repair queue from the first review is therefore closed. This remains
an asset-level acceptance, not a claim that other course scopes are complete.
