# ML Zoomcamp 2026 workshop illustration inventory

This is the workshop-specific companion to the current illustration audit. It
covers the four video-backed ML Zoomcamp workshops that are stored under the
2026 cohort: deployment/FastAPI, deep learning, serverless, and Kubernetes.

The workshop READMEs currently contain no embedded instructional image
references and their workshop directories contain no published image assets.
That is an inventory result, not an approval that the videos need no
illustrations. Each video must still be checked against the illustration rubric
before a useful, source-backed visual is added.

## Video and unit map

| Workshop unit | YouTube video | Transcript cache | Current published illustrations | Initial candidate teaching points |
| --- | --- | --- | --- | --- |
| Module 5: FastAPI and uv | `jzGzw98Eikk` | `/home/alexey/.cache/youtube_transcripts/jzGzw98Eikk.txt` | None; audited in `6302aed` | model → prediction service; FastAPI request/response; pipeline and model artifact; Docker/Fly deployment state |
| Deep learning / PyTorch | `Ne25VujHRLA` | `/home/alexey/.cache/youtube_transcripts/Ne25VujHRLA.txt` | None; six candidates rejected in `ce2198e` | image → preprocessing tensor → pretrained model → class scores; transfer learning; frozen base plus ten-class head |
| Serverless deployment | `sHQaeVm5hT8` | `/home/alexey/.cache/youtube_transcripts/sHQaeVm5hT8.txt` | None; no candidate cleared in `d6e3afc` | Lambda request/response; model-in-Docker packaging; scikit-learn/ONNX deployment path; pay-per-request boundary |
| Kubernetes deployment | `c_CzCsCnWoU` | `/home/alexey/.cache/youtube_transcripts/c_CzCsCnWoU.txt` | None; no candidate cleared in `6ff0694` | model → FastAPI → Docker → Kind/Kubernetes; ONNX inference; health checks; deployment/service/pod relationships |

The `/home/alexey/git/workshops` source repository contains the corresponding
ML workshop projects (`mlzoomcamp-fastapi-uv`, `mlzoomcamp-deep-learning`,
`mlzoomcamp-serverless`, and `mlzoomcamp-k8s`) but likewise has no published
illustration references in those project READMEs. The canonical cohort targets
are `05-deployment/workshop/README.md`,
`08-deep-learning/pytorch/README.md`, `09-serverless/workshop/README.md`, and
`10-kubernetes/workshop/README.md`.

## Processing status

All four units are now **AUDITED — NO PUBLISH** for video-backed
illustrations. The workers scored candidates and found no publishable visual:
FastAPI could not acquire a source frame, while the Deep Learning, Serverless,
and Kubernetes candidates failed the publish gate. No README image reference
was added, and no decorative or transcript-invented visual was substituted.

The four audit reports are the evidence for this no-publish decision. Reopen a
unit only if a source recording becomes available or the lesson context
changes; then repeat the same fetch → extract → rubric → crop/regenerate →
independent-review flow.

For a retained screenshot-derived frame, preserve the original frame, make a
native bounded crop, and pass both the original and crop to imagegen when the
worker has that skill. Exact code, UI labels, URLs, plots, numbers, and
tables must instead use deterministic rendering or native lesson markup. Every
accepted asset needs a YouTube ID/timestamp, source and crop coordinates,
rubric score, output hash, and independent visual review.

The absence of an image in a workshop README is therefore a queue item for
review, not permission to invent a decorative diagram or to copy an arbitrary
screen from the recording.

The transcript fetch succeeded for all four videos. Direct `yt-dlp` downloads
from this environment were blocked by YouTube's bot check, so no video was
published or placed in a tracked directory. The frame-extraction pass must use
the documented mirror/download workflow or an already available local source,
then record the actual source path and duration in the per-image provenance.
