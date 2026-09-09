# ML Zoomcamp 2026 workshop illustration inventory

This is the workshop-specific companion to the current illustration audit. It
covers the four video-backed ML Zoomcamp workshops that are stored under the
2026 cohort: deployment/FastAPI, deep learning, serverless, and Kubernetes.

The workshop READMEs are processed independently. The FastAPI workshop now has
two published, source-backed imagegen illustrations; the other three workshops
are still in the source-frame audit queue. A missing image is never treated as
proof that a video has no useful teaching visual.

## Video and unit map

| Workshop unit | YouTube video | Transcript cache | Current published illustrations | Initial candidate teaching points |
| --- | --- | --- | --- | --- |
| Module 5: FastAPI and uv | `jzGzw98Eikk` | `/home/alexey/.cache/youtube_transcripts/jzGzw98Eikk.txt` | 2 imagegen assets; accepted in `5256dd8` | model → prediction service; FastAPI request/response; pipeline and model artifact; Docker/Fly deployment state |
| Deep learning / PyTorch | `Ne25VujHRLA` | `/home/alexey/.cache/youtube_transcripts/Ne25VujHRLA.txt` | Source acquired; candidate audit in progress | image → preprocessing tensor → pretrained model → class scores; transfer learning; frozen base plus ten-class head |
| Serverless deployment | `sHQaeVm5hT8` | `/home/alexey/.cache/youtube_transcripts/sHQaeVm5hT8.txt` | Source acquired; candidate audit in progress | Lambda request/response; model-in-Docker packaging; scikit-learn/ONNX deployment path; pay-per-request boundary |
| Kubernetes deployment | `c_CzCsCnWoU` | `/home/alexey/.cache/youtube_transcripts/c_CzCsCnWoU.txt` | Source acquired; candidate audit in progress | model → FastAPI → Docker → Kind/Kubernetes; ONNX inference; health checks; deployment/service/pod relationships |

The `/home/alexey/git/workshops` source repository contains the corresponding
ML workshop projects (`mlzoomcamp-fastapi-uv`, `mlzoomcamp-deep-learning`,
`mlzoomcamp-serverless`, and `mlzoomcamp-k8s`) but likewise has no published
illustration references in those project READMEs. The canonical cohort targets
are `05-deployment/workshop/README.md`,
`08-deep-learning/pytorch/README.md`, `09-serverless/workshop/README.md`, and
`10-kubernetes/workshop/README.md`.

## Processing status

FastAPI is **PUBLISHED — 2 ASSETS**. Its source video was acquired through the
DataImpulse route, candidate frames were reviewed, and the accepted diagrams
were independently checked for legibility, source support, and removal of
faces/Zoom/editor overlays. Deep Learning, Serverless, and Kubernetes are
**AUDIT IN PROGRESS** after successful source acquisition. No asset is
published for those units until candidate provenance and an independent review
are complete.

The FastAPI audit and independent-review report are the evidence for its
publication decision. The other three audit reports are being built from the
validated source videos in the same way: fetch → extract → rubric →
crop/regenerate → independent review. A worker must not call a candidate
publishable merely because a source frame exists.

For a retained screenshot-derived frame, preserve the original frame, make a
native bounded crop, and pass both the original and crop to imagegen when the
worker has that skill. Exact code, UI labels, URLs, plots, numbers, and
tables must instead use deterministic rendering or native lesson markup. Every
accepted asset needs a YouTube ID/timestamp, source and crop coordinates,
rubric score, output hash, and independent visual review.

The absence of an image in a workshop README is therefore a queue item for
review, not permission to invent a decorative diagram or to copy an arbitrary
screen from the recording.

The transcript fetch succeeded for all four videos. DataImpulse's documented
proxy route supplied validated local source videos for the current pass; the
source files remain in ignored scratch directories and are not published in a
tracked course path. Each frame-extraction pass records the actual source path,
duration, dimensions, and hash in its audit before any final asset is added.
