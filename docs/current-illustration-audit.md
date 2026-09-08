# Current illustration audit

Generated on **2026-09-08** by the read-only audit script.

This is a committed snapshot of the four current Zoomcamp scopes. The script reads the course repositories but does not modify them.

## Source snapshots

| Scope | Repository | HEAD | Worktree | Active selection |
| --- | --- | --- | --- | --- |
| ML | `/home/alexey/git/machine-learning-zoomcamp` | `ff3733fde98aeaa7be323da3bcf45a7ac741c978` | clean | the published 2026 cohort flow and its module manifests |
| LLM | `/home/alexey/git/llm-zoomcamp` | `c557a0a05e27b710014f32e7533f96454b2dc51f` | clean | the published 2026 cohort flow and its module manifests |
| MLOps | `/home/alexey/git/mlops-zoomcamp` | `42a1b0d5f448949f7aa2f25d8f3046045d9975bc` | clean | numbered root module/project README pages; no published cohort manifest exists |
| DE | `/home/alexey/git/data-engineering-zoomcamp` | `bdacd32b83ca2347e764c3c73ce3c3287348cf98` | dirty (snapshot still read-only) | the current 2027 draft cohort and its module manifests; historical cohorts excluded |

## Status contract

- `PASS` means the local Markdown target resolves and a basic raster/vector dimension check succeeded.
- `MISSING`/`OUTSIDE` is an actionable broken reference; `REMOTE` is recorded but not locally checked; `DECODE?` needs an image decoder check.
- `review required` is intentional: filesystem checks cannot prove crop direction/order, visual crispness at lesson size, text or semantic fidelity, or overlay removal. An independent reviewer must record the visual verdict before publishing.
- Completed visual-review evidence is recorded in [`docs/visual-review-evidence-2026-09-08.md`](visual-review-evidence-2026-09-08.md); this scanner's queue remains conservative and is not a substitute for that evidence.
- Thumbnail and homework/support assets are reference-checked but are not counted as instructional illustrations in the unit list.

## Scope summary

| Scope | State | Active units | Illustration coverage | Image references | Visual review queue | Broken refs |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| ML | `published current cohort` | 105 | 86 present / 19 missing | 317 (314 local) | 307 visual reviews required | 0 missing/outside |
| LLM | `published current cohort` | 72 | 36 present / 36 missing | 38 (38 local) | 38 visual reviews required | 0 missing/outside |
| MLOps | `current self-paced curriculum` | 7 | 5 present / 2 missing | 38 (37 local) | 31 visual reviews required | 0 missing/outside |
| DE | `current draft; unpublished` | 88 | 19 present / 69 missing | 61 (61 local) | 61 visual reviews required | 0 missing/outside |

## Active units

Every row is in the selected active scope. `YES` means at least one resolving local instructional illustration reference; navigation thumbnails and homework checklists do not satisfy that column.

| Scope | Module | Unit | Unit file | Illustration present/missing | Instructional refs | All local/remote image refs |
| --- | --- | --- | --- | --- | ---: | ---: |
| ML | `cohorts/2026/01-intro` | Introduction to Machine Learning | `cohorts/2026/01-intro/01-what-is-ml.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/01-intro` | ML vs Rule-Based Systems | `cohorts/2026/01-intro/02-ml-vs-rules.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/01-intro` | Supervised Machine Learning | `cohorts/2026/01-intro/03-supervised-ml.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/01-intro` | CRISP-DM | `cohorts/2026/01-intro/04-crisp-dm.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/01-intro` | Model Selection Process | `cohorts/2026/01-intro/05-model-selection.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/01-intro` | Setting up the Environment | `cohorts/2026/01-intro/06-environment.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/01-intro` | Introduction to NumPy | `cohorts/2026/01-intro/07-numpy.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/01-intro` | Linear Algebra Refresher | `cohorts/2026/01-intro/08-linear-algebra.md` | **YES** | 2 | 2 |
| ML | `cohorts/2026/01-intro` | Introduction to Pandas | `cohorts/2026/01-intro/09-pandas.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/01-intro` | Summary | `cohorts/2026/01-intro/10-summary.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/02-regression` | Car price prediction project | `cohorts/2026/02-regression/01-car-price-intro.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/02-regression` | Data preparation | `cohorts/2026/02-regression/02-data-preparation.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/02-regression` | Exploratory data analysis | `cohorts/2026/02-regression/03-eda.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/02-regression` | Setting up the validation framework | `cohorts/2026/02-regression/04-validation-framework.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/02-regression` | Linear regression | `cohorts/2026/02-regression/05-linear-regression-simple.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/02-regression` | Linear regression: vector form | `cohorts/2026/02-regression/06-linear-regression-vector.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/02-regression` | Training linear regression: Normal equation | `cohorts/2026/02-regression/07-linear-regression-training.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/02-regression` | Baseline model for car price prediction project | `cohorts/2026/02-regression/08-baseline-model.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/02-regression` | Root Mean Squared Error (RMSE) | `cohorts/2026/02-regression/09-rmse.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/02-regression` | Computing RMSE on validation data | `cohorts/2026/02-regression/10-car-price-validation.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/02-regression` | Feature engineering | `cohorts/2026/02-regression/11-feature-engineering.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/02-regression` | Categorical variables | `cohorts/2026/02-regression/12-categorical-variables.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/02-regression` | Regularization | `cohorts/2026/02-regression/13-regularization.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/02-regression` | Tuning the model | `cohorts/2026/02-regression/14-tuning-model.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/02-regression` | Using the model | `cohorts/2026/02-regression/15-using-model.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/02-regression` | Car price prediction project summary | `cohorts/2026/02-regression/16-summary.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/02-regression` | Explore more | `cohorts/2026/02-regression/17-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Churn prediction project | `cohorts/2026/03-classification/01-churn-project.md` | **YES** | 2 | 2 |
| ML | `cohorts/2026/03-classification` | Data preparation | `cohorts/2026/03-classification/02-data-preparation.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/03-classification` | Setting up the validation framework | `cohorts/2026/03-classification/03-validation.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | EDA | `cohorts/2026/03-classification/04-eda.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/03-classification` | Feature importance: Churn rate and risk ratio | `cohorts/2026/03-classification/05-risk.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Feature importance: Mutual information | `cohorts/2026/03-classification/06-mutual-info.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Feature importance: Correlation | `cohorts/2026/03-classification/07-correlation.md` | **YES** | 2 | 4 |
| ML | `cohorts/2026/03-classification` | One-hot encoding | `cohorts/2026/03-classification/08-ohe.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Logistic regression | `cohorts/2026/03-classification/09-logistic-regression.md` | **YES** | 1 | 4 |
| ML | `cohorts/2026/03-classification` | Training logistic regression with Scikit-Learn | `cohorts/2026/03-classification/10-training-log-reg.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/03-classification` | Model interpretation | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Using the model | `cohorts/2026/03-classification/12-using-log-reg.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Summary | `cohorts/2026/03-classification/13-summary.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Explore more | `cohorts/2026/03-classification/14-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/04-evaluation` | Evaluation metrics: session overview | `cohorts/2026/04-evaluation/01-overview.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/04-evaluation` | Accuracy and dummy model | `cohorts/2026/04-evaluation/02-accuracy.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/04-evaluation` | Confusion table | `cohorts/2026/04-evaluation/03-confusion-table.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/04-evaluation` | Precision and Recall | `cohorts/2026/04-evaluation/04-precision-recall.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/04-evaluation` | ROC Curves | `cohorts/2026/04-evaluation/05-roc.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/04-evaluation` | ROC AUC | `cohorts/2026/04-evaluation/06-auc.md` | **YES** | 2 | 2 |
| ML | `cohorts/2026/04-evaluation` | Cross-Validation | `cohorts/2026/04-evaluation/07-cross-validation.md` | **MISSING** | 0 | 1 |
| ML | `cohorts/2026/04-evaluation` | Summary | `cohorts/2026/04-evaluation/08-summary.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/04-evaluation` | Explore more | `cohorts/2026/04-evaluation/09-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/05-deployment` | Intro / Session overview | `cohorts/2026/05-deployment/01-intro.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/05-deployment` | Saving and loading the model | `cohorts/2026/05-deployment/02-pickle.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/05-deployment` | Web services: introduction to Flask | `cohorts/2026/05-deployment/03-flask-intro.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/05-deployment` | Serving the churn model with Flask | `cohorts/2026/05-deployment/04-flask-deployment.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/05-deployment` | Python virtual environment: Pipenv | `cohorts/2026/05-deployment/05-pipenv.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/05-deployment` | Environment management: Docker | `cohorts/2026/05-deployment/06-docker.md` | **YES** | 2 | 2 |
| ML | `cohorts/2026/05-deployment` | Deployment to the cloud: AWS Elastic Beanstalk (optional) | `cohorts/2026/05-deployment/07-aws-eb.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/05-deployment` | Summary | `cohorts/2026/05-deployment/08-summary.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/05-deployment` | Explore more | `cohorts/2026/05-deployment/09-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/06-trees` | Credit risk scoring project | `cohorts/2026/06-trees/01-credit-risk.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/06-trees` | Data cleaning and preparation | `cohorts/2026/06-trees/02-data-prep.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/06-trees` | Decision trees | `cohorts/2026/06-trees/03-decision-trees.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/06-trees` | Decision tree learning algorithm | `cohorts/2026/06-trees/04-decision-tree-learning.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/06-trees` | Decision trees parameter tuning | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | **YES** | 2 | 2 |
| ML | `cohorts/2026/06-trees` | Ensemble learning and random forest | `cohorts/2026/06-trees/06-random-forest.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/06-trees` | Gradient boosting and XGBoost | `cohorts/2026/06-trees/07-boosting.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/06-trees` | XGBoost parameter tuning | `cohorts/2026/06-trees/08-xgb-tuning.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/06-trees` | Selecting the best model | `cohorts/2026/06-trees/09-final-model.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/06-trees` | Summary | `cohorts/2026/06-trees/10-summary.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/06-trees` | Explore more | `cohorts/2026/06-trees/11-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/08-deep-learning` | Fashion classification | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/08-deep-learning` | TensorFlow and Keras | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/08-deep-learning` | Pre-trained convolutional neural networks | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/08-deep-learning` | Convolutional neural networks | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | **YES** | 8 | 11 |
| ML | `cohorts/2026/08-deep-learning` | Transfer learning | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/08-deep-learning` | Adjusting the learning rate | `cohorts/2026/08-deep-learning/06-learning-rate.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/08-deep-learning` | Checkpointing | `cohorts/2026/08-deep-learning/07-checkpointing.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/08-deep-learning` | Adding more layers | `cohorts/2026/08-deep-learning/08-more-layers.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/08-deep-learning` | Regularization and dropout | `cohorts/2026/08-deep-learning/09-dropout.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/08-deep-learning` | Data augmentation | `cohorts/2026/08-deep-learning/10-augmentation.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/08-deep-learning` | Training a larger model | `cohorts/2026/08-deep-learning/11-large-model.md` | **MISSING** | 0 | 0 |
| ML | `cohorts/2026/08-deep-learning` | Using the model | `cohorts/2026/08-deep-learning/12-using-model.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/08-deep-learning` | Summary | `cohorts/2026/08-deep-learning/13-summary.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/08-deep-learning` | Explore more | `cohorts/2026/08-deep-learning/14-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/08-deep-learning` | Installation of TensorFlow | `cohorts/2026/08-deep-learning/install.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/09-serverless` | Introduction to Serverless | `cohorts/2026/09-serverless/01-intro.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/09-serverless` | AWS Lambda | `cohorts/2026/09-serverless/02-aws-lambda.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/09-serverless` | TensorFlow Lite | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/09-serverless` | Preparing the code for Lambda | `cohorts/2026/09-serverless/04-preparing-code.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/09-serverless` | Preparing a Docker image | `cohorts/2026/09-serverless/05-docker-image.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/09-serverless` | Creating the lambda function | `cohorts/2026/09-serverless/06-creating-lambda.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/09-serverless` | API Gateway: exposing the lambda function | `cohorts/2026/09-serverless/07-api-gateway.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/09-serverless` | Summary | `cohorts/2026/09-serverless/08-summary.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/09-serverless` | Explore more | `cohorts/2026/09-serverless/09-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/09-serverless` | Python 3.12 vs TF Lite 2.17 | `cohorts/2026/09-serverless/updates.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/10-kubernetes` | Overview | `cohorts/2026/10-kubernetes/01-overview.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/10-kubernetes` | TensorFlow Serving | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/10-kubernetes` | Creating a pre-processing service | `cohorts/2026/10-kubernetes/03-preprocessing.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/10-kubernetes` | Running everything locally with Docker-compose | `cohorts/2026/10-kubernetes/04-docker-compose.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/10-kubernetes` | Introduction to Kubernetes | `cohorts/2026/10-kubernetes/05-kubernetes-intro.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/10-kubernetes` | Deploying a simple service to Kubernetes | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/10-kubernetes` | Deploying TensorFlow models to Kubernetes | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/10-kubernetes` | Deploying to EKS | `cohorts/2026/10-kubernetes/08-eks.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/10-kubernetes` | Summary | `cohorts/2026/10-kubernetes/09-summary.md` | **YES** | 2 | 2 |
| ML | `cohorts/2026/10-kubernetes` | Explore more | `cohorts/2026/10-kubernetes/10-explore-more.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | Introduction | `cohorts/2026/01-agentic-rag/01-intro.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | Environment | `cohorts/2026/01-agentic-rag/02-environment.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | RAG | `cohorts/2026/01-agentic-rag/03-rag.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | The Course FAQ Dataset | `cohorts/2026/01-agentic-rag/04-dataset.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | Search | `cohorts/2026/01-agentic-rag/05-search.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | Building the Prompt | `cohorts/2026/01-agentic-rag/06-building-prompt.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | The LLM | `cohorts/2026/01-agentic-rag/07-llm.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | RAG Helper | `cohorts/2026/01-agentic-rag/08-rag-helper.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | Data Ingestion | `cohorts/2026/01-agentic-rag/09-data-ingestion.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | Wrap-up of Part 1 | `cohorts/2026/01-agentic-rag/10-rag-next-steps.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | Agents | `cohorts/2026/01-agentic-rag/11-agents-intro.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | Quick RAG Revision (Optional) | `cohorts/2026/01-agentic-rag/12-rag-revision.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/01-agentic-rag` | Function Calling | `cohorts/2026/01-agentic-rag/13-function-calling.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | The Agentic Loop | `cohorts/2026/01-agentic-rag/14-agentic-loop.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | ToyAIKit | `cohorts/2026/01-agentic-rag/15-frameworks.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/01-agentic-rag` | Other Frameworks | `cohorts/2026/01-agentic-rag/16-other-frameworks.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/02-vector-search` | Vector Search | `cohorts/2026/02-vector-search/01-intro.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/02-vector-search` | Embeddings | `cohorts/2026/02-vector-search/02-embeddings.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/02-vector-search` | Embedding Our Dataset | `cohorts/2026/02-vector-search/03-embeddings-dataset.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/02-vector-search` | Vector Search | `cohorts/2026/02-vector-search/04-vector-search.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/02-vector-search` | Vector Search with minsearch | `cohorts/2026/02-vector-search/05-minsearch-vector.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/02-vector-search` | RAG with Vector Search | `cohorts/2026/02-vector-search/06-rag-vector.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/02-vector-search` | Vector Search with sqlitesearch | `cohorts/2026/02-vector-search/07-sqlitesearch-vector.md` | **YES** | 2 | 2 |
| LLM | `cohorts/2026/02-vector-search` | Vector Search with PGVector | `cohorts/2026/02-vector-search/08-pgvector.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/02-vector-search` | Using ONNX Runtime instead of PyTorch | `cohorts/2026/02-vector-search/09-onnx-embedder.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/02-vector-search` | Next Steps | `cohorts/2026/02-vector-search/10-next-steps.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/03-orchestration` | AI Orchestration | `cohorts/2026/03-orchestration/01-intro.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/03-orchestration` | Context Engineering | `cohorts/2026/03-orchestration/02-context-engineering.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/03-orchestration` | Setting up Kestra | `cohorts/2026/03-orchestration/03-setup.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/03-orchestration` | AI Copilot | `cohorts/2026/03-orchestration/04-ai-copilot.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/03-orchestration` | Retrieval Augmented Generation | `cohorts/2026/03-orchestration/05-rag.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/03-orchestration` | AI Agents | `cohorts/2026/03-orchestration/06-agents.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/03-orchestration` | Multi-Agent Systems | `cohorts/2026/03-orchestration/07-multi-agent.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/03-orchestration` | Best Practices | `cohorts/2026/03-orchestration/08-best-practices.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/03-orchestration` | Next Steps | `cohorts/2026/03-orchestration/09-next-steps.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/04-evaluation` | Evaluation | `cohorts/2026/04-evaluation/01-intro.md` | **YES** | 2 | 2 |
| LLM | `cohorts/2026/04-evaluation` | Generating Ground Truth Data | `cohorts/2026/04-evaluation/02-ground-truth.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/04-evaluation` | Generating Ground Truth for All Documents | `cohorts/2026/04-evaluation/03-ground-truth-batch.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/04-evaluation` | Search Evaluation | `cohorts/2026/04-evaluation/04-search-evaluation.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/04-evaluation` | Search Evaluation Metrics | `cohorts/2026/04-evaluation/05-search-metrics.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/04-evaluation` | Search Parameter Tuning | `cohorts/2026/04-evaluation/06-search-tuning.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/04-evaluation` | RAG and Agent Evaluation | `cohorts/2026/04-evaluation/11-evaluation-intro.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/04-evaluation` | Generating RAG Answers | `cohorts/2026/04-evaluation/12-rag-answers.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/04-evaluation` | LLM as a Judge | `cohorts/2026/04-evaluation/13-llm-as-judge.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/04-evaluation` | Agent Evaluation | `cohorts/2026/04-evaluation/14-agent-evaluation.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/04-evaluation` | Next Steps | `cohorts/2026/04-evaluation/15-next-steps.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/05-monitoring` | Monitoring | `cohorts/2026/05-monitoring/01-intro.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Assistant | `cohorts/2026/05-monitoring/02-assistant-setup.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Chat App | `cohorts/2026/05-monitoring/03-chat-app.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Capturing Metrics | `cohorts/2026/05-monitoring/04-metrics.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Storing Data in PostgreSQL | `cohorts/2026/05-monitoring/05-database.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Querying Data | `cohorts/2026/05-monitoring/06-querying.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Streamlit Dashboard | `cohorts/2026/05-monitoring/07-streamlit-dashboard.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | User Feedback | `cohorts/2026/05-monitoring/08-user-feedback.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Built-in Judge | `cohorts/2026/05-monitoring/09-built-in-judge.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Feedback Dashboard | `cohorts/2026/05-monitoring/10-feedback-dashboard.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/05-monitoring` | Synthetic Data Generation | `cohorts/2026/05-monitoring/11-synthetic-data.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/05-monitoring` | Grafana Dashboards | `cohorts/2026/05-monitoring/12-grafana.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/05-monitoring` | Docker Compose | `cohorts/2026/05-monitoring/13-docker-compose.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/05-monitoring` | Next Steps | `cohorts/2026/05-monitoring/14-next-steps.md` | **MISSING** | 0 | 0 |
| LLM | `cohorts/2026/06-best-practices` | Best Practices for RAG | `cohorts/2026/06-best-practices/01-intro.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/06-best-practices` | Hybrid Search | `cohorts/2026/06-best-practices/02-hybrid-search.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/06-best-practices` | Document Reranking | `cohorts/2026/06-best-practices/03-reranking.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/06-best-practices` | Hybrid Search with LangChain | `cohorts/2026/06-best-practices/04-langchain.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/06-best-practices` | Next Steps | `cohorts/2026/06-best-practices/05-next-steps.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/07-project-example` | End-to-End Project Example | `cohorts/2026/07-project-example/01-intro.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/07-project-example` | Evaluating Retrieval | `cohorts/2026/07-project-example/02-evaluating-retrieval.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/07-project-example` | Evaluating RAG | `cohorts/2026/07-project-example/03-evaluating-rag.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/07-project-example` | Interface and Ingestion Pipeline | `cohorts/2026/07-project-example/04-interface.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/07-project-example` | Monitoring and Containerization | `cohorts/2026/07-project-example/05-monitoring.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/07-project-example` | Summary and Closing Remarks | `cohorts/2026/07-project-example/06-summary.md` | **YES** | 1 | 1 |
| LLM | `cohorts/2026/07-project-example` | Chunking for Longer Texts | `cohorts/2026/07-project-example/07-chunking.md` | **YES** | 1 | 1 |
| MLOps | `01-intro` | 1. Introduction | `01-intro/README.md` | **YES** | 6 | 6 |
| MLOps | `02-experiment-tracking` | 2. Experiment tracking and model management | `02-experiment-tracking/README.md` | **YES** | 7 | 7 |
| MLOps | `03-orchestration` | 3. Orchestration and ML Pipelines | `03-orchestration/README.md` | **YES** | 3 | 3 |
| MLOps | `04-deployment` | 4. Model Deployment | `04-deployment/README.md` | **YES** | 6 | 6 |
| MLOps | `05-monitoring` | 5. Model Monitoring | `05-monitoring/README.md` | **YES** | 9 | 9 |
| MLOps | `06-best-practices` | 6. Best Practices | `06-best-practices/README.md` | **MISSING** | 0 | 2 |
| MLOps | `07-project` | 07-project | `07-project/README.md` | **MISSING** | 0 | 1 |
| DE | `cohorts/2027/01-docker-terraform` | Introduction to Docker | `cohorts/2027/01-docker-terraform/01-introduction.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Virtual Environments and Data Pipelines | `cohorts/2027/01-docker-terraform/02-virtual-environment.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Dockerizing the Pipeline | `cohorts/2027/01-docker-terraform/03-dockerizing-pipeline.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Running PostgreSQL with Docker | `cohorts/2027/01-docker-terraform/04-postgres-docker.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | NY Taxi Dataset and Data Ingestion | `cohorts/2027/01-docker-terraform/05-data-ingestion.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Creating the Data Ingestion Script | `cohorts/2027/01-docker-terraform/06-ingestion-script.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | pgAdmin - Database Management Tool | `cohorts/2027/01-docker-terraform/07-pgadmin.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Dockerizing the Ingestion Script | `cohorts/2027/01-docker-terraform/08-dockerizing-ingestion.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Docker Compose | `cohorts/2027/01-docker-terraform/09-docker-compose.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | SQL Refresher | `cohorts/2027/01-docker-terraform/10-sql-refresher.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Cleanup | `cohorts/2027/01-docker-terraform/11-cleanup.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | Terraform Overview | `cohorts/2027/01-docker-terraform/12-terraform-overview.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/01-docker-terraform` | GCP Overview | `cohorts/2027/01-docker-terraform/13-gcp-overview.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | What is Workflow Orchestration? | `cohorts/2027/02-workflow-orchestration/01-what-is-workflow-orchestration.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | What is Kestra? | `cohorts/2027/02-workflow-orchestration/02-what-is-kestra.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Installing Kestra | `cohorts/2027/02-workflow-orchestration/03-installing-kestra.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Kestra Concepts | `cohorts/2027/02-workflow-orchestration/04-kestra-concepts.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Orchestrate Python Code | `cohorts/2027/02-workflow-orchestration/05-orchestrate-python-code.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Getting Started Pipeline | `cohorts/2027/02-workflow-orchestration/06-getting-started-pipeline.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Local DB: Load Taxi Data to Postgres | `cohorts/2027/02-workflow-orchestration/07-load-taxi-data-to-postgres.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Local DB: Learn Scheduling and Backfills | `cohorts/2027/02-workflow-orchestration/08-scheduling-and-backfills.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | ETL vs ELT | `cohorts/2027/02-workflow-orchestration/09-etl-vs-elt.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Setup Google Cloud Platform (GCP) | `cohorts/2027/02-workflow-orchestration/10-setup-google-cloud-platform.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | GCP Workflow: Load Taxi Data to BigQuery | `cohorts/2027/02-workflow-orchestration/11-load-taxi-data-to-bigquery.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | GCP Workflow: Schedule and Backfill Full Dataset | `cohorts/2027/02-workflow-orchestration/12-schedule-and-backfill-full-dataset.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Introduction: Why AI for Workflows? | `cohorts/2027/02-workflow-orchestration/13-why-ai-for-workflows.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Context Engineering with ChatGPT | `cohorts/2027/02-workflow-orchestration/14-context-engineering-with-chatgpt.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | AI Copilot in Kestra | `cohorts/2027/02-workflow-orchestration/15-ai-copilot-in-kestra.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Bonus: Retrieval Augmented Generation (RAG) | `cohorts/2027/02-workflow-orchestration/16-retrieval-augmented-generation.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Bonus: Deploy to the Cloud (Optional) | `cohorts/2027/02-workflow-orchestration/17-deploy-to-the-cloud.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/02-workflow-orchestration` | Additional Resources | `cohorts/2027/02-workflow-orchestration/18-additional-resources.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/03-data-warehouse` | Data Warehouse and BigQuery | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | **YES** | 6 | 6 |
| DE | `cohorts/2027/03-data-warehouse` | Partitioning vs Clustering | `cohorts/2027/03-data-warehouse/02-partitioning-vs-clustering.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/03-data-warehouse` | BigQuery Best Practices | `cohorts/2027/03-data-warehouse/03-bigquery-best-practices.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/03-data-warehouse` | Internals of BigQuery | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/03-data-warehouse` | Machine Learning in BigQuery | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | **YES** | 1 | 1 |
| DE | `cohorts/2027/03-data-warehouse` | Deploying a Machine Learning Model from BigQuery | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | **YES** | 6 | 6 |
| DE | `cohorts/2027/04-analytics-engineering` | Analytics Engineering Basics | `cohorts/2027/04-analytics-engineering/01-analytics-engineering-basics.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | What is dbt? | `cohorts/2027/04-analytics-engineering/02-what-is-dbt.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Core vs dbt Cloud | `cohorts/2027/04-analytics-engineering/03-dbt-core-vs-dbt-cloud.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Project Structure | `cohorts/2027/04-analytics-engineering/04-dbt-project-structure.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Sources | `cohorts/2027/04-analytics-engineering/05-dbt-sources.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Models | `cohorts/2027/04-analytics-engineering/06-dbt-models.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Seeds and Macros | `cohorts/2027/04-analytics-engineering/07-dbt-seeds-and-macros.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | Documentation | `cohorts/2027/04-analytics-engineering/08-documentation.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Tests | `cohorts/2027/04-analytics-engineering/09-dbt-tests.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Packages | `cohorts/2027/04-analytics-engineering/10-dbt-packages.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/04-analytics-engineering` | dbt Commands | `cohorts/2027/04-analytics-engineering/11-dbt-commands.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Introduction to Bruin | `cohorts/2027/05-data-platforms/01-introduction.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Getting Started with Bruin | `cohorts/2027/05-data-platforms/02-getting-started.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Building an End-to-End Pipeline with NYC Taxi Data | `cohorts/2027/05-data-platforms/03-nyc-taxi-pipeline.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Using Bruin MCP with AI Agents | `cohorts/2027/05-data-platforms/04-bruin-mcp.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Deploying to Bruin Cloud | `cohorts/2027/05-data-platforms/05-bruin-cloud.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Core Concepts: Projects | `cohorts/2027/05-data-platforms/06-core-concepts-projects.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Core Concepts: Pipelines | `cohorts/2027/05-data-platforms/07-core-concepts-pipelines.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Core Concepts: Assets | `cohorts/2027/05-data-platforms/08-core-concepts-assets.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Core Concepts: Variables | `cohorts/2027/05-data-platforms/09-core-concepts-variables.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/05-data-platforms` | Core Concepts: Commands | `cohorts/2027/05-data-platforms/10-core-concepts-commands.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/06-batch` | Introduction to Batch Processing | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/06-batch` | Introduction to Spark | `cohorts/2027/06-batch/02-introduction-to-spark.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/06-batch` | Installing Spark | `cohorts/2027/06-batch/03-installing-spark.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/06-batch` | First Look at Spark/PySpark | `cohorts/2027/06-batch/04-first-look-at-spark.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | Spark DataFrames | `cohorts/2027/06-batch/05-spark-dataframes.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | Preparing Yellow and Green Taxi Data | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/06-batch` | SQL with Spark | `cohorts/2027/06-batch/07-sql-with-spark.md` | **YES** | 2 | 2 |
| DE | `cohorts/2027/06-batch` | Anatomy of a Spark Cluster | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | GroupBy in Spark | `cohorts/2027/06-batch/09-groupby-in-spark.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/06-batch` | Joins in Spark | `cohorts/2027/06-batch/10-joins-in-spark.md` | **YES** | 2 | 2 |
| DE | `cohorts/2027/06-batch` | Operations on Spark RDDs | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | **YES** | 2 | 2 |
| DE | `cohorts/2027/06-batch` | Spark RDD mapPartition | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | **YES** | 2 | 2 |
| DE | `cohorts/2027/06-batch` | Connecting to Google Cloud Storage | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/06-batch` | Creating a Local Spark Cluster | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | **YES** | 2 | 2 |
| DE | `cohorts/2027/06-batch` | Setting up a Dataproc Cluster | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/06-batch` | Connecting Spark to BigQuery | `cohorts/2027/06-batch/16-connecting-spark-to-bigquery.md` | **YES** | 1 | 1 |
| DE | `cohorts/2027/07-streaming` | PyFlink: Stream Processing Workshop | `cohorts/2027/07-streaming/01-introduction.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Redpanda - a Kafka-compatible broker | `cohorts/2027/07-streaming/02-redpanda.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Produce messages to Kafka | `cohorts/2027/07-streaming/03-produce-messages-to-kafka.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Consume messages with Python | `cohorts/2027/07-streaming/04-consume-messages-with-python.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Save events to PostgreSQL | `cohorts/2027/07-streaming/05-save-events-to-postgresql.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Why Flink? | `cohorts/2027/07-streaming/06-why-flink.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | The Flink image and services | `cohorts/2027/07-streaming/07-the-flink-image-and-services.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | The pass-through Flink job | `cohorts/2027/07-streaming/08-the-pass-through-flink-job.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Offsets - earliest vs latest | `cohorts/2027/07-streaming/09-offsets-earliest-vs-latest.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Aggregation with tumbling windows | `cohorts/2027/07-streaming/10-aggregation-with-tumbling-windows.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Late events and upserts | `cohorts/2027/07-streaming/11-late-events-and-upserts.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Understanding window types | `cohorts/2027/07-streaming/12-understanding-window-types.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Cleanup | `cohorts/2027/07-streaming/13-cleanup.md` | **MISSING** | 0 | 0 |
| DE | `cohorts/2027/07-streaming` | Q&A | `cohorts/2027/07-streaming/14-questions-and-answers.md` | **MISSING** | 0 | 0 |

## Active illustration references and quality/check status

This is the complete image-reference occurrence list for the selected unit files. Repeated references remain separate so the Markdown consumer is auditable.

| Scope | Unit | Line | Markdown target | Kind | Check | Dimensions | Quality status |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 14 | `images/01-what-is-ml-01-price-field-imagegen-pilot.png` | instructional illustration | PASS | 1645×956 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 33 | `images/01-what-is-ml-03-expert-or-model-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 49 | `images/01-what-is-ml-05-model-training-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 57 | `images/01-what-is-ml-06-using-model-imagegen-pilot.png` | instructional illustration | PASS | 1751×898 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 65 | `images/01-what-is-ml-07-suggest-price-imagegen-pilot.png` | instructional illustration | PASS | 1145×1374 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 14 | `images/02-ml-vs-rules-01-spam-examples-imagegen-pilot.png` | instructional illustration | PASS | 1626×967 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 28 | `images/02-ml-vs-rules-03-more-spam-imagegen-pilot.png` | instructional illustration | PASS | 1629×965 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 64 | `images/02-ml-vs-rules-05-encode-email-imagegen-pilot.png` | instructional illustration | PASS | 1628×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 88 | `images/02-ml-vs-rules-07-rule-based-summary-imagegen-pilot.png` | instructional illustration | PASS | 1770×889 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 92 | `images/02-ml-vs-rules-08-ml-summary-imagegen-pilot.png` | instructional illustration | PASS | 1537×1023 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 60 | `images/03-supervised-ml-04-regression-imagegen-pilot.png` | instructional illustration | PASS | 1698×926 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 73 | `images/03-supervised-ml-05-multiclass-imagegen-pilot.png` | instructional illustration | PASS | 1695×928 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 81 | `images/03-supervised-ml-06-ranking-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 93 | `images/03-supervised-ml-07-summary-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 25 | `images/04-crisp-dm-02-process-diagram-imagegen-pilot.png` | instructional illustration | PASS | 1628×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 31 | `images/04-crisp-dm-03-business-understanding-imagegen-pilot.png` | instructional illustration | PASS | 1628×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 62 | `images/04-crisp-dm-04-data-preparation-imagegen-pilot.png` | instructional illustration | PASS | 1693×929 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 20 | `images/05-model-selection-01-train-validation-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 43 | `images/05-model-selection-02-multiple-comparisons-imagegen-pilot.png` | instructional illustration | PASS | 1580×996 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 55 | `images/05-model-selection-03-train-valid-test-imagegen-pilot.png` | instructional illustration | PASS | 1619×971 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 67 | `images/05-model-selection-04-select-and-test-imagegen-pilot.png` | instructional illustration | PASS | 1693×929 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 23 | `images/06-environment-01-create-repo-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 27 | `images/06-environment-02-create-codespace-crisp.png` | instructional illustration | PASS | 1594×987 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 33 | `images/06-environment-03-vscode-desktop-crisp.png` | instructional illustration | PASS | 1508×1043 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 49 | `images/06-environment-04-push-pip-install-crisp.png` | instructional illustration | PASS | 1969×799 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 59 | `images/06-environment-05-jupyter-notebook-crisp.png` | instructional illustration | PASS | 1723×913 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 63 | `images/06-environment-06-homework-notebook-crisp.png` | homework/support | PASS | 1493×1054 | reference checked; non-illustration asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 65 | `images/08-linear-algebra-02-dot-product-crisp.png` | instructional illustration | PASS | 1665×945 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 116 | `images/08-linear-algebra-04-matrix-vector-idea-crisp.png` | instructional illustration | PASS | 1645×956 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 67 | `images/10-summary-04-supervised-g-x-y-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 73 | `images/10-summary-05-crisp-dm-bigger-picture-imagegen-pilot.png` | instructional illustration | PASS | 1254×1254 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 79 | `images/10-summary-06-model-selection-split-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 17 | `images/01-car-price-intro-01-select-best-price-crisp.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 26 | `images/01-car-price-intro-02-kaggle-dataset-crisp.png` | instructional illustration | PASS | 1857×847 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 31 | `images/01-car-price-intro-03-kaggle-data-explorer-crisp.png` | instructional illustration | PASS | 1790×879 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 39 | `images/01-car-price-intro-04-msrp-column-crisp.png` | instructional illustration | PASS | 1790×879 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 67 | `images/01-car-price-intro-06-github-repo-crisp.png` | instructional illustration | PASS | 1716×917 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 75 | `images/01-car-price-intro-07-chapter-files-crisp.png` | instructional illustration | PASS | 2170×725 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 99 | `images/03-eda-03-long-tail-distribution-crisp.png` | instructional illustration | PASS | 1888×833 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 120 | `images/03-eda-04-zoom-below-100k-crisp.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 181 | `images/03-eda-06-log1p-normal-distribution-crisp.png` | instructional illustration | PASS | 1870×841 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 25 | `images/04-validation-framework-01-train-val-test-split-crisp.png` | instructional illustration | PASS | 1611×976 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 18 | `images/06-linear-regression-vector-01-g-x-approx-y-crisp.png` | instructional illustration | PASS | 1386×1135 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 34 | `images/06-linear-regression-vector-02-dot-product-notation-crisp.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 75 | `images/06-linear-regression-vector-04-fake-feature-crisp.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 121 | `images/06-linear-regression-vector-06-matrix-vector-multiplication-crisp.png` | instructional illustration | PASS | 1570×1001 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 37 | `images/07-linear-regression-training-01-inverse-solution-crisp.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 59 | `images/07-linear-regression-training-02-gram-matrix-crisp.png` | instructional illustration | PASS | 1363×1154 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 79 | `images/07-linear-regression-training-03-normal-equation-crisp.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/08-baseline-model.md` | 128 | `images/08-baseline-model-06-prediction-histogram-crisp.png` | instructional illustration | PASS | 1561×1008 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/10-car-price-validation.md` | 22 | `images/10-car-price-validation-01-split-diagram-crisp.png` | instructional illustration | PASS | 1517×1037 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/11-feature-engineering.md` | 13 | `images/11-feature-engineering-01-feature-engineering-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 137 | `images/15-using-model-05-website-request-diagram-imagegen.png` | instructional illustration | PASS | 1521×1034 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/17-explore-more.md` | 4 | `images/17-explore-more-01-feature-experiments-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/01-churn-project.md` | 25 | `images/01-churn-project-01-churn-problem-crisp.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/01-churn-project.md` | 36 | `images/01-churn-project-02-binary-classification-crisp.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/03-validation.md` | 25 | `images/03-validation-01-train-val-test-split-crisp.png` | instructional illustration | PASS | 1509×1042 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/05-risk.md` | 109 | `images/05-risk-03-difference-vs-risk-ratio-imagegen-pilot.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/06-mutual-info.md` | 30 | `images/06-mutual-info-01-mutual-information-wikipedia-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 34 | `images/07-correlation-01-correlation-coefficient-imagegen-pilot.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 42 | `images/07-correlation-02-binary-target-imagegen-pilot.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 135 | `images/07-correlation-04-churn-rate-tenure-clean.png` | local image | PASS | 1617×973 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 168 | `images/07-correlation-05-churn-rate-monthly-charges-clean.png` | local image | PASS | 1774×887 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/08-ohe.md` | 52 | `images/08-ohe-01-one-hot-table-crisp.png` | instructional illustration | PASS | 1443×1090 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 33 | `images/09-logistic-regression-01-binary-classification-clean.png` | local image | PASS | 1617×973 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 57 | `images/09-logistic-regression-02-from-linear-to-logistic-clean.png` | local image | PASS | 1702×924 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 63 | `images/09-logistic-regression-03-sigmoid-formula-clean.png` | local image | PASS | 1617×973 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 98 | `images/09-logistic-regression-04-sigmoid-plot-crisp.png` | instructional illustration | PASS | 1488×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 183 | `images/11-log-reg-interpretation-06-second-example-imagegen.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/12-using-log-reg.md` | 124 | `images/12-using-log-reg-04-production-diagram-imagegen.png` | instructional illustration | PASS | 1983×793 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/13-summary.md` | 10 | `images/13-summary-01-churn-prediction-imagegen.png` | instructional illustration | PASS | 1717×916 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/14-explore-more.md` | 6 | `images/14-explore-more-01-preprocessing-model-comparison-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 21 | `images/01-overview-02-churn-scenario-crisp.png` | instructional illustration | PASS | 1445×1088 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 15 | `images/02-accuracy-02-accuracy-example-crisp.png` | instructional illustration | PASS | 1804×1360 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 84 | `images/02-accuracy-01-accuracy-vs-threshold-crisp.png` | instructional illustration | PASS | 1488×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 118 | `images/02-accuracy-08-class-imbalance-crisp.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 24 | `images/03-confusion-table-01-four-outcomes-crisp.png` | instructional illustration | PASS | 1504×1046 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 51 | `images/03-confusion-table-04-confusion-counts-crisp.png` | instructional illustration | PASS | 1554×1012 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 94 | `images/03-confusion-table-07-accuracy-from-table-crisp.png` | instructional illustration | PASS | 1554×1012 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 19 | `images/04-precision-recall-01-precision-definition-crisp.png` | instructional illustration | PASS | 1472×1068 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 32 | `images/04-precision-recall-03-precision-pie-crisp.png` | instructional illustration | PASS | 1728×910 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 42 | `images/04-precision-recall-04-recall-definition-crisp.png` | instructional illustration | PASS | 1415×1111 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 55 | `images/04-precision-recall-05-recall-example-crisp.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 61 | `images/04-precision-recall-06-precision-recall-table-crisp.png` | instructional illustration | PASS | 1565×1005 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 75 | `images/05-roc-01-tpr-fpr-vs-threshold-crisp.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 88 | `images/05-roc-02-random-model-tpr-fpr-crisp.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 112 | `images/05-roc-03-ideal-model-tpr-fpr-crisp.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 130 | `images/05-roc-04-model-vs-ideal-tpr-fpr-crisp.png` | instructional illustration | PASS | 1521×1034 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 148 | `images/05-roc-05-roc-curve-manual-crisp.png` | instructional illustration | PASS | 1278×1231 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 176 | `images/05-roc-06-roc-curve-sklearn-crisp.png` | instructional illustration | PASS | 1278×1231 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/06-auc.md` | 22 | `images/06-auc-02-auc-values-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/06-auc.md` | 50 | `images/06-auc-05-auc-interpretation-imagegen-v2.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/07-cross-validation.md` | 46 | `images/07-cross-validation-01-kfold-diagram-pilot.png` | local image | PASS | 1647×955 | review required: native/source asset |
| ML | `cohorts/2026/04-evaluation/09-explore-more.md` | 6 | `images/09-explore-more-01-threshold-precision-recall-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 10 | `images/01-intro-01-title-imagegen.png` | instructional illustration | PASS | 1422×1106 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 31 | `images/01-intro-02-model-deployment-diagram-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 55 | `images/01-intro-05-environments-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/03-flask-intro.md` | 19 | `images/03-flask-intro-02-request-response-imagegen.png` | instructional illustration | PASS | 1560×1008 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 13 | `images/05-pipenv-01-title-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 23 | `images/05-pipenv-02-version-conflict-imagegen.png` | instructional illustration | PASS | 1616×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 29 | `images/05-pipenv-03-isolated-environments-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 36 | `images/05-pipenv-04-venv-tools-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/06-docker.md` | 49 | `images/06-docker-02-containers-on-host-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/06-docker.md` | 127 | `images/06-docker-05-port-mapping-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 29 | `images/07-aws-eb-02-eb-architecture-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/09-explore-more.md` | 6 | `images/09-explore-more-01-deployment-choices-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 24 | `images/01-credit-risk-01-loan-application-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 32 | `images/01-credit-risk-02-historical-data-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 60 | `images/01-credit-risk-03-probability-of-default-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 37 | `images/03-decision-trees-01-risk-rules-tree-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 120 | `images/03-decision-trees-05-memorizing-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 179 | `images/03-decision-trees-06-learned-rules-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 185 | `images/03-decision-trees-07-decision-stump-imagegen.png` | instructional illustration | PASS | 1617×973 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 193 | `images/04-decision-tree-learning-08-stopping-criteria-imagegen.png` | instructional illustration | PASS | 1620×971 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 119 | `images/05-decision-tree-tuning-05-heatmap-imagegen.png` | instructional illustration | PASS | 1573×1000 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 132 | `images/05-decision-tree-tuning-07-wider-search-imagegen.png` | instructional illustration | PASS | 1642×958 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 26 | `images/06-random-forest-01-board-of-experts-imagegen.png` | instructional illustration | PASS | 1491×1055 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 58 | `images/06-random-forest-02-random-forest-imagegen.png` | instructional illustration | PASS | 1491×1055 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 87 | `images/06-random-forest-03-auc-vs-trees-imagegen.png` | instructional illustration | PASS | 1463×1075 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 133 | `images/06-random-forest-04-tuning-max-depth-imagegen.png` | instructional illustration | PASS | 1434×1097 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 186 | `images/06-random-forest-05-tuning-min-samples-leaf-imagegen.png` | instructional illustration | PASS | 1434×1097 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/07-boosting.md` | 27 | `images/07-boosting-01-boosting-vs-random-forest-imagegen.png` | instructional illustration | PASS | 1491×1055 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/07-boosting.md` | 32 | `images/07-boosting-02-gradient-boosting-trees-imagegen.png` | instructional illustration | PASS | 1491×1055 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/07-boosting.md` | 187 | `images/07-boosting-03-train-val-auc-imagegen.png` | instructional illustration | PASS | 1463×1075 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 24 | `images/08-xgb-tuning-01-parameters-imagegen.png` | instructional illustration | PASS | 1491×1055 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 81 | `images/08-xgb-tuning-02-tuning-eta-imagegen.png` | instructional illustration | PASS | 1463×1075 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 114 | `images/08-xgb-tuning-03-max-depth-curves-imagegen.png` | instructional illustration | PASS | 1548×1016 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 152 | `images/08-xgb-tuning-04-min-child-weight-curves-imagegen.png` | instructional illustration | PASS | 1562×1007 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 19 | `images/09-final-model-01-comparing-validation-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 57 | `images/09-final-model-02-tuned-random-forest-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 88 | `images/09-final-model-03-xgb-validation-auc-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 111 | `images/09-final-model-04-full-train-prep-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 127 | `images/09-final-model-05-feature-matrices-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 136 | `images/09-final-model-06-dmatrix-imagegen.png` | instructional illustration | PASS | 1672×940 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 166 | `images/09-final-model-07-final-test-auc-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 14 | `images/10-summary-01-summary-slide-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 25 | `images/10-summary-02-decision-tree-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 27 | `images/10-summary-03-overfitting-auc-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 37 | `images/10-summary-04-random-forest-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 45 | `images/10-summary-05-gradient-boosting-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 47 | `images/10-summary-06-xgb-parameters-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/11-explore-more.md` | 4 | `images/11-explore-more-01-ensemble-experiments-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | 19 | `images/01-fashion-classification-01-tabular-vs-images-imagegen.png` | instructional illustration | PASS | 1445×1088 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | 34 | `images/01-fashion-classification-02-upload-service-imagegen.png` | instructional illustration | PASS | 1444×1089 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | 51 | `images/01-fashion-classification-03-clothing-dataset-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | 62 | `images/01-fashion-classification-04-dataset-small-train-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | 88 | `images/01-fashion-classification-05-cs231n-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | 107 | `images/01-fashion-classification-06-notebook-plan-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/01-fashion-classification.md` | 113 | `images/01-fashion-classification-07-notebook-plan-2-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 24 | `images/02-tensorflow-keras-01-keras-inside-tensorflow-imagegen.png` | instructional illustration | PASS | 1445×1088 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 46 | `images/02-tensorflow-keras-02-install-tensorflow-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 65 | `images/02-tensorflow-keras-03-imports-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 82 | `images/02-tensorflow-keras-04-load-img-import-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 102 | `images/02-tensorflow-keras-05-image-sizes-imagegen.png` | instructional illustration | PASS | 1445×1088 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 112 | `images/02-tensorflow-keras-06-load-img-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 124 | `images/02-tensorflow-keras-07-rgb-channels-imagegen.png` | instructional illustration | PASS | 1445×1088 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/02-tensorflow-keras.md` | 146 | `images/02-tensorflow-keras-08-numpy-array-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 25 | `images/03-pretrained-models-02-imagenet-crisp.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 36 | `images/03-pretrained-models-01-keras-applications-crisp.png` | instructional illustration | PASS | 1478×1064 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 54 | `images/03-pretrained-models-03-sagemaker-gpu-crisp.png` | instructional illustration | PASS | 1622×969 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 88 | `images/03-pretrained-models-04-xception-model-crisp.png` | instructional illustration | PASS | 1478×1064 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 93 | `images/03-pretrained-models-05-xception-weights-download-crisp.png` | instructional illustration | PASS | 1478×1064 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 108 | `images/03-pretrained-models-06-batch-shape-crisp.png` | instructional illustration | PASS | 1478×1064 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 125 | `images/03-pretrained-models-07-preprocess-input-crisp.png` | instructional illustration | PASS | 1478×1064 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 152 | `images/03-pretrained-models-08-decode-predictions-crisp.png` | instructional illustration | PASS | 1478×1064 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 22 | `images/04-conv-neural-nets-01-cnn-overview-imagegen.png` | instructional illustration | PASS | 1585×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 50 | `images/04-conv-neural-nets-02-feature-map-imagegen.png` | instructional illustration | PASS | 1537×1023 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 61 | `images/04-conv-neural-nets-03-one-feature-map-per-filter-imagegen.png` | instructional illustration | PASS | 1413×1113 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 74 | `images/04-conv-neural-nets-04-chained-conv-layers-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 111 | `images/04-conv-neural-nets-05-vector-representation-imagegen.png` | instructional illustration | PASS | 1412×1114 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 139 | `images/04-conv-neural-nets-06-logistic-regression-crisp.png` | instructional illustration | PASS | 2670×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 163 | `images/04-conv-neural-nets-07-dense-layer-imagegen.png` | instructional illustration | PASS | 1414×1112 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 185 | `images/04-conv-neural-nets-08-summary-imagegen.png` | instructional illustration | PASS | 1405×1119 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 246 | `https://github.com/user-attachments/assets/3cfca38d-56bd-4a51-a3ce-70d8c071d4c8` | remote | REMOTE | — | not locally checked |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 248 | `https://github.com/user-attachments/assets/5465dc2e-402d-41c9-a6fb-3ecfdc384796` | remote | REMOTE | — | not locally checked |
| ML | `cohorts/2026/08-deep-learning/04-conv-neural-nets.md` | 248 | `https://github.com/user-attachments/assets/c8a57bb4-c454-4169-b18c-41b79449bbe6` | remote | REMOTE | — | not locally checked |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 36 | `images/05-transfer-learning-01-transfer-learning-idea-imagegen.png` | instructional illustration | PASS | 1619×971 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 91 | `images/05-transfer-learning-02-found-3068-images-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 95 | `images/05-transfer-learning-03-class-indices-one-hot-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 147 | `images/05-transfer-learning-04-validation-341-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 214 | `images/05-transfer-learning-05-pooling-vectors-crisp.png` | instructional illustration | PASS | 2736×2022 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 239 | `images/05-transfer-learning-06-dense-10-outputs-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 341 | `images/05-transfer-learning-07-training-output-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/05-transfer-learning.md` | 357 | `images/05-transfer-learning-08-history-plot-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/06-learning-rate.md` | 49 | `images/06-learning-rate-01-book-analogy-imagegen.png` | instructional illustration | PASS | 1444×1089 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/06-learning-rate.md` | 90 | `images/06-learning-rate-02-make-model-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/06-learning-rate.md` | 121 | `images/06-learning-rate-03-scores-loop-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/06-learning-rate.md` | 146 | `images/06-learning-rate-04-train-accuracy-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/06-learning-rate.md` | 162 | `images/06-learning-rate-05-val-accuracy-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/06-learning-rate.md` | 169 | `images/06-learning-rate-06-two-lr-validation-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/06-learning-rate.md` | 184 | `images/06-learning-rate-07-select-001-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 22 | `images/07-checkpointing-01-oscillation-crisp.png` | instructional illustration | PASS | 1609×977 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 44 | `images/07-checkpointing-02-callbacks-imagegen.png` | instructional illustration | PASS | 1508×1043 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 99 | `images/07-checkpointing-04-save-best-only-imagegen.png` | instructional illustration | PASS | 1508×1043 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 28 | `images/08-more-layers-01-inner-layer-diagram-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 41 | `images/08-more-layers-02-activation-functions-crisp.png` | instructional illustration | PASS | 2032×774 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 137 | `images/08-more-layers-06-val-accuracy-plot-crisp.png` | instructional illustration | PASS | 1609×977 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 25 | `images/09-dropout-01-motivation-logo-imagegen.png` | instructional illustration | PASS | 1696×927 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 35 | `images/09-dropout-02-hiding-input-imagegen.png` | instructional illustration | PASS | 1024×1536 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 43 | `images/09-dropout-03-frozen-neuron-imagegen-v2.png` | instructional illustration | PASS | 1717×916 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 90 | `images/09-dropout-04-v3-diagram-imagegen.png` | instructional illustration | PASS | 1817×866 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 135 | `images/09-dropout-07-dropout-02-vs-train-imagegen.png` | instructional illustration | PASS | 1613×975 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 152 | `images/09-dropout-06-val-accuracy-dropout-imagegen.png` | instructional illustration | PASS | 1609×977 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 165 | `images/09-dropout-08-no-regularization-overfit-imagegen.png` | instructional illustration | PASS | 1609×977 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 15 | `images/10-augmentation-01-generate-more-images-imagegen.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 27 | `images/10-augmentation-02-flip-rotation-shift-grids-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 29 | `images/10-augmentation-03-zoom-grid-imagegen.png` | instructional illustration | PASS | 1891×831 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 127 | `images/10-augmentation-05-nvidia-smi-cpu-bound-imagegen.png` | instructional illustration | PASS | 1717×916 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 129 | `images/10-augmentation-06-val-stuck-077-imagegen.png` | instructional illustration | PASS | 1650×953 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/12-using-model.md` | 94 | `images/12-using-model-03-load-img-pants-imagegen.png` | instructional illustration | PASS | 1199×1312 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/13-summary.md` | 9 | `images/13-summary-01-use-case-diagram-imagegen.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/14-explore-more.md` | 5 | `images/14-explore-more-01-learning-paths-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/install.md` | 9 | `images/install-01-gpu-stack-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 25 | `images/01-intro-01-clothes-classification-use-case-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 44 | `images/01-intro-02-aws-lambda-deployment-imagegen.png` | instructional illustration | PASS | 1691×930 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 51 | `images/01-intro-03-lambda-uses-tf-lite-imagegen.png` | instructional illustration | PASS | 1835×857 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 57 | `images/01-intro-04-module-plan-crisp.png` | instructional illustration | PASS | 1400×890 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 69 | `images/01-intro-05-module-plan-lambda-gateway-crisp.png` | instructional illustration | PASS | 1400×845 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 17 | `images/02-aws-lambda-01-search-lambda-crisp.png` | instructional illustration | PASS | 3000×1896 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 41 | `images/02-aws-lambda-02-create-function-crisp.png` | instructional illustration | PASS | 3000×1896 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 67 | `images/02-aws-lambda-03-pong-handler-crisp.png` | instructional illustration | PASS | 3000×1896 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 81 | `images/02-aws-lambda-04-test-pong-response-crisp.png` | instructional illustration | PASS | 3288×1566 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 109 | `images/02-aws-lambda-05-pants-response-crisp.png` | instructional illustration | PASS | 3288×1566 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 111 | `images/02-aws-lambda-06-final-handler-code-crisp.png` | instructional illustration | PASS | 3288×1566 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 127 | `images/02-aws-lambda-07-serverless-vs-serverful-imagegen.png` | instructional illustration | PASS | 1660×948 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/02-aws-lambda.md` | 146 | `images/02-aws-lambda-08-invite-link-function-crisp.png` | instructional illustration | PASS | 3000×1896 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 82 | `images/03-tensorflow-lite-01-load-keras-model-crisp.png` | instructional illustration | PASS | 3000×1836 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 93 | `images/03-tensorflow-lite-02-03-predictions-to-tflite-crisp.png` | instructional illustration | PASS | 2048×768 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 139 | `images/03-tensorflow-lite-04-model-sizes-crisp.png` | instructional illustration | PASS | 3000×1836 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 188 | `images/03-tensorflow-lite-05-interpreter-indexes-crisp.png` | instructional illustration | PASS | 3000×1836 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 221 | `images/03-tensorflow-lite-06-keras-preprocess-source-crisp.png` | instructional illustration | PASS | 2170×725 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 263 | `images/03-tensorflow-lite-07-keras-image-helper-crisp.png` | instructional illustration | PASS | 3000×1836 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 278 | `images/03-tensorflow-lite-08-tflite-runtime-install-crisp.png` | instructional illustration | PASS | 3000×1836 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/04-preparing-code.md` | 14 | `images/04-preparing-code-01-lesson-plan-crisp.png` | instructional illustration | PASS | 3000×2016 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/04-preparing-code.md` | 29 | `images/04-preparing-code-02-nbconvert-crisp.png` | instructional illustration | PASS | 3000×2016 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/04-preparing-code.md` | 34 | `images/04-preparing-code-03-generated-script-crisp.png` | instructional illustration | PASS | 3000×2016 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/04-preparing-code.md` | 52 | `images/04-preparing-code-04-predict-function-crisp.png` | instructional illustration | PASS | 3312×1320 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/04-preparing-code.md` | 113 | `images/04-preparing-code-06-final-script-crisp.png` | instructional illustration | PASS | 3000×2016 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/04-preparing-code.md` | 134 | `images/04-preparing-code-05-test-in-ipython-crisp.png` | instructional illustration | PASS | 3000×2016 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/05-docker-image.md` | 29 | `images/05-docker-image-01-ecr-public-gallery-crisp.png` | instructional illustration | PASS | 3300×1500 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/05-docker-image.md` | 60 | `images/05-docker-image-02-dockerfile-crisp.png` | instructional illustration | PASS | 3000×1890 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/05-docker-image.md` | 98 | `images/05-docker-image-03-test-script-crisp.png` | instructional illustration | PASS | 3000×1890 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/05-docker-image.md` | 120 | `images/05-docker-image-04-glibc-error-crisp.png` | instructional illustration | PASS | 3300×1578 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/05-docker-image.md` | 143 | `images/05-docker-image-05-tflite-wheels-crisp.png` | instructional illustration | PASS | 3300×1590 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/05-docker-image.md` | 161 | `images/05-docker-image-06-rebuild-crisp.png` | instructional illustration | PASS | 2682×1758 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/05-docker-image.md` | 170 | `images/05-docker-image-07-float32-error-crisp.png` | instructional illustration | PASS | 3300×1848 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 36 | `images/06-creating-lambda-01-ecr-create-repository-crisp.png` | instructional illustration | PASS | 2682×1758 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 119 | `images/06-creating-lambda-02-docker-push-crisp.png` | instructional illustration | PASS | 2682×1758 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 135 | `images/06-creating-lambda-03-create-function-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 154 | `images/06-creating-lambda-04-timeout-error-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 163 | `images/06-creating-lambda-05-configure-timeout-memory-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 176 | `images/06-creating-lambda-06-test-success-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 188 | `images/06-creating-lambda-07-lambda-pricing-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/06-creating-lambda.md` | 195 | `images/06-creating-lambda-08-price-calculation-crisp.png` | instructional illustration | PASS | 3000×2040 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/07-api-gateway.md` | 22 | `images/07-api-gateway-01-create-rest-api-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/07-api-gateway.md` | 28 | `images/07-api-gateway-02-create-resource-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/07-api-gateway.md` | 44 | `images/07-api-gateway-03-lambda-permission-crisp.png` | instructional illustration | PASS | 3000×1890 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/07-api-gateway.md` | 58 | `images/07-api-gateway-04-method-test-crisp.png` | instructional illustration | PASS | 3300×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/07-api-gateway.md` | 66 | `images/07-api-gateway-05-test-response-crisp.png` | instructional illustration | PASS | 3300×1530 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/07-api-gateway.md` | 78 | `images/07-api-gateway-06-deploy-stage-crisp.png` | instructional illustration | PASS | 1520×980 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/07-api-gateway.md` | 92 | `images/07-api-gateway-07-test-py-gateway-url-crisp.png` | instructional illustration | PASS | 3312×1848 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/08-summary.md` | 19 | `images/08-summary-01-lambda-handler-code-crisp.png` | instructional illustration | PASS | 3000×1890 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/08-summary.md` | 36 | `images/08-summary-02-summary-points-crisp.png` | instructional illustration | PASS | 3000×1890 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/08-summary.md` | 49 | `images/08-summary-03-tflite-inference-code-crisp.png` | instructional illustration | PASS | 3000×1890 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/08-summary.md` | 55 | `images/08-summary-04-tflite-wheels-crisp.png` | instructional illustration | PASS | 3300×1590 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/08-summary.md` | 63 | `images/08-summary-05-tensorflow-wheel-size-crisp.png` | instructional illustration | PASS | 3300×1590 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/09-explore-more.md` | 3 | `images/09-explore-more-01-serverless-models-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/updates.md` | 12 | `images/updates-01-runtime-compatibility-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/01-overview.md` | 32 | `images/01-overview-01-tf-serving-inference-imagegen.png` | instructional illustration | PASS | 1448×1086 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/01-overview.md` | 50 | `images/01-overview-02-architecture-imagegen.png` | instructional illustration | PASS | 1619×971 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/01-overview.md` | 56 | `images/01-overview-03-grpc-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/01-overview.md` | 75 | `images/01-overview-05-cpu-gpu-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/01-overview.md` | 84 | `images/01-overview-04-kubernetes-imagegen.png` | instructional illustration | PASS | 1448×1086 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/01-overview.md` | 110 | `images/01-overview-06-plan-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 39 | `images/02-tensorflow-serving-01-saved-model-crisp.png` | instructional illustration | PASS | 1685×933 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 68 | `images/02-tensorflow-serving-02-signature-crisp.png` | instructional illustration | PASS | 3750×1239 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 113 | `images/02-tensorflow-serving-03-docker-run-crisp.png` | instructional illustration | PASS | 2760×1494 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 136 | `images/02-tensorflow-serving-04-install-libraries-crisp.png` | instructional illustration | PASS | 3000×1230 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 166 | `images/02-tensorflow-serving-05-grpc-stub-crisp.png` | instructional illustration | PASS | 3000×1650 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 204 | `images/02-tensorflow-serving-06-prepare-request-crisp.png` | instructional illustration | PASS | 3000×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 261 | `images/02-tensorflow-serving-07-prediction-crisp.png` | instructional illustration | PASS | 1520×1120 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/03-preprocessing.md` | 39 | `images/03-preprocessing-01-nbconvert-crisp.png` | instructional illustration | PASS | 2940×1542 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/03-preprocessing.md` | 86 | `images/03-preprocessing-02-gateway-script-crisp.png` | instructional illustration | PASS | 3000×1920 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/03-preprocessing.md` | 105 | `images/03-preprocessing-03-flask-app-crisp.png` | instructional illustration | PASS | 3000×1920 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/03-preprocessing.md` | 149 | `images/03-preprocessing-05-tensorflow-protobuf-crisp.png` | instructional illustration | PASS | 3000×1920 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/03-preprocessing.md` | 187 | `images/03-preprocessing-06-proto-py-crisp.png` | instructional illustration | PASS | 3000×1920 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/03-preprocessing.md` | 196 | `images/03-preprocessing-04-pipenv-install-crisp.png` | instructional illustration | PASS | 2760×1704 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/04-docker-compose.md` | 99 | `images/04-docker-compose-03-isolated-containers-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/05-kubernetes-intro.md` | 34 | `images/05-kubernetes-intro-01-cluster-nodes-pods-imagegen.png` | instructional illustration | PASS | 1448×1086 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/05-kubernetes-intro.md` | 48 | `images/05-kubernetes-intro-02-deployments-imagegen.png` | instructional illustration | PASS | 1438×1093 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/05-kubernetes-intro.md` | 74 | `images/05-kubernetes-intro-03-services-crisp.png` | instructional illustration | PASS | 1441×1091 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/05-kubernetes-intro.md` | 94 | `images/05-kubernetes-intro-05-definitions-imagegen.png` | instructional illustration | PASS | 1441×1091 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/05-kubernetes-intro.md` | 96 | `images/05-kubernetes-intro-04-external-internal-ingress-imagegen.png` | instructional illustration | PASS | 1441×1091 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/05-kubernetes-intro.md` | 112 | `images/05-kubernetes-intro-06-scaling-imagegen.png` | instructional illustration | PASS | 1442×1091 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | 96 | `images/06-kubernetes-simple-service-01-ping-app-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | 101 | `images/06-kubernetes-simple-service-02-build-ping-crisp.png` | instructional illustration | PASS | 3576×1938 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | 141 | `images/06-kubernetes-simple-service-03-cluster-info-crisp.png` | instructional illustration | PASS | 2682×1644 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | 179 | `images/06-kubernetes-simple-service-04-deployment-yaml-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | 213 | `images/06-kubernetes-simple-service-05-kind-load-crisp.png` | instructional illustration | PASS | 2682×1860 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | 234 | `images/06-kubernetes-simple-service-06-service-yaml-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/06-kubernetes-simple-service.md` | 262 | `images/06-kubernetes-simple-service-07-service-lb-crisp.png` | instructional illustration | PASS | 2670×1896 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | 15 | `images/07-kubernetes-tf-serving-01-kube-config-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | 78 | `images/07-kubernetes-tf-serving-02-model-deployment-crisp.png` | instructional illustration | PASS | 2682×1914 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | 80 | `images/07-kubernetes-tf-serving-03-model-test-crisp.png` | instructional illustration | PASS | 1388×1276 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | 121 | `images/07-kubernetes-tf-serving-04-model-service-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | 161 | `images/07-kubernetes-tf-serving-05-gateway-deployment-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | 204 | `images/07-kubernetes-tf-serving-06-telnet-crisp.png` | instructional illustration | PASS | 2682×1902 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/07-kubernetes-tf-serving.md` | 246 | `images/07-kubernetes-tf-serving-07-gateway-service-crisp.png` | instructional illustration | PASS | 2682×1902 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/08-eks.md` | 18 | `images/08-eks-01-eksctl-install-crisp.png` | instructional illustration | PASS | 2682×1902 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/08-eks.md` | 50 | `images/08-eks-02-eks-config-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/08-eks.md` | 63 | `images/08-eks-04-create-cluster-crisp.png` | instructional illustration | PASS | 2700×1902 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/08-eks.md` | 111 | `images/08-eks-03-ecr-push-crisp.png` | instructional illustration | PASS | 3576×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/08-eks.md` | 152 | `images/08-eks-05-external-ip-crisp.png` | instructional illustration | PASS | 2700×1902 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/08-eks.md` | 174 | `images/08-eks-06-aws-console-crisp.png` | instructional illustration | PASS | 3576×1542 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/09-summary.md` | 26 | `images/09-summary-01-architecture-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/09-summary.md` | 62 | `images/09-summary-02-local-alternatives-crisp.png` | instructional illustration | PASS | 3018×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/10-kubernetes/10-explore-more.md` | 4 | `images/10-explore-more-01-cluster-options-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/01-intro.md` | 71 | `images/01-intro-01-rag-project-overview-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/03-rag.md` | 136 | `images/03-rag-08-rag-architecture-sketch-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/08-rag-helper.md` | 18 | `images/08-rag-helper-01-reusable-rag-helper-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/09-data-ingestion.md` | 232 | `images/09-data-ingestion-06-annotated-architecture-sketch-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/10-rag-next-steps.md` | 19 | `images/10-rag-next-steps-01-rag-roadmap-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/11-agents-intro.md` | 48 | `images/11-agents-intro-04-agentic-flow-diagram-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/12-rag-revision.md` | 15 | `images/12-rag-revision-01-typo-retry-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/01-agentic-rag/16-other-frameworks.md` | 11 | `images/16-other-frameworks-01-shared-agent-loop-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/02-vector-search/01-intro.md` | 24 | `images/01-intro-03-rag-pipeline-whiteboard-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/02-vector-search/02-embeddings.md` | 26 | `images/02-embeddings-01-vector-space-whiteboard-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/02-vector-search/07-sqlitesearch-vector.md` | 37 | `images/07-sqlitesearch-vector-01-ann-vs-nn-whiteboard-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/02-vector-search/07-sqlitesearch-vector.md` | 55 | `images/07-sqlitesearch-vector-02-ingestion-deployment-split-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/02-vector-search/10-next-steps.md` | 14 | `images/10-next-steps-01-similarity-search-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/03-orchestration/01-intro.md` | 38 | `images/01-intro-01-ai-orchestration-path-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/03-orchestration/02-context-engineering.md` | 22 | `images/02-context-engineering-01-context-quality-flow-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/03-orchestration/03-setup.md` | 39 | `images/03-setup-01-secure-kestra-setup-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/03-orchestration/08-best-practices.md` | 13 | `images/08-best-practices-01-pattern-selection-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/04-evaluation/01-intro.md` | 16 | `images/01-intro-01-agentic-rag-diagram-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/04-evaluation/01-intro.md` | 30 | `images/01-intro-02-interact-or-generate-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| LLM | `cohorts/2026/04-evaluation/03-ground-truth-batch.md` | 100 | `images/03-ground-truth-batch-03-parallel-split-whiteboard-imagegen.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| LLM | `cohorts/2026/04-evaluation/11-evaluation-intro.md` | 36 | `images/11-evaluation-intro-01-rag-agent-evaluation-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/04-evaluation/14-agent-evaluation.md` | 18 | `images/14-agent-evaluation-01-agent-evaluation-record-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/04-evaluation/15-next-steps.md` | 16 | `images/15-next-steps-01-evaluation-feedback-loop-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/05-monitoring/10-feedback-dashboard.md` | 10 | `images/10-feedback-dashboard-01-monitoring-panels-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/05-monitoring/11-synthetic-data.md` | 11 | `images/11-synthetic-data-01-live-data-loop-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/05-monitoring/13-docker-compose.md` | 14 | `images/13-docker-compose-01-service-topology-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/06-best-practices/01-intro.md` | 21 | `images/01-intro-01-rag-technique-map-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/06-best-practices/02-hybrid-search.md` | 6 | `images/02-hybrid-search-01-keyword-vector-fusion-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/06-best-practices/03-reranking.md` | 12 | `images/03-reranking-01-rrf-rerank-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/06-best-practices/04-langchain.md` | 11 | `images/04-langchain-01-retriever-wrapper-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/06-best-practices/05-next-steps.md` | 16 | `images/05-next-steps-01-retrieval-roadmap-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/07-project-example/01-intro.md` | 5 | `images/01-intro-01-fitness-rag-project-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/07-project-example/02-evaluating-retrieval.md` | 5 | `images/02-evaluating-retrieval-01-hit-rate-mrr-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/07-project-example/03-evaluating-rag.md` | 5 | `images/03-evaluating-rag-01-llm-judge-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/07-project-example/04-interface.md` | 5 | `images/04-interface-01-api-ingestion-flow-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/07-project-example/05-monitoring.md` | 5 | `images/05-monitoring-01-compose-observability-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/07-project-example/06-summary.md` | 5 | `images/06-summary-01-project-delivery-path-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| LLM | `cohorts/2026/07-project-example/07-chunking.md` | 5 | `images/07-chunking-01-long-document-chunks-imagegen.png` | instructional illustration | PASS | 1672×940 | review required: crisp/generated asset |
| MLOps | `01-intro/README.md` | 10 | `images/illustrations/01-01-mlops-lifecycle.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `01-intro/README.md` | 22 | `images/illustrations/01-02-01-cloud-workspace.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `01-intro/README.md` | 37 | `images/illustrations/01-02-02-aws-vm-setup.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `01-intro/README.md` | 112 | `images/illustrations/01-03-ride-duration-training.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `01-intro/README.md` | 126 | `images/illustrations/01-04-course-overview.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `01-intro/README.md` | 137 | `images/illustrations/01-05-mlops-maturity-model.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `01-intro/README.md` | 152 | `../images/homework-checklist.png` | homework/support | PASS | 1672×941 | reference checked; non-illustration asset |
| MLOps | `02-experiment-tracking/README.md` | 14 | `images/illustrations/02-01-experiment-tracking.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `02-experiment-tracking/README.md` | 25 | `images/illustrations/02-02-mlflow-getting-started.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `02-experiment-tracking/README.md` | 41 | `images/illustrations/02-03-mlflow-experiment-tracking.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `02-experiment-tracking/README.md` | 52 | `images/illustrations/02-04-model-management.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `02-experiment-tracking/README.md` | 63 | `images/illustrations/02-05-model-registry.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `02-experiment-tracking/README.md` | 75 | `images/illustrations/02-06-mlflow-in-practice.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `02-experiment-tracking/README.md` | 85 | `images/illustrations/02-07-benefits-limitations-alternatives.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `02-experiment-tracking/README.md` | 95 | `../images/homework-checklist.png` | homework/support | PASS | 1672×941 | reference checked; non-illustration asset |
| MLOps | `03-orchestration/README.md` | 8 | `images/illustrations/03-01-ml-pipeline.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `03-orchestration/README.md` | 17 | `images/illustrations/03-02-notebook-to-script.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `03-orchestration/README.md` | 30 | `images/illustrations/03-03-orchestrated-workflow.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `03-orchestration/README.md` | 83 | `../images/homework-checklist.png` | homework/support | PASS | 1672×941 | reference checked; non-illustration asset |
| MLOps | `04-deployment/README.md` | 8 | `images/illustrations/04-01-three-deployment-modes.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `04-deployment/README.md` | 19 | `images/illustrations/04-02-flask-docker-service.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `04-deployment/README.md` | 32 | `images/illustrations/04-03-registry-model-serving.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `04-deployment/README.md` | 45 | `images/illustrations/04-04-streaming-kinesis-lambda.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `04-deployment/README.md` | 59 | `images/illustrations/04-05-batch-scoring-script.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `04-deployment/README.md` | 76 | `images/illustrations/04-06-mage-batch-workflow.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `04-deployment/README.md` | 86 | `../images/homework-checklist.png` | homework/support | PASS | 1672×941 | reference checked; non-illustration asset |
| MLOps | `05-monitoring/README.md` | 8 | `images/illustrations/05-01-ml-monitoring-loop.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 19 | `images/illustrations/05-02-monitoring-environment.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 30 | `images/illustrations/05-03-reference-model-preparation.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 41 | `images/illustrations/05-04-evidently-metrics.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 51 | `images/illustrations/05-05-monitoring-dashboard.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 61 | `images/illustrations/05-06-dummy-monitoring.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 72 | `images/illustrations/05-07-data-quality-monitoring.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 85 | `images/illustrations/05-08-save-dashboard.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `05-monitoring/README.md` | 96 | `images/illustrations/05-09-debugging-tests-reports.png` | instructional illustration | PASS | 1672×941 | review required: native/source asset |
| MLOps | `06-best-practices/README.md` | 48 | `AWS-stream-pipeline-redrawn.png` | local image | PASS | 1575×998 | review required: native/source asset |
| MLOps | `06-best-practices/README.md` | 93 | `ci_cd_zoomcamp-redrawn.png` | local image | PASS | 1450×1085 | review required: native/source asset |
| MLOps | `07-project/README.md` | 104 | `https://static.streamlit.io/badges/streamlit_badge_black_white.svg` | remote | REMOTE | — | not locally checked |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 65 | `images/01-data-warehouse-and-bigquery-02-data-warehouse-diagram-imagegen.png` | instructional illustration | PASS | 1693×929 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 173 | `images/01-data-warehouse-and-bigquery-04-external-table-details-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 201 | `images/01-data-warehouse-and-bigquery-05-partitioning-diagram-crisp.png` | instructional illustration | PASS | 1674×940 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 245 | `images/01-data-warehouse-and-bigquery-06-partition-pruning-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 279 | `images/01-data-warehouse-and-bigquery-07-clustering-diagram-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 318 | `images/01-data-warehouse-and-bigquery-08-cluster-pruning-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | 13 | `images/04-internals-of-bigquery-01-architecture-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | 52 | `images/04-internals-of-bigquery-02-columnar-storage-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | 74 | `images/04-internals-of-bigquery-03-dremel-tree-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 66 | `images/05-machine-learning-in-bigquery-01-model-choice-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 26 | `images/06-deploying-a-machine-learning-model-01-exported-to-gcs-crisp.png` | instructional illustration | PASS | 1740×904 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 40 | `images/06-deploying-a-machine-learning-model-02-copy-model-local-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 65 | `images/06-deploying-a-machine-learning-model-03-docker-running-crisp.png` | instructional illustration | PASS | 2092×752 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 73 | `images/06-deploying-a-machine-learning-model-04-model-status-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 91 | `images/06-deploying-a-machine-learning-model-05-predict-crisp.png` | instructional illustration | PASS | 1694×929 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 96 | `images/06-deploying-a-machine-learning-model-06-predict-payment-type-2-crisp.png` | instructional illustration | PASS | 1692×929 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 32 | `images/01-introduction-to-batch-processing-01-batch-vs-streaming-imagegen.png` | instructional illustration | PASS | 1601×982 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 46 | `images/01-introduction-to-batch-processing-02-streaming-example-imagegen.png` | instructional illustration | PASS | 1133×1388 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 116 | `images/01-introduction-to-batch-processing-07-batch-vs-streaming-share-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/02-introduction-to-spark.md` | 26 | `images/02-introduction-to-spark-02-data-processing-engine-whiteboard-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/02-introduction-to-spark.md` | 62 | `images/02-introduction-to-spark-03-when-to-use-spark-whiteboard-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/02-introduction-to-spark.md` | 87 | `images/02-introduction-to-spark-04-typical-workflow-whiteboard-imagegen.png` | instructional illustration | PASS | 1627×967 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 22 | `images/03-installing-spark-01-install-guide-java-crisp.png` | instructional illustration | PASS | 2170×725 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 45 | `images/03-installing-spark-02-java-home-crisp.png` | instructional illustration | PASS | 1586×992 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 71 | `images/03-installing-spark-03-spark-download-page-crisp.png` | instructional illustration | PASS | 1590×989 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 80 | `images/03-installing-spark-04-spark-home-crisp.png` | instructional illustration | PASS | 1586×992 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 107 | `images/03-installing-spark-05-spark-shell-crisp.png` | instructional illustration | PASS | 1586×992 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 38 | `images/04-first-look-at-spark-01-spark-ui-crisp.png` | instructional illustration | PASS | 1844×853 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 79 | `images/04-first-look-at-spark-02-schema-problem-pandas-crisp.png` | instructional illustration | PASS | 1797×875 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 123 | `images/04-first-look-at-spark-03-schema-structtype-crisp.png` | instructional illustration | PASS | 1833×858 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 149 | `images/04-first-look-at-spark-04-partitions-slides-imagegen.png` | instructional illustration | PASS | 1402×1122 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 26 | `images/05-spark-dataframes-01-print-schema-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 43 | `images/05-spark-dataframes-02-select-crisp.png` | instructional illustration | PASS | 2007×784 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 108 | `images/05-spark-dataframes-03-built-in-functions-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 169 | `images/05-spark-dataframes-04-udf-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 82 | `images/06-preparing-taxi-data-04-zcat-crisp.png` | instructional illustration | PASS | 2109×745 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 87 | `images/06-preparing-taxi-data-05-tree-raw-crisp.png` | instructional illustration | PASS | 1562×1007 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 107 | `images/06-preparing-taxi-data-06-schema-strings-crisp.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 172 | `images/06-preparing-taxi-data-07-spark-ui-one-task-crisp.png` | instructional illustration | PASS | 1751×898 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 181 | `images/06-preparing-taxi-data-08-tree-pq-crisp.png` | instructional illustration | PASS | 1562×1007 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/07-sql-with-spark.md` | 36 | `images/07-sql-with-spark-01-read-parquet-crisp.png` | instructional illustration | PASS | 1562×1007 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/07-sql-with-spark.md` | 50 | `images/07-sql-with-spark-02-common-columns-crisp.png` | instructional illustration | PASS | 1562×1007 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 50 | `images/08-anatomy-of-a-spark-cluster-01-spark-submit-master-imagegen.png` | instructional illustration | PASS | 1448×1086 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 56 | `images/08-anatomy-of-a-spark-cluster-02-executors-failure-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 67 | `images/08-anatomy-of-a-spark-cluster-03-executors-pull-partitions-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 94 | `images/08-anatomy-of-a-spark-cluster-04-s3-gcs-instead-of-hdfs-imagegen.png` | instructional illustration | PASS | 1539×1022 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/09-groupby-in-spark.md` | 54 | `images/09-groupby-in-spark-02-three-stages-crisp.png` | instructional illustration | PASS | 1586×992 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/09-groupby-in-spark.md` | 120 | `images/09-groupby-in-spark-03-reshuffling-whiteboard-imagegen.png` | instructional illustration | PASS | 1569×1002 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/09-groupby-in-spark.md` | 158 | `images/09-groupby-in-spark-04-shuffle-read-write-crisp.png` | instructional illustration | PASS | 1586×992 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/10-joins-in-spark.md` | 59 | `images/10-joins-in-spark-02-sort-merge-join-stages-crisp.png` | instructional illustration | PASS | 1794×877 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/10-joins-in-spark.md` | 176 | `images/10-joins-in-spark-04-broadcast-exchange-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | 99 | `images/11-operations-on-spark-rdds-02-map-key-value-whiteboard-imagegen.png` | instructional illustration | PASS | 1667×943 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | 248 | `images/11-operations-on-spark-rdds-06-dag-two-stages-crisp.png` | instructional illustration | PASS | 1586×992 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | 20 | `images/12-spark-rdd-mappartition-01-map-partitions-diagram-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | 51 | `images/12-spark-rdd-mappartition-02-feature-columns-crisp.png` | instructional illustration | PASS | 2120×742 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | 39 | `images/14-creating-a-local-spark-cluster-01-spark-master-ui-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | 88 | `images/14-creating-a-local-spark-cluster-02-worker-registered-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | 28 | `images/15-setting-up-a-dataproc-cluster-01-create-cluster-crisp.png` | instructional illustration | PASS | 1597×985 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | 67 | `images/15-setting-up-a-dataproc-cluster-02-submit-job-form-crisp.png` | instructional illustration | PASS | 1222×1287 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | 125 | `images/15-setting-up-a-dataproc-cluster-05-reports-in-bucket-crisp.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/16-connecting-spark-to-bigquery.md` | 73 | `images/16-connecting-spark-to-bigquery-02-failed-to-find-bigquery-crisp.png` | instructional illustration | PASS | 1881×836 | review required: crisp/generated asset |

## Review handoff

- The machine-check snapshot contains 454 image-reference occurrences; 0 are missing or outside their repository.
- 0 active instructional references are crop-only candidates and must be checked against their retained original source before acceptance.
- The implementation agent must retain each original non-crisp source, crop only when it isolates useful content, merge adjacent screenshots on the content side in the correct orientation, and pass the original source image(s) plus any merged source reference to imagegen. A 2×/3× resized derivative must never be the only imagegen input.
- The independent reviewer must inspect crop direction/order, visual crispness, text/semantic fidelity, overlays, and every Markdown reference, then record an explicit verdict in the rollout report.

Reproduce this snapshot with: `python scripts/audit-illustrations/audit_illustrations.py --workspace-root /home/alexey/git --output /tmp/current-illustration-audit-2026-09-08-b.md`

The selected DE scope is explicitly `published=false`; it is included because it is the current 2027 draft work scope, not because it is already live. Historical cohorts and unrelated course repositories are excluded.
