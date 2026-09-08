# Imagegen regeneration ledger — 2026-09-08

This ledger records the imagegen replacements made during the crispness
re-audit. Every generation used the retained original non-crisp source and a
crop/reference after the source was inspected. The crop was never treated as
the authoritative replacement. Original JPGs and crop preparation files stay
in their course repositories.

`pending re-review` is intentional: the implementation check is not an
independent acceptance. A reviewer must compare the published target with the
source and lesson invariants before it can be called accepted.

| Repository / published target | Original + crop input | Imagegen output ID | Commit | Implementation check |
| --- | --- | --- | --- | --- |
| DE `03-data-warehouse/...04-external-table-details-crisp.png` | `...04-external-table-details.jpg` + `...-cropped.png` | `exec-dab7881d-712e-4b53-8bb4-643dbaeadcda` | `cc8ee1f` | Crisp, camera-free; pending independent URI review |
| DE `03-data-warehouse/...05-partitioning-diagram-crisp.png` | `...05-partitioning-diagram.jpg` + `...-cropped.png` | `exec-1c2d90b0-45db-42ec-8f1b-3f3699a8c160` | `1fbadf9` | Regenerated with lowercase `stackoverflow`; pending re-review |
| DE `03-data-warehouse/...06-partition-pruning-crisp.png` | `...06-partition-pruning.jpg` + `...-cropped.png` | `exec-2d5f10b4-f8fa-418a-b374-4fcb2087fcd7` | `e043b33` | Crisp; mixed estimate/result state retained from source |
| DE `03-data-warehouse/...07-clustering-diagram-crisp.png` | `...07-clustering-diagram.jpg` + `...-cropped.png` | `exec-5c4be96f-4005-4e74-9237-f2ad0b6672fd` | `eb0bc99` | Crisp, labels and grouping preserved |
| DE `03-data-warehouse/...08-cluster-pruning-crisp.png` | `...08-cluster-pruning.jpg` + `...-cropped.png` | `exec-d9222db8-287c-4eaa-8978-c4ae7a8ac262` | `e043b33` | Crisp, values preserved |
| DE `03-data-warehouse/...05-model-choice-crisp.png` | `...05-model-choice.jpg` + `...-cropped.png` | `exec-c9f8c20c-56aa-466e-8ae2-bb8b2d4d54b2` | `1fbadf9` | Title restored; pending re-review |
| DE `03-data-warehouse/...06-deploying...01-exported-to-gcs-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-540fa0ba-ed2b-4dc7-8ecb-041f26dfc26e` | `73b1eff` | Crisp, bucket and `tip_model/` preserved; pending re-review |
| DE `03-data-warehouse/...06-deploying...02-copy-model-local-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-19d100c2-800a-4f91-bc7b-f444e02d08cb` | `73b1eff` | Crisp terminal; key paths preserved; pending re-review |
| DE `03-data-warehouse/...06-deploying...03-docker-running-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-80f7cf89-bd43-4547-8df9-8f6dc4649281` | `73b1eff` | Crisp `docker ps` state; pending re-review |
| DE `03-data-warehouse/...06-deploying...04-model-status-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-8111c860-e8ae-4f20-a906-2e4ae45bb983` | `7bc4aed` | Crisp `AVAILABLE` response; pending re-review |
| DE `03-data-warehouse/...06-deploying...05-predict-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-5910bfb1-5cf0-418f-91e6-ce23cac12861` | `7bc4aed` | Source-faithful `22.2` and `3.2106109757442027`; pending re-review |
| DE `03-data-warehouse/...06-deploying...06-predict-payment-type-2-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-6f78721d-85fa-48db-b391-e2e07183c9e6` | `7bc4aed` | Source-faithful `payment_type: 2` and low prediction; pending re-review |
| DE `06-batch/...14-spark-master-ui-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-15db5616-00b0-435c-9162-5deda61971bc` | `6dda8d7` | Full zero-worker UI restored; accepted in first independent review |
| DE `06-batch/...15-create-cluster-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-40d5c175-273e-4732-930c-2c7c908dfb24` | `6dda8d7` | Jupyter/Docker selections preserved; accepted in first independent review |
| DE `06-batch/...16-failed-to-find-bigquery-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-d40960f4-cd15-4bc8-8d89-6965940483bd` | `6dda8d7` | Error meaning preserved; accepted in first independent review |
| DE `06-batch/...04-first-look-at-spark-01-spark-ui-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-5c2e2ff3-61c3-41c8-9867-2473a3e1930c` | `62e6c24` | Crisp zero-job Spark UI; pending independent review |
| DE `06-batch/...04-first-look-at-spark-02-schema-problem-pandas-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-43903919-e160-4c72-9c29-8d315d2444e7` | `62e6c24` | Crisp notebook/schema evidence; pending independent review |
| DE `06-batch/...04-first-look-at-spark-03-schema-structtype-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-99181745-370a-4b82-9fa7-addcc89c36a6` | `62e6c24` | Crisp exact schema code; pending independent review |
| DE `06-batch/...03-installing-spark-01-install-guide-java-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-603231f7-f547-4abc-908f-b7aeb0128150` | `ae96d44` | Crisp documentation page; pending independent review |
| DE `06-batch/...03-installing-spark-02-java-home-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-85605ad3-9fb3-4efb-bb6f-a7cd7c034e4e` | `ae96d44` | Crisp terminal; pending independent review |
| DE `06-batch/...03-installing-spark-03-spark-download-page-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-abe2821c-e83c-41c7-ae57-fef24cfcece6` | `ae96d44` | Release `3.0.3` preserved; pending independent review |
| DE `06-batch/...03-installing-spark-04-spark-home-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-1f93b0df-2f4f-4d23-9906-15cb4f5d7efe` | `d6f1822` | Crisp terminal; pending independent review |
| DE `06-batch/...03-installing-spark-05-spark-shell-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-35984590-455f-43c3-ae19-29278a56d998` | `d6f1822` | Spark 3.0.3 and final range output preserved; pending independent review |
| ML `02-regression/...04-fake-feature-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-37de99a4-c2b2-4abc-aa23-4411e9922fb5` | `095d0dc` | Crisp vectors and relation; accepted in first independent review |
| ML `02-regression/...05-prepend-one-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-c69bfbe7-36bf-42e8-a4fb-53bc18d268a6` | `b72735e` | Corrected to `return dot(xi, w_new)`; pending re-review |

The generated files remain in the local imagegen output directory named in
each tool result. The course repository contains only the copied published
target; the original source and crop remain alongside it for auditability.
