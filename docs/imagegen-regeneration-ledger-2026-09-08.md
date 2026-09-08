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
| DE `06-batch/...05-spark-dataframes-01-print-schema-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-6074c3bc-7846-4c7e-a70d-fb9911251533` | `1854c0d` | Crisp parquet schema output; pending independent review |
| DE `06-batch/...05-spark-dataframes-02-select-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-be2c27f0-4c94-446f-9c67-c933ea41ff7a` | `1854c0d` | Crisp four-column selection output; pending independent review |
| DE `06-batch/...05-spark-dataframes-03-built-in-functions-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-58db4808-795a-456e-b9f1-93a44629ab01` | `1854c0d` | Crisp `F.to*` autocomplete and output; pending independent review |
| DE `06-batch/...05-spark-dataframes-04-udf-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-79e5f330-b8a8-43f4-aa5c-991588b3e548` | `1854c0d` | Crisp UDF/output state; pending independent review |
| DE `06-batch/...06-preparing-taxi-data-04-zcat-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-042d8125-d3bc-44ed-9d32-6549de7883bb` | `339894f` | Regenerated after rejecting `mta_amax`; final header uses exact `mta_tax`; pending review |
| DE `06-batch/...06-preparing-taxi-data-05-tree-raw-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-71e452e0-6ac1-4eac-ad60-7d809179a103` | `339894f` | Crisp raw-data hierarchy; pending independent review |
| DE `06-batch/...06-preparing-taxi-data-06-schema-strings-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-40080e39-799b-448c-822a-c1bc4d64d237` | `339894f` | Crisp all-StringType schema state; pending independent review |
| DE `06-batch/...06-preparing-taxi-data-07-spark-ui-one-task-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-e1c604db-610d-40b2-b9ea-e880a79dc858` | `339894f` | Crisp 1-active/22-completed job state; pending independent review |
| DE `06-batch/...06-preparing-taxi-data-08-tree-pq-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-8e300c2f-999d-41ff-a268-93010a7ae20e` | `339894f` | Crisp parquet tree and `_SUCCESS` markers; pending independent review |
| DE `06-batch/...03-installing-spark-01-install-guide-java-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-603231f7-f547-4abc-908f-b7aeb0128150` | `ae96d44` | Crisp documentation page; pending independent review |
| DE `06-batch/...03-installing-spark-02-java-home-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-85605ad3-9fb3-4efb-bb6f-a7cd7c034e4e` | `ae96d44` | Crisp terminal; pending independent review |
| DE `06-batch/...03-installing-spark-03-spark-download-page-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-abe2821c-e83c-41c7-ae57-fef24cfcece6` | `ae96d44` | Release `3.0.3` preserved; pending independent review |
| DE `06-batch/...03-installing-spark-04-spark-home-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-1f93b0df-2f4f-4d23-9906-15cb4f5d7efe` | `d6f1822` | Crisp terminal; pending independent review |
| DE `06-batch/...03-installing-spark-05-spark-shell-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-35984590-455f-43c3-ae19-29278a56d998` | `d6f1822` | Spark 3.0.3 and final range output preserved; pending independent review |
| DE `06-batch/...07-sql-with-spark-01-read-parquet-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-b4eb4e1b-459d-4aab-87bb-25b3e1b95fb8` | `0904e57` | Regenerated without webcam/browser chrome; accepted by independent review |
| DE `06-batch/...07-sql-with-spark-02-common-columns-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-22e6d1d9-7c12-4415-8608-ff4d68bd6de7` | `0904e57` | Regenerated without webcam/browser chrome; accepted by independent review |
| DE `06-batch/...09-groupby-in-spark-02-three-stages-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-3fdc8c80-a6d9-4d4a-9dc3-46a2fc0649ae` | `fae367c` | Regenerated as a sharp DAG; accepted by independent review |
| DE `06-batch/...09-groupby-in-spark-04-shuffle-read-write-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-9fcc0df1-670e-4587-8e4a-6f5cc16b5281` | `d58916e` | Regenerated as a sharp stage table; task counts and `425.1 MiB` checked; accepted by independent review |
| DE `06-batch/...10-joins-in-spark-02-sort-merge-join-stages-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-e43a56e5-47ba-4e64-bff9-6624e9fa0b55` | `64d18b2` | Follow-up generation restored `WholeStageCodegen (5)`; accepted by independent re-review |
| DE `06-batch/...10-joins-in-spark-04-broadcast-exchange-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-645af126-0ce5-48ca-826c-7f6e9d611f7c` | `f66a710`, `eeb478e`, `bdacd32` | Imagegen base regenerated without webcam; exact `$anonfun$withThreadLocalCaptured$1` labels restored deterministically after imagegen rendered the leading `$` as `S`; independent review pending |
| DE `06-batch/...11-operations-on-spark-rdds-06-dag-two-stages-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-fdb4e6dc-503a-418f-b290-d0f33ad4bec3` | `63927e9` | Regenerated skipped/active RDD DAG; accepted by independent review |
| DE `06-batch/...12-spark-rdd-mappartition-02-feature-columns-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-4ec4adcf-e874-48a6-9c77-1615400d3695` | `aff59ee` | Regenerated feature selection output; accepted by independent review |
| DE `06-batch/...14-creating-a-local-spark-cluster-02-worker-registered-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-0db64305-9e64-4760-8f82-c61e6aaa26d3` | `0806220` | Regenerated worker `ALIVE` UI and resource rows; accepted by independent review |
| DE `06-batch/...15-setting-up-a-dataproc-cluster-02-submit-job-form-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-74c19585-1af4-4137-8500-b047d5c9b610` | `16b4254` | Regenerated exact green/yellow/report arguments; accepted by independent review |
| DE `06-batch/...15-setting-up-a-dataproc-cluster-05-reports-in-bucket-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-3511bef5-af63-4b99-b8a9-ed679d96d569` | `d2432e1` | Regenerated exact `code/`, `pq/`, `report-2020/`, `report-2021/` folders; accepted by independent review |
| ML `02-regression/...04-fake-feature-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-37de99a4-c2b2-4abc-aa23-4411e9922fb5` | `095d0dc` | Crisp vectors and relation; accepted in first independent review |
| ML `02-regression/...05-prepend-one-crisp.png` | matching `.jpg` + `-cropped.png` | `exec-c69bfbe7-36bf-42e8-a4fb-53bc18d268a6` | `b72735e` | Corrected to `return dot(xi, w_new)`; pending re-review |
| ML `08-deep-learning/...03-pretrained-models-01-keras-applications-crisp.png` | `...03-pretrained-models-01-keras-applications.jpg` + `...-cropped.png` | `exec-edccde7f-fb54-4705-b0be-61a4a690de3f` | `7e22144` | Regenerated without browser/camera chrome; exact heading, prose, and visible table values checked; independent review pending |
| ML `08-deep-learning/...11-large-model-05-training-output-crisp.png` | `...11-large-model-05-training-output.jpg` + `...-cropped.png` | `exec-251c1793-18ba-4c10-9e27-be50e305d3cd` | `0f00823` | Regenerated on a wide canvas without notebook/camera chrome; epoch metrics and heading checked line-by-line; independent review pending |

The generated files remain in the local imagegen output directory named in
each tool result. The course repository contains only the copied published
target; the original source and crop remain alongside it for auditability.

## Source-of-truth conflict recorded

The original frame for
`06-batch/...04-first-look-at-spark-03-schema-structtype-crisp.png` shows the
earlier inferred schema (`StringType`, `LongType`, and `DoubleType`), while the
lesson section and its explicit `StructType` code specify timestamps, integer
IDs, and nullable `SR_Flag` as `StringType`. The regenerated target follows
the current lesson code and caption rather than reproducing the contradictory
old frame. This is a semantic correction that requires reviewer confirmation;
it is not evidence that the old screenshot was faithfully regenerated.
