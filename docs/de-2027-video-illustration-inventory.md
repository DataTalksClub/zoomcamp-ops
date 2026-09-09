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
| 01 | `lP8xXebHmuE` | 01–09 Docker/Postgres workshop | **UNPROCESSED** | Docker workflow, virtual environment, Dockerfile, Postgres, ingestion, pgAdmin/Compose; one source spans nine lessons |
| 01 | `QEcps_iskgg` | 10 SQL refresher | **UNPROCESSED** | Join/group/aggregation result; prefer native SQL/result markup |
| 01 | `18jIzE41fJ4` | 12 Terraform overview; 13 GCP overview | **UNPROCESSED** | Terraform plan/apply and GCP resource relationship; one source spans two lessons; never expose credentials |
| 01 | `s2bOYDCKl_M` | Terraform supplemental/setup content linked from module 01 | **UNPROCESSED** | Terraform files/declarations and plan/apply |
| 01 | `Y2ux7gq3Z0o` | Terraform supplemental/setup content linked from module 01 | **UNPROCESSED** | One-file configuration to provisioned resource |
| 01 | `PBi0hHjLftk` | Terraform supplemental/setup content linked from module 01 | **UNPROCESSED** | Variables file versus hard-coded configuration |
| 01 | `JgspdlKXS-w` | Course introduction/overview only | **SUPPLEMENTAL** | Skip for instructional lesson illustrations |
| 02 | `-JLnp-iLins`, `ZvVN_NmB_1s`, `wgPxC4UjoLM`, `MNOKVx8780E`, `VAHm0R_XjqI`, `-KmwrCqRhic`, `Z9ZmmwtXDcU`, `1pu_C_oOAMA`, `E04yurp1tSU`, `TLGFAOHpOYM`, `52u9X_bfTAo`, `b-6KhfWfk2M`, `GHPtRDAv044`, `LmnfjGKwnVU`, `3IbjHfC8bMg`, `XuPDQ1UcNyI` | Lessons 01–16, one video per lesson | **UNPROCESSED** | Process-flow/UI/result frames; date matrices and comparison tables become native markup |
| 03 | `jrHljAoD6nM`, `-CqXf7vhhDs`, `k81mLJVX08w`, `eduHi1inM4s`, `B-WtpB0PuG4`, `BjARzEWaznU` | Lessons 01–06 | **REOPENED** | Existing module-03 images need a fresh crispness pass; four documented imagegen diagrams can remain after review |
| 04 | `uF76d5EmdtU`, `gsKuETFJr54`, `2dYDS4OQbT0`, `7CrrXazV_8k`, `JQYz-8sl1aQ`, `lT4fmTDEqVk`, `UqoWyMjcqrA`, `bvZ-rJm7uMU`, `KfhUA9Kfp8Y`, `t4OeWHW3SsA` | Lessons 01–11 (lesson 03 has no current video URL) | **UNPROCESSED** | dbt project/source/model/test/documentation/command states |
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

The initial audit found:

- Module 01: 0 current instructional image references.
- Module 02: 0 lesson illustrations (one homework screenshot is separate).
- Module 03: 32 active image references before the latest cost-slide removal;
  four have direct imagegen evidence, while the remaining screenshot-derived
  set is reopened for crispness.
- Module 06: screenshot-derived assets exist, but their crop/upscale/sharpen
  provenance does not satisfy the new crispness rule.
- Modules 04, 05, and 07: no current instructional image set was found.

This inventory does not claim that every lesson should receive an image. Each
candidate still has to pass the illustration rubric and the independent visual
review gate.

## Verification — 2026-09-09

### DE module 01 canonical-video audit

| Canonical video | Unit coverage | Verification state |
| --- | --- | --- |
| `lP8xXebHmuE` | Units 01–09 | Transcript cached; no local video/frame. |
| `QEcps_iskgg` | Unit 10 | No cached transcript or original frame. |
| `18jIzE41fJ4` | Units 12–13 | No transcript/frame; 12/13 split unresolved. |
| — | Unit 11 | No canonical video identified. |

Fetch attempts for `QEcps_iskgg`, `18jIzE41fJ4`, and the legacy supplemental
IDs `s2bOYDCKl_M`, `Y2ux7gq3Z0o`, `PBi0hHjLftk`, and `JgspdlKXS-w` hit proxy
HTTP 407. Those failed fetches are not source evidence.

The following cues are backed by the cached transcript for `lP8xXebHmuE` and
are provisional for units 01–09 only. None is accepted without fetching and
inspecting the original frame.

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
