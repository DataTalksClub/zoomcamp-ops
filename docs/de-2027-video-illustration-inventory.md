# DE Zoomcamp 2027 video-to-illustration inventory

Updated **2026-09-09**. This inventory compares the current
`cohorts/2027` lessons with the canonical workshop/module pages at the
repository root. A video is **unprocessed** when its current lesson has no
source-backed illustration derived from that recording. A video is **reopened**
when illustrations exist but their crispness was only established by crop,
upscale, or sharpening.

## Selection rules

- Use the canonical module/workshop recording for the current lesson it
  teaches; community walkthroughs are not canonical source material.
- A single recording can map to several lessons. Record the video once and
  map accepted frames to the relevant lesson(s).
- Extract only frames that teach a durable concept, relationship, result, or
  state. A table/list becomes native Markdown/HTML; it is not a screenshot
  deliverable.
- A `*-crisp` filename is not evidence of crispness. Existing screenshot
  assets remain open until imagegen provenance and an independent visual check
  exist.

## Canonical video map

| Module | Video | Current lesson(s) | Current status | Candidate use |
| --- | --- | --- | --- | --- |
| 01 | `lP8xXebHmuE` | 01–09 Docker/Postgres workshop | **PROCESSED — 1 ASSET** | Docker volume relationship; raw screenshots rejected, conceptual redraw published in unit 01 |
| 01 | `QEcps_iskgg` | 10 SQL refresher | **AUDITED — NO ASSET** | Exact joins/grouping/aggregation results remain native SQL/result markup |
| 01 | `18jIzE41fJ4` | 12 Terraform overview; 13 GCP overview | **PROCESSED — 1 ASSET** | GCP service-family relationship published in unit 13; no credentials or exact UI |
| 01 | `s2bOYDCKl_M` | Terraform supplemental/setup content linked from module 01 | **PROCESSED — 1 ASSET** | Terraform/provider flow published in unit 12; raw editor/camera state rejected |
| 01 | `Y2ux7gq3Z0o` | Terraform supplemental/setup content linked from module 01 | **AUDITED — NO ASSET** | Exact Terraform/UI state needs native treatment; no imagegen asset published |
| 01 | `PBi0hHjLftk` | Terraform supplemental/setup content linked from module 01 | **AUDITED — NO ASSET** | Credential/project identifiers and exact state are publication hard gates |
| 01 | `JgspdlKXS-w` | Course introduction/overview only | **SUPPLEMENTAL** | Skip for instructional lesson illustrations |
| 02 | `-JLnp-iLins`, `ZvVN_NmB_1s`, `wgPxC4UjoLM`, `MNOKVx8780E`, `VAHm0R_XjqI`, `-KmwrCqRhic`, `Z9ZmmwtXDcU`, `1pu_C_oOAMA`, `E04yurp1tSU`, `TLGFAOHpOYM`, `52u9X_bfTAo`, `b-6KhfWfk2M`, `GHPtRDAv044`, `LmnfjGKwnVU`, `3IbjHfC8bMg`, `XuPDQ1UcNyI` | Lessons 01–16, one video per lesson | **AUDITED — NO ASSET** | 23 native-only review candidates; date matrices, comparison tables, exact UI, code, and results remain native markup |
| 03 | `jrHljAoD6nM`, `-CqXf7vhhDs`, `k81mLJVX08w`, `eduHi1inM4s`, `B-WtpB0PuG4`, `BjARzEWaznU` | Lessons 01–06 | **AUDITED — 12 CRISP ASSETS** | 12 source-backed bitmaps retained; three table/result screenshots converted to native Markdown and one unsafe terminal screenshot removed |
| 04 | `uF76d5EmdtU`, `gsKuETFJr54`, `2dYDS4OQbT0`, `7CrrXazV_8k`, `JQYz-8sl1aQ`, `lT4fmTDEqVk`, `UqoWyMjcqrA`, `bvZ-rJm7uMU`, `KfhUA9Kfp8Y`, `t4OeWHW3SsA` | Lessons 01–11 (lesson 03 has no current video URL) | **PROCESSED — 3 ASSETS** | Three durable source-backed concepts were regenerated with imagegen; exact code/UI/table/terminal candidates remain native or were rejected |
| 05 | `f6vg7lGqZx0`, `JJwHKSidX_c`, `q0k_iz9kWsI`, `224xH7h8OaQ`, `uBqjLEwF8rc`, `YWDjnSxbBtY`, `uzp_DiR4Sok`, `ZElY5SoqrwI`, `XCx0nDmhhxA`, `3nykPEs_V7E` | Lessons 01–10 | **UNPROCESSED** | Bruin concepts, pipeline/assets/variables/commands, durable UI/result states |
| 06 | `dcHe5Fl3MF8`, `FhaqbEOuQ8U`, `hqUbB9c8sKg`, `r_Sf6fCB40c`, `ti3aC1m3rE8`, `CI3P4tAtru4`, `uAlp2VuZZPY`, `68CipcZt7ZA`, `9qrDsY_2COo`, `lu7TrqAWuH4`, `Bdu-xIrF3OM`, `k3uB2K99roI`, `Yyz293hBVcQ`, `HXBwSlXo5IA`, `osAiAYahvh8`, `HIm2BOj8C0Q` | Lessons 01–16 | **REOPENED** | Existing image set is source-backed but most screenshot replacements are crop/upscale/sharpen; regenerate retained screenshots or replace duplicated exact output with native content |
| 07 | `YDUgFeHQzJU` plus the canonical theory recordings `hfvju3iOIP0`, `WxTxKGcfA-k`, `zPLZUDPi4AY`, `ZnEZFEYKppw`, `aegTuyxX7Yg`, `SXQtWyRpMKs`, `dUyA_63eRb0`, `NcpKlujh34Y`, `TNx5rmLY8Pk`, `r1OuLdwxbRc`, `DziQ4a4tn9Y`, `tBY_hBuyzwI` | Current introduction and theory lessons | **UNPROCESSED** | Process only source-backed streaming concepts from these recordings; remove unsupported/invented illustrations |

## Module 01 shared-video chop plan

The cached transcript for `lP8xXebHmuE` already identifies useful windows:

| Approximate window | Lesson mapping | Keep as an illustration only when it shows |
| --- | --- | --- |
| 09:33–27:52 | 01 introduction | Docker/container relationship or a meaningful command result |
| 36:23–42:00 | 02 virtual environments | environment isolation/result, not command typing |
| 42:55–55:41 | 03 Dockerfile | completed image/container state or layered relationship |
| 56:45–1:07:26 | 04 Postgres | running database container and durable connection state |
| 1:07:34–1:28:55 | 05 data ingestion | successful ingestion/result state |
| 1:29:00–1:45:39 | 06 ingestion script | notebook-to-script result, not duplicated code |
| 1:48:08–2:02:42 | 07–09 pgAdmin/network/Compose | connected services or successful multi-container state |
| 2:04:58–2:06:19 | 08–09 wrap-up | only if it adds a result not present in the lesson |

The source recording and extracted candidates belong under the repository's
gitignored `.tmp/videos/` and `.tmp/illustrations/`; only reviewed final assets
and this provenance map are publishable.

## Current illustration audit

The current audit found:

- Module 01: 3 accepted source-backed imagegen references; all raw screenshot
  crops remain scratch evidence only.
- Module 02: 0 lesson illustrations (one homework screenshot is separate).
- Module 03: 12 source-backed bitmap references remain after independent review;
  three table/result screenshots were converted to native Markdown and one
  unsafe terminal screenshot was removed. All retained bitmaps are genuinely
  crisp; no resize-only output remains.
- Module 04: 3 source-backed imagegen assets passed independent visual review;
  exact code/UI/table/terminal candidates remain native or were rejected.
- Module 06: source/frame audit is complete; 13 conceptual redraws await
  independent review, one needs a new crop/redraw, 26 exact/native candidates
  should remain native, and one warning-heavy screenshot should be removed.
- Module 07: source/frame audit is complete; 7 sources have redraw-worthy
  concepts, while exact/native and unsuitable candidates remain documented. No
  bitmap was published.
- Module 05: source/frame audit is still in progress.

This inventory does not claim that every lesson should receive an image. Each
candidate still has to pass the illustration rubric and the independent visual
review gate.

## Verification — 2026-09-09

### DE module 01 canonical-video audit and closure

| Canonical video | Unit coverage | Verification state |
| --- | --- | --- |
| `lP8xXebHmuE` | Units 01–09 | Transcript cached; source validated; one conceptual volume illustration published in unit 01. |
| `QEcps_iskgg` | Unit 10 | Source validated; exact SQL/result views audited and kept native; no bitmap published. |
| `18jIzE41fJ4` | Units 12–13 | Source validated; one conceptual GCP service-family illustration published in unit 13. |
| `s2bOYDCKl_M` | Supplemental Terraform setup | Source validated; one conceptual Terraform/provider illustration published in unit 12. |
| `Y2ux7gq3Z0o` | Supplemental Terraform setup | Source validated; no asset after native UI/identifier review. |
| `PBi0hHjLftk` | Supplemental Terraform setup | Source validated; no asset after credential/project-identifier review. |
| — | Unit 11 | No canonical video identified. |

The six source videos above were acquired through the documented DataImpulse
route and validated with `ffprobe`. The worker preserved source hashes, frame
hashes, native crop coordinates, and candidate decisions under
`.tmp/workshop-processing/de-2027-m01/`. The three accepted assets were made
with imagegen from the original source frame plus focused crop, independently
reviewed, and committed with tracked provenance in the DE module-01 directory.
The raw JPEG frames and crops are not published.

The following cues remain useful as audit context for units 01–09; the accepted
asset is limited to the durable volume relationship:

| Unit(s) | Transcript window | Provisional candidate cue |
| --- | --- | --- |
| 01 | 09:33–27:52 | Docker/container relationship or command result |
| 02 | 36:23–42:00 | Environment isolation/result, not command typing |
| 03 | 42:55–55:41 | Completed image/container state or layered relationship |
| 04 | 56:45–1:07:26 | Running database container and durable connection state |
| 05 | 1:07:34–1:28:55 | Successful ingestion/result state |
| 06 | 1:29:00–1:45:39 | Notebook-to-script result, not duplicated code |
| 07–09 | 1:48:08–2:02:42 | Connected services or multi-container state |
| 08–09 | 2:04:58–2:06:19 | Wrap-up result only if not in the lesson |

### DE module 02 audit and closure

All 16 canonical workflow-orchestration recordings were acquired through the
DataImpulse route, validated with `ffprobe`, and sampled at source resolution.
The complete worker report is
`.tmp/workshop-processing/de-2027-m02/status.md`. It records 16/16 validated
downloads, 262 sampled originals, and 23 retained review candidates. Every
retained candidate is native-only: topology/Gantt/input/result screens, exact
code or commands, or transient Kestra/GCP UI. No imagegen asset was generated
or published, and all raw source MP4s were removed after their hashes and audit
records were preserved. This is an intentional no-asset decision, not a claim
that the videos contain no useful teaching moments.

### DE module 03 audit and closure

The complete source/frame/current-asset audit is under
`.tmp/workshop-processing/de-2027-m03/STATUS.md`, with the independent review
under `.tmp/workshop-processing/de-2027-m03/INDEPENDENT-REVIEW.md`. All 16
pre-change bitmaps were inspected at normal lesson width: 10 passed directly
and six were conditional. The conditional cases were resolved without
inventing visuals: three exact table/result screenshots became native Markdown
tables, one terminal screenshot containing an unnecessary `rm -rf model`
command was removed, and three path/SHA provenance typos were corrected in the
tracked module audit. The remaining 12 bitmap assets are source-backed,
crisp, and free of presenter/camera/Zoom/editor overlays.

### DE module 04 audit and closure

The complete Module 04 source/frame audit is under
`.tmp/workshop-processing/de-2027-m04/audit-summary.md`; the tracked visual
provenance is `cohorts/2027/04-analytics-engineering/visual-audit-2026-09-09.md`,
and the independent review is under
`.tmp/workshop-processing/de-2027-m04/INDEPENDENT-REVIEW.md`. All 10 canonical
videos and transcripts were validated. Three durable concepts were selected
from the recordings, cropped with source coordinates, and regenerated from the
original frame plus focused crop: the analytics-engineering toolchain, the dbt
model-to-warehouse flow, and dbt lineage. The first dbt-flow redraw was rejected
because its persistence path implied a loop; it was regenerated and re-reviewed.
All three final assets passed independent visual review. Exact code, tables,
editor/browser/terminal UI, and transient values were not published as bitmap
illustrations.

### DE module 07 audit

`YDUgFeHQzJU` has a cached transcript, but no bitmap references remain. The
two native Mermaid diagrams in unit 10 are source-backed and retained. The
unsupported generated visuals `06-why-flink` and
`10-tumbling-window-watermark` have already been removed.

The prioritized transcript-backed candidates below remain **UNPROCESSED**
until their original frames are fetched and inspected. Scores prioritize
review; they do not indicate acceptance.

| Unit | Timestamp | Score | Status |
| --- | --- | ---: | --- |
| 02 | 13:18–13:49 | 9 | **UNPROCESSED** — frame fetch/inspection pending |
| 05 | 47:57–48:33 | 9 | **UNPROCESSED** — frame fetch/inspection pending |
| 07 | 1:03:03–1:03:21 | 10 | **UNPROCESSED** — frame fetch/inspection pending |
| 08 | 1:09:31–1:10:57 | 9 | **UNPROCESSED** — frame fetch/inspection pending |
| 11 | 1:17:29–1:17:41 | 10 | **UNPROCESSED** — frame fetch/inspection pending |

Exact UI or terminal candidates must use a deterministic native crop after the
original frame is inspected; imagegen is not permitted for those candidates.
No invented assets were added, and nothing is published yet.

### Module 03 deployment screenshot closure

The six existing source-backed screenshots in the module 03 deployment lesson
were refreshed after this inventory was reopened. Each pass sent the original
JPG and true native crop to imagegen for a clean frame/background reference;
the exact terminal or Postman content was then rendered deterministically.
Resize-only or sharpen-only derivatives were rejected. The current published
commits are `8478f19`, `d78ba11`, `92a20c6`, `051e3b6`, and `44fca50` (with
`1353000` covering the first deployment frame), and every target has an
independent acceptance record. This closes the module 03 deployment screenshot
queue without changing the source-video inventory above.
