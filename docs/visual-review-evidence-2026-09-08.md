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

> **Current correction (2026-09-09):** The user rechecked published outputs
> and found that several images described as crisp are still merely enlarged,
> softened, or otherwise not publication-ready. Treat every acceptance claim
> below as historical evidence about the specific bytes and review scope at
> that time, not as a current repository-wide crispness guarantee. The live
> status is **audit required** until a fresh reviewer opens the current
> published pixel, its original non-crisp source, and the lesson-size render.
> A filename, dimensions, interpolation, or prior agent PASS cannot close
> that gate.

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
was subsequently completed and independently accepted in the MLOps repair
follow-up below.

## Independent LLM review

Avicenna independently inspected all 38 active LLM references at native
resolution and at a 608px desktop lesson render. Dimensions were not used as
a crispness proxy.

| Scope | Accepted | Needs correction | Remove | Unresolved | Repair |
| --- | ---: | ---: | ---: | ---: | --- |
| LLM active refs | 28 | 9 | 1 | 0 | Repair the nine relationship errors and remove the unsupported partial evaluation intro visual |

The nine repair targets were: Agentic RAG refs `01-intro-01`, `03-rag-08`, and
`16-other-frameworks`; evaluation refs `01-intro-01`, `11-evaluation-intro-01`,
and `14-agent-evaluation-01`; and project refs `02-evaluating-retrieval-01`,
`03-evaluating-rag-01`, and `07-chunking-01`. The removed target is
`04-evaluation/01-intro-02-interact-or-generate-imagegen.png`. The follow-up
sections below record the accepted repair batches; this initial table is kept
as the pre-repair baseline, not as a current completion claim.

## Independent ML regression review

Pauli independently inspected all 22 active references in
`cohorts/2026/02-regression` at native resolution and simulated lesson size.
The result exposed the exact evidence gap behind the earlier overclaim:

| Scope | Accepted | Needs correction | Remove/native | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| ML regression active refs | 4 | 0 confirmed visually | 0 | 18 |

The four accepted assets were the three conceptual imagegen illustrations and
`06-linear-regression-vector-04-fake-feature-crisp.png`, whose source, bounded
crop, imagegen output ID, and target are recorded. The other 18 are visually
legible but remain unaccepted because no durable record proves that the
original non-crisp source and bounded crop were supplied to imagegen. The two
follow-up batches below reprocessed and independently accepted those 18
assets. This is not a repository-wide completion claim.

## ML regression repair follow-up

`b97d2ea` regenerated the remaining eight unresolved screenshot-derived
references in the 2026 regression module from their original JPGs plus
bounded crops. Averroes independently checked every target at native and
608px lesson size.

| Batch | Accepted | Needs correction | Unresolved |
| --- | ---: | ---: | ---: |
| ML regression `b97d2ea` | 8 | 0 | 0 |

The reviewer confirmed exact formulas, values, axes, split relationships, and
removal of webcam/browser/cursor artifacts. Each target contains C2PA
`gpt-image`/OpenAI Media Service provenance and differs materially from its
original JPG; this batch is accepted at asset level.

## ML intro repair follow-up

`70c642f` regenerated four ML intro targets from original JPGs plus bounded
crops. Erdos independently checked them at native and 608px lesson size.

| Target group | Accepted | Needs correction |
| --- | ---: | ---: |
| Multiclass diagram and two linear-algebra diagrams | 3 | 0 |
| Multiple-comparisons diagram | 0 | 1 |

The multiple-comparisons output is crisp and complete but uses the wrong
currency labels for the lesson; a focused semantic repair is open. The other
three are accepted with C2PA/OpenAI Media Service provenance and no clipping,
scribbles, camera, browser, or cursor artifacts.

## ML intro currency repair

`2da77a8` regenerated the multiple-comparisons image from the original JPG and
bounded crop. Einstein independently checked the published image at native
1617×973 and 608px lesson size.

| Target | Decision | Evidence |
| --- | --- | --- |
| `01-intro/05-model-selection-02-multiple-comparisons-imagegen-pilot.png` | ACCEPT | Exact `EURO`, `US DOLLAR`, `ZLOTY`, `RUBLE`, and `HRYVNIA` labels; five emails/coins, title, and `20%`; no browser/camera/cursor/scribble/clipping artifacts; C2PA/JUMD provenance matches recorded output |

## Independent DE warehouse and batch review

Aristotle independently inspected all 58 currently active references in
`cohorts/2027/03-data-warehouse` and `cohorts/2027/06-batch` at native
resolution and simulated 800px lesson width. This is an asset-level result;
the repair queue remains open.

| Scope | Accepted | Needs correction | Remove/native | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| DE data warehouse | 13 | 3 | 0 | 0 |
| DE batch | 40 | 2 | 0 | 0 |
| Total | 53 | 5 | 0 | 0 |

Open repairs: remove the selection overlays from warehouse partition-pruning
and cluster-pruning targets; tighten the warehouse Docker `docker ps` crop;
remove the Spark built-in-functions active-cell border while preserving the
autocomplete list; and restore the clipped Stage 30 → Stage 31 DAG connector.
A focused worker is handling these five targets. No DE repository-wide pass is
claimed.

## LLM Agentic RAG repair follow-up

`da89a5f` regenerated the first three LLM repair targets and removed the
unsupported evaluation-intro image reference. Volta independently inspected
the three new PNGs at native and 608px lesson size.

| Target | Decision | Evidence |
| --- | --- | --- |
| `01-agentic-rag/01-intro-01-rag-project-overview-imagegen.png` | ACCEPT | Correct question → search over FAQ corpus → retrieved context → LLM → answer flow; C2PA `gpt-image` metadata; no clipping or overlays |
| `01-agentic-rag/03-rag-08-rag-architecture-sketch-imagegen.png` | ACCEPT | Complete assistant/question → search → knowledge base → retrieved data → prompt → LLM → answer flow; clean redraw of the Zoom/webcam source |
| `01-agentic-rag/16-other-frameworks-01-shared-agent-loop-imagegen.png` | ACCEPT | SDK A/B/C each share the complete messages → tool call → observe → answer loop; crisp at both sizes |

The old unsupported asset remains unreferenced. The other six LLM repair
targets were handled in `8606daf` below; the two follow-ups together cover all
nine repair targets from the initial audit.

## LLM evaluation/project repair follow-up

`8606daf` regenerated the remaining six LLM repair targets. Sartre
independently inspected all six at native and 608px lesson size.

| Batch | Accepted | Needs correction | Unresolved |
| --- | ---: | ---: | ---: |
| LLM evaluation/project repairs `8606daf` | 6 | 0 | 0 |

The reviewer confirmed exact relationships and labels, matching provenance
hashes, C2PA/OpenAI Media Service `gpt-image` metadata, no overlays/clipping,
and material pixel differences from the pre-repair images. Five conceptual
assets honestly document their prior semantic PNGs and bounded references
without claiming nonexistent JPG sources. All LLM repair targets are now
independently accepted; the remaining LLM active refs still retain their
original 28/38 review result.

## Independent ML intro review

Meitner independently inspected all 32 active local references in
`cohorts/2026/01-intro` at native resolution and display size using the rubric.

| Scope | Accepted | Needs correction | Remove/native | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| ML intro active refs | 20 | 6 | 6 | 2 |

The initial repair queue included the multiclass diagram, multiple-comparisons
diagram, two linear-algebra diagrams, six environment visuals (including two
with profile faces and one exposed tokenized Jupyter URL), and two exact
list/code visuals that should become native lesson content. The first four
imagegen targets and the currency-label repair are independently accepted in
the follow-ups above; environment and native-content repairs remain open. This
is a bounded-scope result, not a full ML approval.

## MLOps repair follow-up

`d47085f` regenerated `06-best-practices/AWS-stream-pipeline-redrawn.png`
from the original reference and current target. Epicurus independently checked
the original, the new native output, and a 1000×650 lesson-size render:

| Target | Decision | Evidence |
| --- | --- | --- |
| MLOps `06-best-practices/AWS-stream-pipeline-redrawn.png` | ACCEPT | Labels and relationships preserved; both connectors have approximately 90–100px interior margins; no camera/browser/editor/selection artifacts; crisp and legible at lesson size |

The MLOps repair queue from the first review is therefore closed. This remains
an asset-level acceptance, not a claim that other course scopes are complete.

## ML regression screenshot repair follow-up

`0c4bceb` regenerated the first ten ML regression screenshot-derived assets
from original JPGs plus explicit bounded crops. Boole independently inspected
all ten at native and 608px lesson size.

| Batch | Accepted | Needs correction | Unresolved |
| --- | ---: | ---: | ---: |
| ML regression `0c4bceb` | 10 | 0 | 0 |

The reviewer confirmed exact UI labels/values, histogram axes and shapes,
split relationships, complete crops, no capture artifacts, byte-identical
imagegen outputs, C2PA/JUMD `gpt-image` provenance, and no post-generation
resizing or sharpening.

## DE repair follow-up

The five-target DE repair `04f9c77` was independently checked by Singer. Three
targets were accepted immediately; two warehouse targets required a second
correction because of source-value drift and a residual editor marker.

`de422d4` corrected those two targets, and Fermat independently accepted both
at native and 800px lesson size:

| Batch | Accepted | Needs correction | Unresolved |
| --- | ---: | ---: | ---: |
| DE five-target repair after `de422d4` | 5 | 0 | 0 |

The accepted warehouse values are exactly `105.9 MB` for partition pruning and
`843.5 MB` for cluster pruning; all five outputs have matching ledger hashes
and signed `gpt-image` provenance.

## ML evaluation repair follow-up

`0dfa1df` rebuilt the accuracy plot deterministically from all 21 lesson values
and removed the duplicate/wrong confusion-table image reference. Mencius
independently verified the 21 points, the `0.803` maximum at threshold `0.50`,
the axes, and the retained native table/output.

| Batch | Accepted | Removed/native | Unresolved |
| --- | ---: | ---: | ---: |
| ML evaluation `0dfa1df` | 1 | 1 | 16 |

The 16 provenance-unresolved evaluation assets remain explicitly open.

## ML classification and deployment/tree review baselines

Pascal's independent classification review found 7 accepted and 11
provenance-unresolved refs; James is reprocessing those 11 with retained
source/crop/imagegen evidence. Bacon's independent deployment/tree review
found 15 accepted, 13 semantic/axis corrections, 10 native removals, and 10
provenance-unresolved refs. Native removals are being handled in `14b5a3e`;
the 13 semantic/axis repairs are in a separate focused worker. These are open
queues, not crispness approvals.

### ML classification follow-up

Hume independently rechecked the two corrections in `bcb530d` at native and
rendered sizes. Both passed the visual and semantic checks: the correlation
diagram uses `MEDIUM` consistently, and the monthly-charges chart preserves
the lesson values with aligned `0/20/40/60%` guides. The imagegen/source
hash chain and C2PA metadata also matched the repair ledger. This acceptance
is limited to these two assets; it is not a repository-wide crispness claim.

| Batch | Accepted | Needs repair | Unresolved |
| --- | ---: | ---: | ---: |
| ML classification correction `bcb530d` | 2 | 0 | 0 |

### ML deployment/tree independent review

Worker commit `6a7a98c` replaced the 13 semantic/axis targets identified in
the deployment/tree baseline. It used imagegen for three semantic diagrams
and deterministic native rendering for ten exact plots, and added a
provenance ledger plus reproducible renderer. A separate Luna-max reviewer
checked every native asset and rendered-size view for visual crispness,
semantic fidelity, and crop/overlay defects. Twelve assets passed those
checks. One diagram is visually crisp but has reversed root-branch semantics
and is being corrected in a focused follow-up; it is not accepted.

| Batch | Implemented | Independently accepted | Needs repair |
| --- | ---: | ---: | ---: |
| ML deployment/tree repair `6a7a98c` | 13 | 12 | 1 |

The remaining diagram was regenerated in `1947c96` from its original JPG and
bounded crop. Banach independently checked the native and 608px renders,
confirmed the corrected `Yes → job in [yes]` and `No → seniority < 5`
branches, found no camera/overlay artifacts, and verified the imagegen
metadata and source/crop hashes.

| Batch | Accepted | Needs repair | Unresolved |
| --- | ---: | ---: | ---: |
| ML deployment/tree correction `1947c96` | 1 | 0 | 0 |

## ML deep-learning, serverless, and Kubernetes audit

Herschel independently reviewed all 173 active refs in ML modules 08--10 at
native size and simulated 608px lesson size. This is a bounded asset audit,
not a claim about the other ML modules.

| Scope | Accepted | Needs repair | Remove/native | Unresolved | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Deep learning | 34 | 3 | 24 | 7 | 68 |
| Serverless | 7 | 0 | 35 | 14 | 56 |
| Kubernetes | 11 | 3 | 33 | 2 | 49 |
| **Total** | **52** | **6** | **92** | **23** | **173** |

The six repair targets are: two dropout/overfitting diagrams and the
activation-functions image in deep learning; three Kubernetes intro diagrams.
The 23 unresolved refs are screenshot-derived or otherwise lacking a
verifiable redraw chain. Three Luna-max workers are processing these disjoint
module scopes. Native code, tables, plans, commands, and exact outputs are
being removed as image embeds rather than redrawn as invented illustrations.

### ML 08--10 repair progress

The first cleanup checkpoints are now pushed:

| Scope | Commit | Result | Remaining |
| --- | --- | --- | --- |
| Deep learning | `a765b7b` | removed 24 native-content embeds | 9 repair/unresolved targets |
| Deep learning | `3213505` | regenerated one unresolved visual with imagegen from original JPG + bounded crop | follow-up queue remains |
| Deep learning | `a3ab678` | regenerated the transfer-learning pooling visual with imagegen from original JPG + bounded crop | 8 repair targets |
| Serverless | `bc153ae` | removed 35 native-content embeds | 14 AWS/UI targets |

These checkpoint commits do not constitute crispness approval for the
remaining queues. Each regenerated asset still needs independent native-size
and lesson-size review before it is recorded as accepted.

Kubernetes has also completed its implementation queue in focused commits:
`c613aa7` removed 33 native-content embeds, `c4a0f88` regenerated the three
defective intro diagrams with imagegen, `d679ff8` removed a duplicate command
capture, and `ae4eb6c` documented the one AWS-console reference left
unresolved because a faithful redraw could invent UI text. The three
regenerated diagrams were independently checked and rejected for semantic
errors despite being genuinely crisp: two have incorrect service arrows and
the definitions diagram changes exact Kubernetes terms. A correction worker is
now fixing those three; the unresolved AWS-console item is not an approval.

Serverless then removed nine additional unreproducible AWS UI captures in
`2d32576` and `17db699`, preserving the JSON response natively. Five API
Gateway captures were then handled by `3ebc5a1`; the reconciliation below
supersedes this sentence. The generated replacements still require an
independent semantic review before they can be marked accepted.

## Checkpoint reconciliation after the ML 08--10 worker batches

The machine-learning-zoomcamp repository's committed head is synchronized at
`7481b93`. These are implementation checkpoints, not dimensions-only
crispness approvals. Every generated replacement is subject to the
independent review gate: exact source facts, correct relationships, no camera
or overlay artifacts, and readability at lesson size.

Completed implementation checkpoints:

- `3ebc5a1` regenerated the five API Gateway references with imagegen from
  each original JPG and bounded crop.
- `3213505` regenerated the convolution lesson's logistic-regression visual
  from its original JPG and crop.
- `a3ab678` regenerated the transfer-learning pooling visual from its original
  JPG and crop.
- `98cce69` regenerated seven deep-learning charts/diagrams: the transfer
  history plot, four learning-rate plots, and two dropout/overfitting plots.
- `0316a68` regenerated the ReLU activation visual.
- `1d093c9` regenerated the Kubernetes ingress and scaling diagrams after the
  first independent review found wrong service arrows.
- `7481b93` corrected the Kubernetes definitions terminology deterministically
  after the same review found altered exact terms.

Remaining bounded review targets:

### Deep learning — two regenerated assets awaiting independent review

- `08-deep-learning/images/04-conv-neural-nets-06-logistic-regression-crisp.png`
- `08-deep-learning/images/05-transfer-learning-05-pooling-vectors-crisp.png`

### Serverless — API Gateway follow-up

An independent review accepted asset 01. Assets 02, 04, and 05 were visually
accepted but require provenance-ledger correction: one source hash is
malformed, and the source JPG assignments for 04/05 are swapped relative to
their crops. Asset 06 needs a visual repair because an orange cursor/highlight
remains beside `Deploy API`. These four follow-ups are open.

Commit `51ef765` repaired the cursor/highlight and corrected the 02/04/05
source, crop, and output hash records. Darwin is independently rechecking all
five assets after that commit; none is promoted to final acceptance until that
review is recorded.

### Kubernetes — accepted correction and one unresolved source-faithfulness target

The prior independent review rejected the first redraws despite their visual
crispness. The corrected three-asset batch was independently accepted:

- `10-kubernetes/images/05-kubernetes-intro-04-external-internal-ingress-imagegen.png`
- `10-kubernetes/images/05-kubernetes-intro-05-definitions-imagegen.png`
- `10-kubernetes/images/05-kubernetes-intro-06-scaling-imagegen.png`

The following AWS-console capture was unresolved because a faithful redraw
could invent UI text:

- `10-kubernetes/images/08-eks-06-aws-console-crisp.png`

Commit `efc683b` removed that embed while preserving the source JPG, crop, and
PNG and recording exact hashes and the source-faithfulness rationale. The
lesson explanation remains in place, so this module no longer publishes that
unverified console capture.

Other previously recorded queues remain open: the 16 provenance-unresolved
assets in ML evaluation and the ten provenance-unresolved assets in ML
deployment/trees. The conservative scanner queue is not reduced by these
implementation commits until independent evidence is recorded.

## Bounded deep-learning chart review checkpoint

A read-only independent review checked the eight regenerated assets from
`98cce69` and `0316a68` at native size and at a simulated 608px lesson width.
The reviewer also inspected each retained original JPG and bounded crop, the
notebook values, and the repair provenance. All eight passed this bounded
review; this is not a claim about the remaining deep-learning assets or the
repository as a whole.

| Batch | Accepted | Needs repair | Remove | Scope |
| --- | ---: | ---: | ---: | --- |
| Deep-learning charts and ReLU review | 8 | 0 | 0 | `98cce69`, `0316a68` |

Accepted targets:

- `05-transfer-learning-08-history-plot-crisp.png`
- `06-learning-rate-04-train-accuracy-crisp.png`
- `06-learning-rate-05-val-accuracy-crisp.png`
- `06-learning-rate-06-two-lr-validation-crisp.png`
- `06-learning-rate-07-select-001-crisp.png`
- `08-more-layers-02-activation-functions-crisp.png`
- `09-dropout-07-dropout-02-vs-train-imagegen.png`
- `09-dropout-08-no-regularization-overfit-imagegen.png`

The seven plot files are deterministic native Matplotlib renders from the
lesson notebook values, not enlarged screenshots. The ReLU file is a clean
imagegen redraw with the equation and graph semantics preserved. All eight
were readable at 608px and had no camera, browser, overlay, or crop remnants.
The two remaining deep-learning redraws in the earlier open list were the
logistic-regression and pooling visuals from `3213505` and `a3ab678`.

Plato completed that final bounded review. Both assets passed native and 608px
checks, with exact lesson relationships, matching source/crop/output hashes,
C2PA imagegen metadata, and no camera, handwriting, player chrome, or overlay
artifacts.

| Batch | Accepted | Needs repair | Remove |
| --- | ---: | ---: | ---: |
| ML deep-learning final redraws `3213505` / `a3ab678` | 2 | 0 | 0 |

## Bounded Kubernetes correction review checkpoint

Pasteur independently reviewed the three corrected Kubernetes diagrams after
the first imagegen batch failed semantic review. All three passed native and
608px checks. The ingress and scaling diagrams contain clean imagegen
metadata; the definitions diagram is a deterministic SVG rasterization. The
review confirmed the exact service flow and terms `ClusterIP`, `LoadBalancer`,
and `same image and configuration`.

| Batch | Accepted | Needs repair | Remove |
| --- | ---: | ---: | ---: |
| Kubernetes correction `1d093c9` / `7481b93` | 3 | 0 | 0 |

## Bounded API Gateway review checkpoint

Hilbert independently reviewed all five API Gateway redraws at native and
608px sizes. Asset 01 passed outright. Assets 02, 04, and 05 were visually
correct but remain open until their source/crop/hash provenance is corrected;
asset 06 remains open for removal of an orange cursor/highlight artifact.

| Asset group | Visually accepted | Provenance follow-up | Needs visual repair |
| --- | ---: | ---: | ---: |
| API Gateway `3ebc5a1` | 4 | 3 | 1 |

Darwin rechecked the post-repair commit `51ef765`. All five assets now pass:
the 02/04/05 source/crop/output hashes match the corrected ledger, and the
06 orange cursor/highlight is gone. All five are genuine imagegen redraws with
clean native and 608px renders, C2PA metadata, and no camera/browser/cursor
overlays.

| Batch | Accepted | Needs repair | Unresolved |
| --- | ---: | ---: | ---: |
| API Gateway final review `51ef765` | 5 | 0 | 0 |

## LLM and MLOps strict re-audit follow-up

The strict re-audit covered all 37 LLM refs and all 37 local MLOps refs. LLM
had one semantic defect and one current-provenance gap; MLOps had no
instructional visual defects, but its decorative remote Streamlit badge was
removed as out of scope.

| Scope | Accepted | Needs repair | Remove/native | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| LLM strict audit baseline | 35 | 1 | 0 | 1 |
| MLOps strict audit baseline | 37 | 0 | 1 | 0 |

LLM commits `3394c44` and `24c46ca` repaired the judge comparison and
regenerated the agentic retry flow from its original JPG and bounded crop.
Halley independently accepted both at native and 608px sizes, including C2PA
and hash checks. MLOps commit `65c76a3` removed only the non-instructional
Streamlit badge; its 37 instructional assets remain accepted within this
bounded audit.

## DE focused repair review

The DE strict audit found the Docker-running screenshot technically sharp but
unreadable at lesson width because of its extreme aspect ratio. Commit
`90fc461` regenerated it with imagegen from the original JPG and bounded crop,
preserving the exact Docker facts and removing browser/overlay artifacts. The
wider DE audit still
has 34 inspected assets awaiting final rubric reconciliation and 8 not yet
inspected.

Kepler independently accepted `90fc461` at native and 608px sizes, confirming
the exact container ID, image, command, timestamps, ports, and container name,
plus matching JPG/crop/output hashes and C2PA metadata.

| Batch | Accepted | Needs repair | Unresolved |
| --- | ---: | ---: | ---: |
| DE Docker-running repair `90fc461` | 1 | 0 | 0 |

The ML deployment port-mapping failure was separately repaired in
`f951bbaec48899ac3145e0f73ce49cdec48e8935`: the focused redraw now shows
`HOST PORT 9696 → CONTAINER PORT 9696` and the exact `9696:9696` mapping at
608px, with matching provenance hashes. It still awaits an independent
reviewer; the worker's local check is not acceptance.

The DE 06-batch strict checkpoint then classified the eight previously
uninspected refs as follows:

| Batch | Accepted | Needs repair | Remove/native | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| DE 06-batch uninspected eight | 1 | 2 | 1 | 4 |

DE follow-up commits `3771ae1`, `ed8bfff`, and `f5605c6` repaired the missing
`1TB` mapPartitions annotation, regenerated the Dataproc submit form, and
removed the BigQuery traceback screenshot. Commits `28447dc` and `d93b267`
then regenerated the Spark master and worker UI captures with imagegen and
retained exact provenance. Descartes subsequently accepted the submit form,
master UI, and worker UI; the provenance-only follow-up remains open for
mapPartitions, Dataproc create-cluster, and reports-in-bucket.

Descartes independently reviewed six of those outputs. Spark master, worker,
and Dataproc submit-form outputs passed. MapPartitions still needs its tracked
crop retained; Dataproc create-cluster lacks a ledger row; reports-in-bucket
documents the wrong narrow crop. A provenance worker is fixing those three.

## ML tree provenance audit

The strict tree audit found 12 fresh refs: 11 visually crisp and semantically
correct but lacking durable source/crop/output chains, plus one XGBoost
parameter wording defect (`min_child_weight` was presented as equality with
`min_samples_leaf`). The focused worker retained/recreated evidence for the
11 and repaired the wording; the 11 plus the corrected XGBoost summary are now
independently accepted except for any future changes to those bytes.

Fermat independently accepted the corrected XGBoost summary in `991debf`,
including final-model values and reproducible hashes. The same review accepted
the DE Dataproc regeneration `9ffc47e` and the ML Docker port-mapping repair
`f951bba`, all at native and 608px sizes with C2PA and no capture artifacts.

## DE 06-batch strict audit checkpoints

The DE 06--16 audit classified 16 active refs: 9 accepted and 7 visually
crisp but provenance-unresolved. The unresolved set is four Spark-cluster
diagrams, one reshuffling diagram, one broadcast-exchange diagram, and one
RDD map/key-value diagram. The separate DE 01--05 audit inspected 18 refs but
stalled before final reconciliation; those 18 remain pending and are not
counted as accepted.

## ML classification and evaluation strict audit follow-up

Fresh strict audits replaced the earlier broad approvals for ML modules 03
and 04. Both audits inspected every active ref at native and simulated 608px
lesson size and kept provenance-unverified assets separate from acceptance.

| Scope | Accepted | Needs repair | Remove/native | Unresolved |
| --- | ---: | ---: | ---: | ---: |
| ML classification | 11 | 2 | 1 | 4 |
| ML evaluation | 3 | 2 | 1 | 15 |

Classification repairs are queued for the wrong production probability and
the ungrounded preprocessing/model-comparison diagram; the one-hot table will
be removed as native lesson markup. Evaluation repairs are queued for two
precision/recall visuals, while the low-value recall-definition image will be
removed. The 19 provenance-unresolved assets remain open.

Bacon independently rechecked the classification repairs: both visuals pass,
the one-hot image reference is gone, and the native table preserves all seven
rows and five encoded columns. The evaluation visuals are semantically correct
but initially failed provenance-only review because their bounded crops were
temporary. Commit `2de31ca` retained both crops and added the reproducible
crop script without changing published PNG pixels; a final provenance review
is still required.

| Follow-up batch | Accepted | Needs provenance review | Remove |
| --- | ---: | ---: | ---: |
| Classification `ef15e0f` / `5375259` | 2 | 0 | 1 image embed |
| Evaluation `00cf1c9` / `a755623` / `2de31ca` | 0 | 2 | 1 image embed |

Leibniz independently accepted the four classification provenance repairs in
`742f5c8`. All source JPGs, tracked crops, output hashes, crop-script
reproductions, C2PA metadata, and native/608px semantic checks passed. The
classification queue is therefore closed; the evaluation queue remains open
only for its 15 unresolved assets.

| Batch | Accepted | Needs repair | Unresolved |
| --- | ---: | ---: | ---: |
| Classification provenance closure `742f5c8` | 4 | 0 | 0 |

Archimedes completed the final evaluation provenance review after `2de31ca`.
Both tracked crops reproduce byte-for-byte from documented coordinates, and
source/crop/output hashes plus C2PA and native/608px semantic checks pass.

| Batch | Accepted | Needs repair | Unresolved |
| --- | ---: | ---: | ---: |
| Evaluation final provenance review `2de31ca` | 2 | 0 | 0 |

Boyle independently reviewed all 15 evaluation assets repaired in the later
batches. Twelve passed immediately; the final three provenance-only items
passed after `31d8a71` retained their crops and reproducible script. The
complete formerly unresolved evaluation queue is now accepted.

| Batch | Accepted | Needs repair | Remove |
| --- | ---: | ---: | ---: |
| Evaluation complete strict review | 15 | 0 | 0 |

The accepted asset in the initial eight-file checkpoint was the RDD DAG image.
Subsequent focused work restored the `1TB` mapPartitions annotation, rebuilt
the Dataproc submit form, and removed the BigQuery error embed. The current
open DE follow-up is provenance for mapPartitions, Dataproc create-cluster,
and reports-in-bucket; these are not silently promoted to accepted.

## Fresh strict audit: ML 01-intro

Arendt's strict re-audit of the current `cohorts/2026/01-intro` references
opened all 29 published outputs at native resolution and simulated 608px
lesson width. The result was **4 ACCEPT, 3 NEEDS, 0 REMOVE-NATIVE, and 22
UNRESOLVED**. The visual check found material redraws rather than simple
upscales and found no camera, browser-chrome, cursor, or accidental overlay
artifacts. The unresolved status is deliberate: 22 outputs have source and
C2PA evidence but no durable source-to-bounded-crop-to-output ledger.

The three repair findings are exact content defects, not “looks crisp”
judgments: two images spell `BMW` as `BWM`, and the suggested-price form leaves
the price field blank. The four accepted outputs are the multiclass,
multiple-comparisons, dot-product, and matrix-vector assets with complete
provenance. This re-audit does not promote the 22 unresolved images.

## Fresh strict audit: DE 04-analytics-engineering and 05-data-platforms

Lagrange found no active instructional illustrations in these modules. The
active local image references are video-navigation thumbnails; presenter faces,
camera insets, and play-button overlays are intentional for that role. Five
`05-data-platforms` thumbnails are byte-identical blank/near-black placeholders
and need either a verified first-party thumbnail or removal of only the image
embed while retaining the video link:

```text
thumbnail-YWDjnSxbBtY.jpg
thumbnail-uzp_DiR4Sok.jpg
thumbnail-ZElY5SoqrwI.jpg
thumbnail-XCx0nDmhhxA.jpg
thumbnail-3nykPEs_V7E.jpg
```

These are navigation-thumbnail repairs, not imagegen candidates. The module
scope correction is also recorded here: the repository has `05-data-platforms`,
not `05-batch-processing`; batch processing is module 06.

## Fresh strict audit: DE 06-batch follow-up

A strict seven-reference audit found **0 ACCEPT, 4 NEEDS, 0 REMOVE-NATIVE,
and 3 UNRESOLVED**. All seven current outputs were judged visually sharp at
native and 608px sizes and none was a simple enlargement or contained camera or
browser artifacts. The open findings are semantic or provenance gates:

- Spark UI has no job row although the lesson says it shows notebook jobs.
- The Pandas schema image says `head -n 1001` while the lesson requires
  `head -n 101`.
- The partitions diagram lacks arrows/executor labels.
- The built-in-functions image omits quotes around `HV0003`.
- StructType, `printSchema`, and `select` are visually/semantically correct
  but lack a durable source-to-crop-to-imagegen ledger.

The outputs contain image-generation metadata, but that alone is not accepted
provenance. The partition crop is also not tracked.

## Additional strict DE audit: 17 active references

The next DE reviewer did not stay limited to the requested early module
boundary; the report is therefore recorded by exact path rather than being
presented as a module-wide result. It inspected 17 active references and found
**11 ACCEPT, 5 REPAIR, and 1 REMOVE**. The accepted files were crisp and
video-backed. The concrete repair/remove queue is:

| File | Decision | Required action |
| --- | --- | --- |
| `02-workflow-orchestration/images/homework-cropped.png` | REMOVE | Replace the screenshot table with Markdown; retain the video/text link. |
| `01-data-warehouse-and-bigquery-06-partition-pruning-crisp.png` | REPAIR | Replace the `CREATE TABLE` result with the SELECT/query-cost evidence described by the lesson. |
| `04-internals-of-bigquery-03-dremel-tree-imagegen.png` | REPAIR | Restore the missing table name in the SQL header. |
| `06-deploying-a-machine-learning-model-04-model-status-crisp.png` | REPAIR | Regenerate the UI with exact line numbering and JSON. |
| `06-deploying-a-machine-learning-model-05-predict-crisp.png` | REPAIR | Reconcile the `22.2` image value with the lesson's `12.2` example. |
| `06-deploying-a-machine-learning-model-06-predict-payment-type-2-crisp.png` | REPAIR | Reconcile the trip-distance value and fix corrupted line numbering. |

The reviewer traced the accepted topics to the corresponding DE video
transcripts. No imagegen repair should proceed from a resized derivative; the
original source and a bounded crop must be retained first.

## Supplemental strict audit: MLOps

Pascal inspected 48 current references representing 45 unique files, including
the 11 AWS/cloud-console screenshots previously outside the smaller scanner
selection. The bounded result was **45 ACCEPT, 0 REPAIR, 0 REMOVE, and 0
PROVENANCE-BLOCKED**: the reviewer found the concept illustrations, diagrams,
and AWS screenshots crisp, useful, source-backed, and free of camera/face/play
button artifacts. The AWS password redaction is intentional. This is a bounded
MLOps result, not evidence about the other repositories.

## Independent review of the repair batch

Lovelace independently reopened the six changed DE items after `0825b7a` and
`580bcda`. All six passed: the five regenerated images were materially
different from resized crops, the exact SQL/JSON/prediction values matched the
lessons, C2PA metadata was present, and the removed homework screenshot was
replaced by a useful native Markdown table. This is the first repair batch in
this round that has both a worker report and a separate reviewer report.

The ML intro repair `fb9e15b` likewise used the original JPGs plus bounded
crops and recorded output hashes in the course provenance ledger. It remains
pending its separate whole-module reviewer; the repair worker's own visual
check is not an acceptance decision.

The independent whole-scope ML intro review is now complete: at `fb9e15b`, all
29 outputs were visually crisp at native and simulated 608px size, and none
was a simple enlargement or retained capture artifact. The bounded result is
**6 ACCEPT, 3 REPAIR, 0 REMOVE, and 20 PROVENANCE-BLOCKED**. The three content
repairs are the two `BWM` labels that should read `BMW`, plus a blank suggested-
price field. The 20 visually good outputs remain blocked until their durable
source-to-bounded-crop-to-output ledgers are recorded; they are not silently
promoted to accepted.

The independent MLOps re-audit did not confirm the earlier 45/45 result. It
accepted 44 of 45 unique files and found one repair: `02-experiment-tracking/
images/db_password.png` still exposes password glyphs through its redaction.
That asset is queued for opaque deterministic redaction or removal; imagegen
must not be used to recreate secret-bearing text.

The queued MLOps repair `8bf083a` replaced that incomplete redaction with a
uniform opaque pixel block. Newton independently confirmed full opacity, no
remaining OCR text at native or 608px size, and intact surrounding UI. The
asset is now accepted.

The ML intro content repair required a correction. `65d5619` fixed the two
`BWM` labels, but its worker invented `850,000 UAH` in the suggested-price
field. Herschel rejected that unsupported value. `20a1024` regenerated only
that image from the original JPG plus bounded crop with the field blank;
Aquinas independently accepted it. The three-item repair queue is therefore
closed with two accepted at `65d5619` and the corrected third at `20a1024`.

Faraday independently accepted all four DE 06-batch semantic repairs in
`3a861c3`, including the blank Jobs-page caption correction, exact
`head -n 101`, six correct partition-to-executor arrows, and quoted `HV0003`.

## Fresh strict audit: LLM 2026

Bernoulli independently reopened all 37 active local instructional image
references at `24c46ca`, native and simulated 608px size. The old `37/37`
acceptance is withdrawn. All 37 were visually crisp and free of faces,
camera/browser chrome, cursors, play buttons, and selection overlays, but the
evidence gate produced **6 ACCEPT, 1 REPAIR, 0 REMOVE, and 30
PROVENANCE-BLOCKED**. C2PA/OpenAI metadata does not prove the source-to-output
chain, and 28 assets lacked an original same-stem source for a direct
anti-upscale comparison.

The repair is
`cohorts/2026/01-agentic-rag/images/11-agents-intro-04-agentic-flow-diagram-
imagegen.png`: the failed search must say `Olama`, while the corrected retry
must say `Ollama`. The remaining 30 outputs are not being called accepted until
their current published hashes and source/reference-to-crop-to-output records
are durable.

The focused LLM repair `7f32e2d` regenerated that flow from the original JPG
and retained crop. Galileo independently accepted the corrected sequence
(`Olama` failure → typo detected → `Ollama` retry), with native/608px checks,
non-upscale comparison, matching hashes, and C2PA metadata. The LLM repair
queue is closed for this asset; the other 30 provenance-blocked assets remain
open.
