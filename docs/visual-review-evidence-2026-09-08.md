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
| ML 2026 | superseded by `85f83bb` | 353 current active refs | **OPEN**; 345 reviews remain in the four-repo live queue | 15/105 currently missing active refs |
| LLM 2026 | `c557a0a` | 38 current local refs | **OPEN**; no crispness acceptance | 36/72 |
| MLOps current lesson set | `e68ba45` | 38 current-scope refs | **OPEN**; no crispness acceptance | 2/7 |
| DE 2027 draft | `4bf778d` | 61 current refs | **OPEN**; no repository-wide acceptance | 69/88 |

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
