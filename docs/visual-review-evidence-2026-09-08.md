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

## Completed visual audits

| Scope | Repository head | Retained active references reviewed | Result | Units without illustrations |
| --- | --- | ---: | --- | ---: |
| ML 2026 | `bfafbbb` | 581/581 | PASS; 0 failures, 0 missing local refs | 0/105 |
| LLM 2026 | `c557a0a` | 38/38 | PASS; 0 soft/chrome-heavy retained assets | 36/72 |
| MLOps current lesson set | `e68ba45` | 38 current-scope refs; repository-wide legacy refs also cleaned | PASS; 0 broken refs after cleanup | 2/7 |
| DE 2027 draft | `21b6693` | 111 retained from 175 reviewed occurrences | PASS for retained assets; 64 unsupported assets removed | 66/88 |

“Units without illustrations” is intentionally not hidden: those units lost
unsupported or invented visuals during the distrust audit. They should receive
a source-backed illustration only when one can be found; do not fill the gap
with made-up content merely to reach 100% coverage.

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
