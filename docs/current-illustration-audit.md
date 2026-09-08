# Current illustration audit

Generated on **2026-09-08** by the read-only audit script.

This is a committed snapshot of the four current Zoomcamp scopes. The script reads the course repositories but does not modify them.

## Source snapshots

| Scope | Repository | HEAD | Worktree | Active selection |
| --- | --- | --- | --- | --- |
| ML | `/home/alexey/git/machine-learning-zoomcamp` | `8aa115bea3a53d80363e2d4dab3609412926a38c` | clean | the published 2026 cohort flow and its module manifests |
| LLM | `/home/alexey/git/llm-zoomcamp` | `15e256f9a12db3117a3f21513d1dd11a56755ce1` | clean | the published 2026 cohort flow and its module manifests |
| MLOps | `/home/alexey/git/mlops-zoomcamp` | `e68ba45e215e8ebada38614444b05098fc933d9f` | clean | numbered root module/project README pages; no published cohort manifest exists |
| DE | `/home/alexey/git/data-engineering-zoomcamp` | `d69458342899d36881d2ff0788dbf9aa8e4b23eb` | clean | the current 2027 draft cohort and its module manifests; historical cohorts excluded |

## Status contract

- `PASS` means the local Markdown target resolves and a basic raster/vector dimension check succeeded.
- `MISSING`/`OUTSIDE` is an actionable broken reference; `REMOTE` is recorded but not locally checked; `DECODE?` needs an image decoder check.
- `review required` is intentional: filesystem checks cannot prove crop direction/order, visual crispness at lesson size, text or semantic fidelity, or overlay removal. An independent reviewer must record the visual verdict before publishing.
- Completed visual-review evidence is recorded in [`docs/visual-review-evidence-2026-09-08.md`](visual-review-evidence-2026-09-08.md); this scanner's queue remains conservative and is not a substitute for that evidence.
- Thumbnail and homework/support assets are reference-checked but are not counted as instructional illustrations in the unit list.

## Scope summary

| Scope | State | Active units | Illustration coverage | Image references | Visual review queue | Broken refs |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| ML | `published current cohort` | 105 | 105 present / 0 missing | 581 (578 local) | 569 visual reviews required | 0 missing/outside |
| LLM | `published current cohort` | 72 | 36 present / 36 missing | 38 (38 local) | 38 visual reviews required | 0 missing/outside |
| MLOps | `current self-paced curriculum` | 7 | 5 present / 2 missing | 38 (37 local) | 31 visual reviews required | 0 missing/outside |
| DE | `current draft; unpublished` | 88 | 22 present / 66 missing | 105 (105 local) | 105 visual reviews required | 0 missing/outside |

## Active units

Every row is in the selected active scope. `YES` means at least one resolving local instructional illustration reference; navigation thumbnails and homework checklists do not satisfy that column.

| Scope | Module | Unit | Unit file | Illustration present/missing | Instructional refs | All local/remote image refs |
| --- | --- | --- | --- | --- | ---: | ---: |
| ML | `cohorts/2026/01-intro` | Introduction to Machine Learning | `cohorts/2026/01-intro/01-what-is-ml.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/01-intro` | ML vs Rule-Based Systems | `cohorts/2026/01-intro/02-ml-vs-rules.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/01-intro` | Supervised Machine Learning | `cohorts/2026/01-intro/03-supervised-ml.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/01-intro` | CRISP-DM | `cohorts/2026/01-intro/04-crisp-dm.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/01-intro` | Model Selection Process | `cohorts/2026/01-intro/05-model-selection.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/01-intro` | Setting up the Environment | `cohorts/2026/01-intro/06-environment.md` | **YES** | 9 | 9 |
| ML | `cohorts/2026/01-intro` | Introduction to NumPy | `cohorts/2026/01-intro/07-numpy.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/01-intro` | Linear Algebra Refresher | `cohorts/2026/01-intro/08-linear-algebra.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/01-intro` | Introduction to Pandas | `cohorts/2026/01-intro/09-pandas.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/01-intro` | Summary | `cohorts/2026/01-intro/10-summary.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/02-regression` | Car price prediction project | `cohorts/2026/02-regression/01-car-price-intro.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Data preparation | `cohorts/2026/02-regression/02-data-preparation.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Exploratory data analysis | `cohorts/2026/02-regression/03-eda.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Setting up the validation framework | `cohorts/2026/02-regression/04-validation-framework.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Linear regression | `cohorts/2026/02-regression/05-linear-regression-simple.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Linear regression: vector form | `cohorts/2026/02-regression/06-linear-regression-vector.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Training linear regression: Normal equation | `cohorts/2026/02-regression/07-linear-regression-training.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Baseline model for car price prediction project | `cohorts/2026/02-regression/08-baseline-model.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/02-regression` | Root Mean Squared Error (RMSE) | `cohorts/2026/02-regression/09-rmse.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/02-regression` | Computing RMSE on validation data | `cohorts/2026/02-regression/10-car-price-validation.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/02-regression` | Feature engineering | `cohorts/2026/02-regression/11-feature-engineering.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/02-regression` | Categorical variables | `cohorts/2026/02-regression/12-categorical-variables.md` | **YES** | 7 | 8 |
| ML | `cohorts/2026/02-regression` | Regularization | `cohorts/2026/02-regression/13-regularization.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/02-regression` | Tuning the model | `cohorts/2026/02-regression/14-tuning-model.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/02-regression` | Using the model | `cohorts/2026/02-regression/15-using-model.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/02-regression` | Car price prediction project summary | `cohorts/2026/02-regression/16-summary.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/02-regression` | Explore more | `cohorts/2026/02-regression/17-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/03-classification` | Churn prediction project | `cohorts/2026/03-classification/01-churn-project.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/03-classification` | Data preparation | `cohorts/2026/03-classification/02-data-preparation.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/03-classification` | Setting up the validation framework | `cohorts/2026/03-classification/03-validation.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/03-classification` | EDA | `cohorts/2026/03-classification/04-eda.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/03-classification` | Feature importance: Churn rate and risk ratio | `cohorts/2026/03-classification/05-risk.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/03-classification` | Feature importance: Mutual information | `cohorts/2026/03-classification/06-mutual-info.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/03-classification` | Feature importance: Correlation | `cohorts/2026/03-classification/07-correlation.md` | **YES** | 3 | 5 |
| ML | `cohorts/2026/03-classification` | One-hot encoding | `cohorts/2026/03-classification/08-ohe.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/03-classification` | Logistic regression | `cohorts/2026/03-classification/09-logistic-regression.md` | **YES** | 2 | 5 |
| ML | `cohorts/2026/03-classification` | Training logistic regression with Scikit-Learn | `cohorts/2026/03-classification/10-training-log-reg.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/03-classification` | Model interpretation | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | **YES** | 6 | 7 |
| ML | `cohorts/2026/03-classification` | Using the model | `cohorts/2026/03-classification/12-using-log-reg.md` | **YES** | 4 | 4 |
| ML | `cohorts/2026/03-classification` | Summary | `cohorts/2026/03-classification/13-summary.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/03-classification` | Explore more | `cohorts/2026/03-classification/14-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/04-evaluation` | Evaluation metrics: session overview | `cohorts/2026/04-evaluation/01-overview.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/04-evaluation` | Accuracy and dummy model | `cohorts/2026/04-evaluation/02-accuracy.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/04-evaluation` | Confusion table | `cohorts/2026/04-evaluation/03-confusion-table.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/04-evaluation` | Precision and Recall | `cohorts/2026/04-evaluation/04-precision-recall.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/04-evaluation` | ROC Curves | `cohorts/2026/04-evaluation/05-roc.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/04-evaluation` | ROC AUC | `cohorts/2026/04-evaluation/06-auc.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/04-evaluation` | Cross-Validation | `cohorts/2026/04-evaluation/07-cross-validation.md` | **YES** | 5 | 6 |
| ML | `cohorts/2026/04-evaluation` | Summary | `cohorts/2026/04-evaluation/08-summary.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/04-evaluation` | Explore more | `cohorts/2026/04-evaluation/09-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/05-deployment` | Intro / Session overview | `cohorts/2026/05-deployment/01-intro.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/05-deployment` | Saving and loading the model | `cohorts/2026/05-deployment/02-pickle.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/05-deployment` | Web services: introduction to Flask | `cohorts/2026/05-deployment/03-flask-intro.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/05-deployment` | Serving the churn model with Flask | `cohorts/2026/05-deployment/04-flask-deployment.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/05-deployment` | Python virtual environment: Pipenv | `cohorts/2026/05-deployment/05-pipenv.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/05-deployment` | Environment management: Docker | `cohorts/2026/05-deployment/06-docker.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/05-deployment` | Deployment to the cloud: AWS Elastic Beanstalk (optional) | `cohorts/2026/05-deployment/07-aws-eb.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/05-deployment` | Summary | `cohorts/2026/05-deployment/08-summary.md` | **YES** | 3 | 3 |
| ML | `cohorts/2026/05-deployment` | Explore more | `cohorts/2026/05-deployment/09-explore-more.md` | **YES** | 1 | 1 |
| ML | `cohorts/2026/06-trees` | Credit risk scoring project | `cohorts/2026/06-trees/01-credit-risk.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/06-trees` | Data cleaning and preparation | `cohorts/2026/06-trees/02-data-prep.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/06-trees` | Decision trees | `cohorts/2026/06-trees/03-decision-trees.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/06-trees` | Decision tree learning algorithm | `cohorts/2026/06-trees/04-decision-tree-learning.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/06-trees` | Decision trees parameter tuning | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | **YES** | 7 | 7 |
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
| ML | `cohorts/2026/08-deep-learning` | Checkpointing | `cohorts/2026/08-deep-learning/07-checkpointing.md` | **YES** | 7 | 7 |
| ML | `cohorts/2026/08-deep-learning` | Adding more layers | `cohorts/2026/08-deep-learning/08-more-layers.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/08-deep-learning` | Regularization and dropout | `cohorts/2026/08-deep-learning/09-dropout.md` | **YES** | 8 | 8 |
| ML | `cohorts/2026/08-deep-learning` | Data augmentation | `cohorts/2026/08-deep-learning/10-augmentation.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/08-deep-learning` | Training a larger model | `cohorts/2026/08-deep-learning/11-large-model.md` | **YES** | 6 | 6 |
| ML | `cohorts/2026/08-deep-learning` | Using the model | `cohorts/2026/08-deep-learning/12-using-model.md` | **YES** | 5 | 5 |
| ML | `cohorts/2026/08-deep-learning` | Summary | `cohorts/2026/08-deep-learning/13-summary.md` | **YES** | 3 | 3 |
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
| DE | `cohorts/2027/03-data-warehouse` | Data Warehouse and BigQuery | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | **YES** | 8 | 8 |
| DE | `cohorts/2027/03-data-warehouse` | Partitioning vs Clustering | `cohorts/2027/03-data-warehouse/02-partitioning-vs-clustering.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/03-data-warehouse` | BigQuery Best Practices | `cohorts/2027/03-data-warehouse/03-bigquery-best-practices.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/03-data-warehouse` | Internals of BigQuery | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/03-data-warehouse` | Machine Learning in BigQuery | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | **YES** | 8 | 8 |
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
| DE | `cohorts/2027/06-batch` | Introduction to Batch Processing | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | **YES** | 6 | 6 |
| DE | `cohorts/2027/06-batch` | Introduction to Spark | `cohorts/2027/06-batch/02-introduction-to-spark.md` | **YES** | 3 | 3 |
| DE | `cohorts/2027/06-batch` | Installing Spark | `cohorts/2027/06-batch/03-installing-spark.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/06-batch` | First Look at Spark/PySpark | `cohorts/2027/06-batch/04-first-look-at-spark.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/06-batch` | Spark DataFrames | `cohorts/2027/06-batch/05-spark-dataframes.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | Preparing Yellow and Green Taxi Data | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | **YES** | 7 | 7 |
| DE | `cohorts/2027/06-batch` | SQL with Spark | `cohorts/2027/06-batch/07-sql-with-spark.md` | **YES** | 2 | 2 |
| DE | `cohorts/2027/06-batch` | Anatomy of a Spark Cluster | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | GroupBy in Spark | `cohorts/2027/06-batch/09-groupby-in-spark.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | Joins in Spark | `cohorts/2027/06-batch/10-joins-in-spark.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | Operations on Spark RDDs | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/06-batch` | Spark RDD mapPartition | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/06-batch` | Connecting to Google Cloud Storage | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | **YES** | 6 | 6 |
| DE | `cohorts/2027/06-batch` | Creating a Local Spark Cluster | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | **YES** | 5 | 5 |
| DE | `cohorts/2027/06-batch` | Setting up a Dataproc Cluster | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | **YES** | 4 | 4 |
| DE | `cohorts/2027/06-batch` | Connecting Spark to BigQuery | `cohorts/2027/06-batch/16-connecting-spark-to-bigquery.md` | **YES** | 3 | 3 |
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
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 14 | `images/01-what-is-ml-01-price-field-imagegen-pilot.png` | instructional illustration | PASS | 1816×866 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 28 | `images/01-what-is-ml-02-known-about-cars-imagegen-pilot.png` | instructional illustration | PASS | 1659×948 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 34 | `images/01-what-is-ml-03-expert-or-model-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 45 | `images/01-what-is-ml-04-features-target-imagegen-pilot.png` | instructional illustration | PASS | 1690×931 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 51 | `images/01-what-is-ml-05-model-training-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 59 | `images/01-what-is-ml-06-using-model-imagegen-pilot.png` | instructional illustration | PASS | 1751×898 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/01-what-is-ml.md` | 67 | `images/01-what-is-ml-07-suggest-price-imagegen-pilot.png` | instructional illustration | PASS | 1432×1098 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 14 | `images/02-ml-vs-rules-01-spam-examples-imagegen-pilot.png` | instructional illustration | PASS | 1626×967 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 25 | `images/02-ml-vs-rules-02-rules-imagegen-pilot.png` | instructional illustration | PASS | 1642×958 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 29 | `images/02-ml-vs-rules-03-more-spam-imagegen-pilot.png` | instructional illustration | PASS | 1629×965 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 58 | `images/02-ml-vs-rules-04-features-imagegen-pilot.png` | instructional illustration | PASS | 1628×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 66 | `images/02-ml-vs-rules-05-encode-email-imagegen-pilot.png` | instructional illustration | PASS | 1628×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 81 | `images/02-ml-vs-rules-06-predictions-imagegen-pilot.png` | instructional illustration | PASS | 1629×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 91 | `images/02-ml-vs-rules-07-rule-based-summary-imagegen-pilot.png` | instructional illustration | PASS | 1770×889 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/02-ml-vs-rules.md` | 95 | `images/02-ml-vs-rules-08-ml-summary-imagegen-pilot.png` | instructional illustration | PASS | 1537×1023 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 24 | `images/03-supervised-ml-01-features-target-imagegen-pilot.png` | instructional illustration | PASS | 1695×928 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 29 | `images/03-supervised-ml-02-feature-matrix-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 45 | `images/03-supervised-ml-03-predictions-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 55 | `images/03-supervised-ml-04-regression-imagegen-pilot.png` | instructional illustration | PASS | 1698×926 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 68 | `images/03-supervised-ml-05-multiclass-imagegen-pilot.png` | instructional illustration | PASS | 1695×928 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 76 | `images/03-supervised-ml-06-ranking-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/03-supervised-ml.md` | 88 | `images/03-supervised-ml-07-summary-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 12 | `images/04-crisp-dm-01-ml-projects-imagegen-pilot.png` | instructional illustration | PASS | 1627×967 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 20 | `images/04-crisp-dm-02-process-diagram-imagegen-pilot.png` | instructional illustration | PASS | 1628×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 26 | `images/04-crisp-dm-03-business-understanding-imagegen-pilot.png` | instructional illustration | PASS | 1628×966 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 57 | `images/04-crisp-dm-04-data-preparation-imagegen-pilot.png` | instructional illustration | PASS | 1693×929 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 61 | `images/04-crisp-dm-05-features-target-imagegen-pilot.png` | instructional illustration | PASS | 1635×962 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/04-crisp-dm.md` | 91 | `images/04-crisp-dm-06-summary-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 20 | `images/05-model-selection-01-train-validation-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 43 | `images/05-model-selection-02-multiple-comparisons-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 55 | `images/05-model-selection-03-train-valid-test-imagegen-pilot.png` | instructional illustration | PASS | 1619×971 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/05-model-selection.md` | 67 | `images/05-model-selection-04-select-and-test-imagegen-pilot.png` | instructional illustration | PASS | 1693×929 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 23 | `images/06-environment-01-create-repo-crisp.png` | instructional illustration | PASS | 1000×628 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 27 | `images/06-environment-02-create-codespace-crisp.png` | instructional illustration | PASS | 1040×644 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 33 | `images/06-environment-03-vscode-desktop-crisp.png` | instructional illustration | PASS | 1040×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 49 | `images/06-environment-04-push-pip-install-crisp.png` | instructional illustration | PASS | 1280×520 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 59 | `images/06-environment-05-jupyter-notebook-crisp.png` | instructional illustration | PASS | 1020×540 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 63 | `images/06-environment-06-homework-notebook-crisp.png` | homework/support | PASS | 1020×720 | reference checked; non-illustration asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 152 | `images/sample-jupyter-notebook-crisp.png` | instructional illustration | PASS | 1120×748 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 160 | `images/sample-code-crisp.png` | instructional illustration | PASS | 2790×1350 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 166 | `images/sample-data-file-crisp.png` | instructional illustration | PASS | 1000×818 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/06-environment.md` | 172 | `images/add-code-for-datafile-download-crisp.png` | instructional illustration | PASS | 3600×1320 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 44 | `images/07-numpy-01-zeros-ones-full-crisp.png` | instructional illustration | PASS | 1000×580 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 69 | `images/07-numpy-02-array-from-list-crisp.png` | instructional illustration | PASS | 1000×480 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 129 | `images/07-numpy-03-two-d-arrays-crisp.png` | instructional illustration | PASS | 1000×580 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 165 | `images/07-numpy-04-columns-crisp.png` | instructional illustration | PASS | 1000×500 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 191 | `images/07-numpy-05-random-seed-crisp.png` | instructional illustration | PASS | 1000×440 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 243 | `images/07-numpy-06-element-wise-crisp.png` | instructional illustration | PASS | 1000×400 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 273 | `images/07-numpy-07-comparison-crisp.png` | instructional illustration | PASS | 1000×370 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/07-numpy.md` | 313 | `images/07-numpy-08-summarizing-crisp.png` | instructional illustration | PASS | 1000×460 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 41 | `images/08-linear-algebra-01-vector-operations-crisp.png` | instructional illustration | PASS | 3360×1170 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 66 | `images/08-linear-algebra-02-dot-product-crisp.png` | instructional illustration | PASS | 2820×1602 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 101 | `images/08-linear-algebra-03-vector-vector-implementation-crisp.png` | instructional illustration | PASS | 3360×1278 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 118 | `images/08-linear-algebra-04-matrix-vector-idea-crisp.png` | instructional illustration | PASS | 2940×1710 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 168 | `images/08-linear-algebra-05-matrix-vector-implementation-crisp.png` | instructional illustration | PASS | 3360×1020 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 228 | `images/08-linear-algebra-06-matrix-matrix-crisp.png` | instructional illustration | PASS | 3360×1230 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 262 | `images/08-linear-algebra-07-identity-matrix-crisp.png` | instructional illustration | PASS | 3360×1158 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/08-linear-algebra.md` | 288 | `images/08-linear-algebra-08-inverse-crisp.png` | instructional illustration | PASS | 3360×1230 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 64 | `images/09-pandas-01-create-dataframe-crisp.png` | instructional illustration | PASS | 3360×1710 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 144 | `images/09-pandas-02-series-and-columns-crisp.png` | instructional illustration | PASS | 3360×1380 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 219 | `images/09-pandas-03-iloc-crisp.png` | instructional illustration | PASS | 3360×1470 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 288 | `images/09-pandas-04-filtering-crisp.png` | instructional illustration | PASS | 3360×1230 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 346 | `images/09-pandas-05-string-operations-crisp.png` | instructional illustration | PASS | 3360×1350 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 391 | `images/09-pandas-06-describe-crisp.png` | instructional illustration | PASS | 3360×1440 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 436 | `images/09-pandas-07-missing-values-crisp.png` | instructional illustration | PASS | 3360×1230 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/09-pandas.md` | 466 | `images/09-pandas-08-groupby-crisp.png` | instructional illustration | PASS | 3360×630 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 17 | `images/10-summary-01-features-target-model-imagegen-pilot.png` | instructional illustration | PASS | 1706×922 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 23 | `images/10-summary-02-rule-based-spam-rules-imagegen-pilot.png` | instructional illustration | PASS | 1716×917 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 27 | `images/10-summary-03-ml-training-data-imagegen-pilot.png` | instructional illustration | PASS | 1713×918 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 35 | `images/10-summary-04-supervised-g-x-y-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 41 | `images/10-summary-05-crisp-dm-bigger-picture-imagegen-pilot.png` | instructional illustration | PASS | 1254×1254 | review required: crisp/generated asset |
| ML | `cohorts/2026/01-intro/10-summary.md` | 47 | `images/10-summary-06-model-selection-split-imagegen-pilot.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 17 | `images/01-car-price-intro-01-select-best-price-crisp.png` | instructional illustration | PASS | 1008×672 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 26 | `images/01-car-price-intro-02-kaggle-dataset-crisp.png` | instructional illustration | PASS | 1078×492 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 31 | `images/01-car-price-intro-03-kaggle-data-explorer-crisp.png` | instructional illustration | PASS | 1152×566 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 39 | `images/01-car-price-intro-04-msrp-column-crisp.png` | instructional illustration | PASS | 1152×566 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 59 | `images/01-car-price-intro-05-project-plan-crisp.png` | instructional illustration | PASS | 970×634 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 68 | `images/01-car-price-intro-06-github-repo-crisp.png` | instructional illustration | PASS | 1060×566 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/01-car-price-intro.md` | 76 | `images/01-car-price-intro-07-chapter-files-crisp.png` | instructional illustration | PASS | 1092×136 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/02-data-preparation.md` | 28 | `images/02-data-preparation-01-download-data-crisp.png` | instructional illustration | PASS | 1154×612 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/02-data-preparation.md` | 48 | `images/02-data-preparation-02-read-csv-crisp.png` | instructional illustration | PASS | 1154×580 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/02-data-preparation.md` | 102 | `images/02-data-preparation-03-lowercase-columns-crisp.png` | instructional illustration | PASS | 1154×290 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/02-data-preparation.md` | 117 | `images/02-data-preparation-04-dtypes-crisp.png` | instructional illustration | PASS | 1154×560 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/02-data-preparation.md` | 151 | `images/02-data-preparation-05-string-columns-crisp.png` | instructional illustration | PASS | 1154×380 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/02-data-preparation.md` | 153 | `images/02-data-preparation-06-strings-list-crisp.png` | instructional illustration | PASS | 1154×460 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/02-data-preparation.md` | 173 | `images/02-data-preparation-07-normalize-values-crisp.png` | instructional illustration | PASS | 1154×392 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 56 | `images/03-eda-01-explore-columns-crisp.png` | instructional illustration | PASS | 1154×612 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 90 | `images/03-eda-02-import-plotting-libraries-crisp.png` | instructional illustration | PASS | 1154×272 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 101 | `images/03-eda-03-long-tail-distribution-crisp.png` | instructional illustration | PASS | 1154×510 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 122 | `images/03-eda-04-zoom-below-100k-crisp.png` | instructional illustration | PASS | 1154×430 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 148 | `images/03-eda-05-log-zero-problem-crisp.png` | instructional illustration | PASS | 1154×232 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 176 | `images/03-eda-06-log1p-normal-distribution-crisp.png` | instructional illustration | PASS | 1154×520 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/03-eda.md` | 226 | `images/03-eda-07-missing-values-crisp.png` | instructional illustration | PASS | 1154×560 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 25 | `images/04-validation-framework-01-train-val-test-split-crisp.png` | instructional illustration | PASS | 1610×977 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 59 | `images/04-validation-framework-02-split-sizes-crisp.png` | instructional illustration | PASS | 1154×418 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 89 | `images/04-validation-framework-03-sequential-split-crisp.png` | instructional illustration | PASS | 1154×612 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 102 | `images/04-validation-framework-04-shuffle-numbers-crisp.png` | instructional illustration | PASS | 1010×506 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 124 | `images/04-validation-framework-05-split-with-shuffled-idx-crisp.png` | instructional illustration | PASS | 1154×460 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 168 | `images/04-validation-framework-06-reset-index-crisp.png` | instructional illustration | PASS | 1154×596 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/04-validation-framework.md` | 200 | `images/04-validation-framework-07-y-target-and-delete-msrp-crisp.png` | instructional illustration | PASS | 1154×362 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/05-linear-regression-simple.md` | 34 | `images/05-linear-regression-simple-01-one-car-one-price-imagegen-pilot.png` | instructional illustration | PASS | 1474×1067 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/05-linear-regression-simple.md` | 51 | `images/05-linear-regression-simple-02-car-10-features-crisp.png` | instructional illustration | PASS | 2910×1410 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/05-linear-regression-simple.md` | 76 | `images/05-linear-regression-simple-03-regression-formula-crisp.png` | instructional illustration | PASS | 3192×2040 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/05-linear-regression-simple.md` | 84 | `images/05-linear-regression-simple-04-sum-notation-crisp.png` | instructional illustration | PASS | 2700×1020 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/05-linear-regression-simple.md` | 118 | `images/05-linear-regression-simple-05-implementation-crisp.png` | instructional illustration | PASS | 3192×1320 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/05-linear-regression-simple.md` | 134 | `images/05-linear-regression-simple-06-weights-interpretation-crisp.png` | instructional illustration | PASS | 3192×780 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/05-linear-regression-simple.md` | 176 | `images/05-linear-regression-simple-07-prediction-undo-log-crisp.png` | instructional illustration | PASS | 2880×1200 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 18 | `images/06-linear-regression-vector-01-g-x-approx-y-crisp.png` | instructional illustration | PASS | 2490×2040 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 34 | `images/06-linear-regression-vector-02-dot-product-notation-crisp.png` | instructional illustration | PASS | 2700×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 62 | `images/06-linear-regression-vector-03-dot-function-crisp.png` | instructional illustration | PASS | 2880×1020 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 76 | `images/06-linear-regression-vector-04-fake-feature-crisp.png` | instructional illustration | PASS | 2700×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 115 | `images/06-linear-regression-vector-05-prepend-one-crisp.png` | instructional illustration | PASS | 2880×1050 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 124 | `images/06-linear-regression-vector-06-matrix-vector-multiplication-crisp.png` | instructional illustration | PASS | 2820×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/06-linear-regression-vector.md` | 183 | `images/06-linear-regression-vector-07-x-dot-w-new-crisp.png` | instructional illustration | PASS | 2880×1218 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 37 | `images/07-linear-regression-training-01-inverse-solution-crisp.png` | instructional illustration | PASS | 2700×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 59 | `images/07-linear-regression-training-02-gram-matrix-crisp.png` | instructional illustration | PASS | 1440×1220 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 79 | `images/07-linear-regression-training-03-normal-equation-crisp.png` | instructional illustration | PASS | 2790×1680 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 113 | `images/07-linear-regression-training-04-gram-matrix-code-crisp.png` | instructional illustration | PASS | 3300×930 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 134 | `images/07-linear-regression-training-05-inverse-check-crisp.png` | instructional illustration | PASS | 3300×930 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 171 | `images/07-linear-regression-training-06-ones-column-stack-crisp.png` | instructional illustration | PASS | 2880×756 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/07-linear-regression-training.md` | 187 | `images/07-linear-regression-training-07-train-function-crisp.png` | instructional illustration | PASS | 3300×540 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/08-baseline-model.md` | 24 | `images/08-baseline-model-01-numerical-columns-crisp.png` | instructional illustration | PASS | 2880×1230 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/08-baseline-model.md` | 42 | `images/08-baseline-model-02-base-features-crisp.png` | instructional illustration | PASS | 2880×252 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/08-baseline-model.md` | 62 | `images/08-baseline-model-03-nan-weights-crisp.png` | instructional illustration | PASS | 2880×330 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/08-baseline-model.md` | 77 | `images/08-baseline-model-04-fillna-zero-crisp.png` | instructional illustration | PASS | 3120×960 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/08-baseline-model.md` | 90 | `images/08-baseline-model-05-missing-feature-ignored-crisp.png` | instructional illustration | PASS | 2700×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/08-baseline-model.md` | 134 | `images/08-baseline-model-06-prediction-histogram-crisp.png` | instructional illustration | PASS | 2880×1860 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/09-rmse.md` | 27 | `images/09-rmse-01-rmse-formula-crisp.png` | instructional illustration | PASS | 3390×1728 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/09-rmse.md` | 41 | `images/09-rmse-02-predictions-vs-actual-prices-crisp.png` | instructional illustration | PASS | 2892×2058 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/09-rmse.md` | 53 | `images/09-rmse-03-differences-crisp.png` | instructional illustration | PASS | 3150×2058 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/09-rmse.md` | 74 | `images/09-rmse-04-squared-errors-mean-crisp.png` | instructional illustration | PASS | 3150×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/09-rmse.md` | 129 | `images/09-rmse-06-rmse-implementation-crisp.png` | instructional illustration | PASS | 3390×1728 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/10-car-price-validation.md` | 22 | `images/10-car-price-validation-01-split-diagram-crisp.png` | instructional illustration | PASS | 1520×1040 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/10-car-price-validation.md` | 62 | `images/10-car-price-validation-02-prepare-x-function-crisp.png` | instructional illustration | PASS | 3198×540 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/10-car-price-validation.md` | 86 | `images/10-car-price-validation-03-train-and-validate-crisp.png` | instructional illustration | PASS | 3198×1242 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/10-car-price-validation.md` | 94 | `images/10-car-price-validation-04-train-vs-validation-parts-crisp.png` | instructional illustration | PASS | 3198×1242 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/11-feature-engineering.md` | 13 | `images/11-feature-engineering-01-feature-engineering-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 21 | `images/12-categorical-variables-01-object-columns-crisp.png` | instructional illustration | PASS | 3198×1608 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 41 | `images/12-categorical-variables-02-encoding-diagram.jpg` | local image | PASS | 1492×1054 | review required: native/source asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 92 | `images/12-categorical-variables-03-doors-loop-crisp.png` | instructional illustration | PASS | 3198×840 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 114 | `images/12-categorical-variables-04-doors-rmse-crisp.png` | instructional illustration | PASS | 3198×930 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 126 | `images/12-categorical-variables-05-top-makes-crisp.png` | instructional illustration | PASS | 3198×690 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 170 | `images/12-categorical-variables-06-categories-dict-crisp.png` | instructional illustration | PASS | 3198×810 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 183 | `images/12-categorical-variables-07-prepare-x-all-categories-crisp.png` | instructional illustration | PASS | 3198×810 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/12-categorical-variables.md` | 200 | `images/12-categorical-variables-08-broken-weights-crisp.png` | instructional illustration | PASS | 3198×1560 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 18 | `images/13-regularization-01-normal-equation-crisp.png` | instructional illustration | PASS | 920×680 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 45 | `images/13-regularization-02-duplicate-columns-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 76 | `images/13-regularization-03-noisy-gram-matrix-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 83 | `images/13-regularization-04-huge-weights-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 104 | `images/13-regularization-05-singular-matrix-crisp.png` | instructional illustration | PASS | 2880×1890 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 137 | `images/13-regularization-06-eye-diagonal-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 175 | `images/13-regularization-07-regularized-training-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/13-regularization.md` | 197 | `images/13-regularization-08-rmse-result-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/14-tuning-model.md` | 35 | `images/14-tuning-model-01-r-values-loop-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/14-tuning-model.md` | 39 | `images/14-tuning-model-02-rmse-per-r-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/14-tuning-model.md` | 53 | `images/14-tuning-model-03-choosing-r-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/14-tuning-model.md` | 70 | `images/14-tuning-model-04-final-model-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 36 | `images/15-using-model-01-full-train-concat-crisp.png` | instructional illustration | PASS | 3240×870 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 53 | `images/15-using-model-02-full-train-prepare-x-crisp.png` | instructional illustration | PASS | 2880×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 73 | `images/15-using-model-03-final-model-weights-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 94 | `images/15-using-model-04-test-rmse-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 134 | `images/15-using-model-06-car-dictionary-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 142 | `images/15-using-model-05-website-request-diagram-imagegen.png` | instructional illustration | PASS | 1521×1034 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 167 | `images/15-using-model-07-single-car-prediction-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/15-using-model.md` | 196 | `images/15-using-model-08-prediction-vs-actual-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/16-summary.md` | 27 | `images/16-summary-01-data-cleaning-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/16-summary.md` | 53 | `images/16-summary-03-linear-regression-loop-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/16-summary.md` | 55 | `images/16-summary-04-vector-form-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/16-summary.md` | 63 | `images/16-summary-05-normal-equation-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/16-summary.md` | 65 | `images/16-summary-06-baseline-model-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/16-summary.md` | 84 | `images/16-summary-07-feature-engineering-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/16-summary.md` | 91 | `images/16-summary-08-categorical-variables-crisp.png` | instructional illustration | PASS | 3300×1740 | review required: crisp/generated asset |
| ML | `cohorts/2026/02-regression/17-explore-more.md` | 4 | `images/17-explore-more-01-feature-experiments-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/01-churn-project.md` | 25 | `images/01-churn-project-01-churn-problem-crisp.png` | instructional illustration | PASS | 1196×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/01-churn-project.md` | 36 | `images/01-churn-project-02-binary-classification-crisp.png` | instructional illustration | PASS | 1196×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/01-churn-project.md` | 81 | `images/01-churn-project-03-module-plan-crisp.png` | instructional illustration | PASS | 984×642 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/02-data-preparation.md` | 33 | `images/02-data-preparation-01-download-data-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/02-data-preparation.md` | 91 | `images/02-data-preparation-02-first-look-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/02-data-preparation.md` | 118 | `images/02-data-preparation-03-normalized-crisp.png` | instructional illustration | PASS | 1100×616 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/02-data-preparation.md` | 147 | `images/02-data-preparation-04-totalcharges-error-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/02-data-preparation.md` | 173 | `images/02-data-preparation-05-coerce-missing-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/02-data-preparation.md` | 205 | `images/02-data-preparation-06-churn-encoding-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/03-validation.md` | 25 | `images/03-validation-01-train-val-test-split-crisp.png` | instructional illustration | PASS | 1042×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/03-validation.md` | 53 | `images/03-validation-02-split-sizes-crisp.png` | instructional illustration | PASS | 1100×644 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/03-validation.md` | 73 | `images/03-validation-03-reset-index-crisp.png` | instructional illustration | PASS | 1100×104 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/03-validation.md` | 98 | `images/03-validation-04-isolate-target-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/04-eda.md` | 54 | `images/04-eda-01-missing-values-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/04-eda.md` | 75 | `images/04-eda-02-churn-rate-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/04-eda.md` | 93 | `images/04-eda-03-churn-rate-mean-crisp.png` | instructional illustration | PASS | 1100×264 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/04-eda.md` | 110 | `images/04-eda-04-numerical-variables-crisp.png` | instructional illustration | PASS | 1100×64 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/04-eda.md` | 137 | `images/04-eda-05-categorical-variables-crisp.png` | instructional illustration | PASS | 1100×164 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/05-risk.md` | 39 | `images/05-risk-01-churn-rate-gender-crisp.png` | instructional illustration | PASS | 1100×588 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/05-risk.md` | 90 | `images/05-risk-02-churn-rate-partner-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/05-risk.md` | 113 | `images/05-risk-03-difference-vs-risk-ratio-imagegen-pilot.png` | instructional illustration | PASS | 1550×1014 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/05-risk.md` | 131 | `images/05-risk-04-risk-ratio-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/05-risk.md` | 194 | `images/05-risk-05-groupby-gender-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/05-risk.md` | 217 | `images/05-risk-06-groupby-contract-crisp.png` | instructional illustration | PASS | 1100×604 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/06-mutual-info.md` | 30 | `images/06-mutual-info-01-mutual-information-wikipedia-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/06-mutual-info.md` | 70 | `images/06-mutual-info-02-mutual-info-scores-crisp.png` | instructional illustration | PASS | 960×500 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/06-mutual-info.md` | 76 | `images/06-mutual-info-03-symmetric-crisp.png` | instructional illustration | PASS | 960×500 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/06-mutual-info.md` | 123 | `images/06-mutual-info-04-sorted-importance-crisp.png` | instructional illustration | PASS | 960×510 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 34 | `images/07-correlation-01-correlation-coefficient-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 42 | `images/07-correlation-02-binary-target-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 61 | `images/07-correlation-03-corrwith-churn-crisp.png` | instructional illustration | PASS | 960×210 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 137 | `images/07-correlation-04-churn-rate-tenure-clean.png` | local image | PASS | 1200×760 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/07-correlation.md` | 170 | `images/07-correlation-05-churn-rate-monthly-charges-clean.png` | local image | PASS | 1400×820 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/08-ohe.md` | 52 | `images/08-ohe-01-one-hot-table-crisp.png` | instructional illustration | PASS | 900×680 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/08-ohe.md` | 77 | `images/08-ohe-02-to-dict-records-crisp.png` | instructional illustration | PASS | 960×350 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/08-ohe.md` | 105 | `images/08-ohe-03-dictvectorizer-fit-crisp.png` | instructional illustration | PASS | 960×450 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/08-ohe.md` | 124 | `images/08-ohe-04-feature-names-crisp.png` | instructional illustration | PASS | 960×650 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/08-ohe.md` | 138 | `images/08-ohe-05-validation-transform-crisp.png` | instructional illustration | PASS | 960×450 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 33 | `images/09-logistic-regression-01-binary-classification-clean.png` | local image | PASS | 1300×760 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 57 | `images/09-logistic-regression-02-from-linear-to-logistic-clean.png` | local image | PASS | 1400×760 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 63 | `images/09-logistic-regression-03-sigmoid-formula-clean.png` | local image | PASS | 1300×820 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 98 | `images/09-logistic-regression-04-sigmoid-plot-crisp.png` | instructional illustration | PASS | 1488×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/09-logistic-regression.md` | 134 | `images/09-logistic-regression-05-logistic-regression-function-crisp.png` | instructional illustration | PASS | 960×410 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/10-training-log-reg.md` | 29 | `images/10-training-log-reg-01-fit-crisp.png` | instructional illustration | PASS | 2640×504 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/10-training-log-reg.md` | 59 | `images/10-training-log-reg-02-coefficients-crisp.png` | instructional illustration | PASS | 3030×918 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/10-training-log-reg.md` | 81 | `images/10-training-log-reg-03-soft-predictions-crisp.png` | instructional illustration | PASS | 1200×400 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/10-training-log-reg.md` | 90 | `images/10-training-log-reg-04-churn-decision-crisp.png` | instructional illustration | PASS | 3030×660 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/10-training-log-reg.md` | 97 | `images/10-training-log-reg-05-selected-customers-crisp.png` | instructional illustration | PASS | 3030×1320 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/10-training-log-reg.md` | 137 | `images/10-training-log-reg-06-accuracy-crisp.png` | instructional illustration | PASS | 3030×1320 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 32 | `images/11-log-reg-interpretation-01-zip-crisp.png` | instructional illustration | PASS | 3030×1818 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 55 | `images/11-log-reg-interpretation-02-coefficients-crisp.png` | instructional illustration | PASS | 3030×1200 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 110 | `images/11-log-reg-interpretation-03-small-features-crisp.png` | instructional illustration | PASS | 2940×1410 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 133 | `images/11-log-reg-interpretation-04-small-model-weights-crisp.png` | instructional illustration | PASS | 2940×1320 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 184 | `images/11-log-reg-interpretation-05-first-example-rendered.png` | local image | PASS | 1200×440 | review required: native/source asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 193 | `images/11-log-reg-interpretation-06-second-example-imagegen.png` | instructional illustration | PASS | 1793×877 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/11-log-reg-interpretation.md` | 195 | `images/11-log-reg-interpretation-07-second-example-crisp.png` | instructional illustration | PASS | 3030×1380 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/12-using-log-reg.md` | 34 | `images/12-using-log-reg-01-final-model-crisp.png` | instructional illustration | PASS | 2898×1170 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/12-using-log-reg.md` | 57 | `images/12-using-log-reg-02-test-accuracy-crisp.png` | instructional illustration | PASS | 3498×1320 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/12-using-log-reg.md` | 97 | `images/12-using-log-reg-03-score-one-customer-crisp.png` | instructional illustration | PASS | 3498×1500 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/12-using-log-reg.md` | 130 | `images/12-using-log-reg-04-production-diagram-imagegen.png` | instructional illustration | PASS | 1983×793 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/13-summary.md` | 10 | `images/13-summary-01-churn-prediction-imagegen.png` | instructional illustration | PASS | 1717×916 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/13-summary.md` | 40 | `images/13-summary-02-notebook-recap-crisp.png` | instructional illustration | PASS | 3408×1284 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/13-summary.md` | 50 | `images/13-summary-03-summary-takeaways-crisp.png` | instructional illustration | PASS | 3408×1410 | review required: crisp/generated asset |
| ML | `cohorts/2026/03-classification/14-explore-more.md` | 6 | `images/14-explore-more-01-preprocessing-model-comparison-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 11 | `images/01-overview-01-title-crisp.png` | instructional illustration | PASS | 956×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 17 | `images/01-overview-03-metric-definition-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 25 | `images/01-overview-02-churn-scenario-crisp.png` | instructional illustration | PASS | 956×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 56 | `images/01-overview-04-load-split-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 60 | `images/01-overview-05-features-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 70 | `images/01-overview-06-predictions-accuracy-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/01-overview.md` | 85 | `images/01-overview-07-module-outline-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 15 | `images/02-accuracy-02-accuracy-example-crisp.png` | instructional illustration | PASS | 1804×1360 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 31 | `images/02-accuracy-03-accuracy-notebook-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 43 | `images/02-accuracy-04-accuracy-score-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 88 | `images/02-accuracy-01-accuracy-vs-threshold-crisp.png` | instructional illustration | PASS | 1488×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 108 | `images/02-accuracy-05-dummy-counter-crisp.png` | instructional illustration | PASS | 1154×390 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 118 | `images/02-accuracy-06-dummy-accuracy-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 122 | `images/02-accuracy-07-thresholds-endpoints-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/02-accuracy.md` | 128 | `images/02-accuracy-08-class-imbalance-crisp.png` | instructional illustration | PASS | 902×680 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 24 | `images/03-confusion-table-01-four-outcomes-crisp.png` | instructional illustration | PASS | 1036×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 39 | `images/03-confusion-table-02-prediction-conditions-crisp.png` | instructional illustration | PASS | 1154×612 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 51 | `images/03-confusion-table-03-and-operator-crisp.png` | instructional illustration | PASS | 1154×612 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 55 | `images/03-confusion-table-04-confusion-counts-crisp.png` | instructional illustration | PASS | 1044×680 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 76 | `images/03-confusion-table-05-confusion-matrix-output-crisp.png` | instructional illustration | PASS | 1154×612 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 96 | `images/03-confusion-table-06-normalized-confusion-matrix-crisp.png` | instructional illustration | PASS | 1154×612 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/03-confusion-table.md` | 102 | `images/03-confusion-table-07-accuracy-from-table-crisp.png` | instructional illustration | PASS | 1044×680 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 19 | `images/04-precision-recall-01-precision-definition-crisp.png` | instructional illustration | PASS | 1472×1069 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 30 | `images/04-precision-recall-02-precision-notebook-crisp.png` | instructional illustration | PASS | 1154×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 34 | `images/04-precision-recall-03-precision-pie-crisp.png` | instructional illustration | PASS | 816×430 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 44 | `images/04-precision-recall-04-recall-definition-crisp.png` | instructional illustration | PASS | 916×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 57 | `images/04-precision-recall-05-recall-example-crisp.png` | instructional illustration | PASS | 800×710 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 63 | `images/04-precision-recall-06-precision-recall-table-crisp.png` | instructional illustration | PASS | 996×640 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/04-precision-recall.md` | 67 | `images/04-precision-recall-07-metrics-summary-crisp.png` | instructional illustration | PASS | 880×660 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 75 | `images/05-roc-01-tpr-fpr-vs-threshold-crisp.png` | instructional illustration | PASS | 1488×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 88 | `images/05-roc-02-random-model-tpr-fpr-crisp.png` | instructional illustration | PASS | 1488×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 112 | `images/05-roc-03-ideal-model-tpr-fpr-crisp.png` | instructional illustration | PASS | 1488×992 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 130 | `images/05-roc-04-model-vs-ideal-tpr-fpr-crisp.png` | instructional illustration | PASS | 1552×1056 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 148 | `images/05-roc-05-roc-curve-manual-crisp.png` | instructional illustration | PASS | 1384×1332 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/05-roc.md` | 176 | `images/05-roc-06-roc-curve-sklearn-crisp.png` | instructional illustration | PASS | 1384×1332 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/06-auc.md` | 22 | `images/06-auc-02-auc-values-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/06-auc.md` | 34 | `images/06-auc-03-auc-notebook-crisp.png` | instructional illustration | PASS | 3462×1752 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/06-auc.md` | 46 | `images/06-auc-04-roc-auc-score-crisp.png` | instructional illustration | PASS | 3462×1752 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/06-auc.md` | 54 | `images/06-auc-05-auc-interpretation-imagegen.png` | instructional illustration | PASS | 1572×1001 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/06-auc.md` | 81 | `images/06-auc-06-auc-simulation-crisp.png` | instructional illustration | PASS | 3030×1680 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/07-cross-validation.md` | 42 | `images/07-cross-validation-02-train-predict-crisp.png` | instructional illustration | PASS | 3030×1110 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/07-cross-validation.md` | 48 | `images/07-cross-validation-01-kfold-diagram-pilot.png` | local image | PASS | 1555×1012 | review required: native/source asset |
| ML | `cohorts/2026/04-evaluation/07-cross-validation.md` | 60 | `images/07-cross-validation-03-split-generator-crisp.png` | instructional illustration | PASS | 3030×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/07-cross-validation.md` | 88 | `images/07-cross-validation-04-tuning-loop-crisp.png` | instructional illustration | PASS | 3030×1710 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/07-cross-validation.md` | 102 | `images/07-cross-validation-05-tuning-results-crisp.png` | instructional illustration | PASS | 3030×1080 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/07-cross-validation.md` | 134 | `images/07-cross-validation-06-final-model-crisp.png` | instructional illustration | PASS | 3030×1680 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/08-summary.md` | 17 | `images/08-summary-01-metrics-list-crisp.png` | instructional illustration | PASS | 3462×930 | review required: crisp/generated asset |
| ML | `cohorts/2026/04-evaluation/09-explore-more.md` | 6 | `images/09-explore-more-01-threshold-precision-recall-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 10 | `images/01-intro-01-title-crisp.png` | instructional illustration | PASS | 864×672 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 31 | `images/01-intro-02-model-deployment-diagram-imagegen-pilot.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 38 | `images/01-intro-03-module-plan-crisp.png` | instructional illustration | PASS | 910×600 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 53 | `images/01-intro-04-module-plan-continued-crisp.png` | instructional illustration | PASS | 910×600 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/01-intro.md` | 59 | `images/01-intro-05-environments-crisp.png` | instructional illustration | PASS | 1478×1064 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/02-pickle.md` | 13 | `images/02-pickle-01-module-plan-crisp.png` | instructional illustration | PASS | 1020×572 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/02-pickle.md` | 42 | `images/02-pickle-02-pickle-dump-crisp.png` | instructional illustration | PASS | 1070×614 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/02-pickle.md` | 49 | `images/02-pickle-03-model-filename-crisp.png` | instructional illustration | PASS | 1070×590 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/02-pickle.md` | 70 | `images/02-pickle-04-loaded-model-crisp.png` | instructional illustration | PASS | 1070×590 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/02-pickle.md` | 89 | `images/02-pickle-05-train-py-crisp.png` | instructional illustration | PASS | 1020×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/03-flask-intro.md` | 12 | `images/03-flask-intro-01-module-overview-crisp.png` | instructional illustration | PASS | 928×688 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/03-flask-intro.md` | 21 | `images/03-flask-intro-02-request-response-crisp.png` | instructional illustration | PASS | 928×600 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/03-flask-intro.md` | 55 | `images/03-flask-intro-03-ping-app-crisp.png` | instructional illustration | PASS | 920×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/04-flask-deployment.md` | 15 | `images/04-flask-deployment-01-module-plan-crisp.png` | instructional illustration | PASS | 920×572 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/04-flask-deployment.md` | 57 | `images/04-flask-deployment-02-predict-py-crisp.png` | instructional illustration | PASS | 920×584 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/04-flask-deployment.md` | 75 | `images/04-flask-deployment-03-json-serializable-error-crisp.png` | instructional illustration | PASS | 960×546 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/04-flask-deployment.md` | 113 | `images/04-flask-deployment-04-test-request-crisp.png` | instructional illustration | PASS | 960×200 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/04-flask-deployment.md` | 127 | `images/04-flask-deployment-05-dev-server-warning-crisp.png` | instructional illustration | PASS | 922×374 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/04-flask-deployment.md` | 148 | `images/04-flask-deployment-06-waitress-windows-crisp.png` | instructional illustration | PASS | 900×380 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 13 | `images/05-pipenv-01-title-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 23 | `images/05-pipenv-02-version-conflict-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 29 | `images/05-pipenv-03-isolated-environments-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 36 | `images/05-pipenv-04-venv-tools-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 84 | `images/05-pipenv-05-pipenv-install-lock-crisp.png` | instructional illustration | PASS | 2754×1680 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/05-pipenv.md` | 104 | `images/05-pipenv-06-shell-path-crisp.png` | instructional illustration | PASS | 2670×870 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/06-docker.md` | 13 | `images/06-docker-01-module-plan-crisp.png` | instructional illustration | PASS | 2724×750 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/06-docker.md` | 51 | `images/06-docker-02-containers-on-host-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/06-docker.md` | 77 | `images/06-docker-03-base-image-docker-hub-crisp.png` | instructional illustration | PASS | 3030×630 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/06-docker.md` | 108 | `images/06-docker-04-dockerfile-crisp.png` | instructional illustration | PASS | 2700×1650 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/06-docker.md` | 133 | `images/06-docker-05-port-mapping-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 9 | `images/07-aws-eb-01-module-plan-crisp.png` | instructional illustration | PASS | 2724×750 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 31 | `images/07-aws-eb-02-eb-architecture-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 54 | `images/07-aws-eb-03-eb-init-crisp.png` | instructional illustration | PASS | 2580×1440 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 64 | `images/07-aws-eb-04-eb-local-test-crisp.png` | instructional illustration | PASS | 2502×1140 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 73 | `images/07-aws-eb-05-eb-create-crisp.png` | instructional illustration | PASS | 2580×1230 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 81 | `images/07-aws-eb-06-eb-url-test-crisp.png` | instructional illustration | PASS | 3318×1560 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/07-aws-eb.md` | 93 | `images/07-aws-eb-07-terminate-environment-crisp.png` | instructional illustration | PASS | 3588×1470 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/08-summary.md` | 10 | `images/08-summary-01-module-plan-crisp.png` | instructional illustration | PASS | 2730×1800 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/08-summary.md` | 32 | `images/08-summary-02-module-plan-continued-crisp.png` | instructional illustration | PASS | 2730×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/08-summary.md` | 42 | `images/08-summary-03-summary-list-crisp.png` | instructional illustration | PASS | 2730×840 | review required: crisp/generated asset |
| ML | `cohorts/2026/05-deployment/09-explore-more.md` | 6 | `images/09-explore-more-01-deployment-choices-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 24 | `images/01-credit-risk-01-loan-application-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 32 | `images/01-credit-risk-02-historical-data-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 60 | `images/01-credit-risk-03-probability-of-default-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 69 | `images/01-credit-risk-04-dataset-columns-crisp.png` | instructional illustration | PASS | 860×660 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/01-credit-risk.md` | 89 | `images/01-credit-risk-05-module-plan-crisp.png` | instructional illustration | PASS | 1000×640 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/02-data-prep.md` | 40 | `images/02-data-prep-01-download-data-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/02-data-prep.md` | 93 | `images/02-data-prep-02-decode-status-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/02-data-prep.md` | 176 | `images/02-data-prep-03-encoded-missing-values-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/02-data-prep.md` | 189 | `images/02-data-prep-04-replace-missing-with-nan-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/02-data-prep.md` | 200 | `images/02-data-prep-05-remove-unknown-status-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/02-data-prep.md` | 220 | `images/02-data-prep-06-train-val-test-split-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/02-data-prep.md` | 239 | `images/02-data-prep-07-binary-target-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 37 | `images/03-decision-trees-01-risk-rules-tree-imagegen.png` | instructional illustration | PASS | 1705×923 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 51 | `images/03-decision-trees-02-assess-risk-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 88 | `images/03-decision-trees-03-training-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 118 | `images/03-decision-trees-04-overfit-auc-crisp.png` | instructional illustration | PASS | 1152×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 126 | `images/03-decision-trees-05-memorizing-imagegen.png` | instructional illustration | PASS | 1363×1154 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 185 | `images/03-decision-trees-06-learned-rules-imagegen.png` | instructional illustration | PASS | 1704×923 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/03-decision-trees.md` | 191 | `images/03-decision-trees-07-decision-stump-imagegen.png` | instructional illustration | PASS | 1364×1153 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 52 | `images/04-decision-tree-learning-01-best-threshold-crisp.png` | instructional illustration | PASS | 1000×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 60 | `images/04-decision-tree-learning-02-candidate-thresholds-crisp.png` | instructional illustration | PASS | 1000×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 84 | `images/04-decision-tree-learning-03-split-t4000-crisp.png` | instructional illustration | PASS | 1000×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 90 | `images/04-decision-tree-learning-04-misclassification-rate-crisp.png` | instructional illustration | PASS | 1000×570 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 183 | `images/04-decision-tree-learning-06-split-algorithm-crisp.png` | instructional illustration | PASS | 910×660 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 191 | `images/04-decision-tree-learning-07-impurity-criteria-crisp.png` | instructional illustration | PASS | 1000×720 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/04-decision-tree-learning.md` | 205 | `images/04-decision-tree-learning-08-stopping-criteria-imagegen.png` | instructional illustration | PASS | 1473×1068 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 25 | `images/05-decision-tree-tuning-01-parameters-crisp.png` | instructional illustration | PASS | 2820×1710 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 65 | `images/05-decision-tree-tuning-02-max-depth-scores-crisp.png` | instructional illustration | PASS | 1581×995 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 87 | `images/05-decision-tree-tuning-03-grid-search-crisp.png` | instructional illustration | PASS | 1040×480 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 119 | `images/05-decision-tree-tuning-04-pivot-crisp.png` | instructional illustration | PASS | 1400×940 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 127 | `images/05-decision-tree-tuning-05-heatmap-crisp.png` | instructional illustration | PASS | 1320×840 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 140 | `images/05-decision-tree-tuning-07-wider-search-crisp.png` | instructional illustration | PASS | 1440×840 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/05-decision-tree-tuning.md` | 182 | `images/05-decision-tree-tuning-06-nan-warning-crisp.png` | instructional illustration | PASS | 1440×560 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 26 | `images/06-random-forest-01-board-of-experts-imagegen.png` | instructional illustration | PASS | 1495×1052 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 58 | `images/06-random-forest-02-random-forest-imagegen.png` | instructional illustration | PASS | 1492×1054 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 87 | `images/06-random-forest-03-auc-vs-trees-crisp.png` | instructional illustration | PASS | 4080×3000 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 133 | `images/06-random-forest-04-tuning-max-depth-crisp.png` | instructional illustration | PASS | 4080×3120 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/06-random-forest.md` | 186 | `images/06-random-forest-05-tuning-min-samples-leaf-crisp.png` | instructional illustration | PASS | 4080×3120 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/07-boosting.md` | 27 | `images/07-boosting-01-boosting-vs-random-forest-imagegen.png` | instructional illustration | PASS | 1493×1054 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/07-boosting.md` | 32 | `images/07-boosting-02-gradient-boosting-trees-imagegen.png` | instructional illustration | PASS | 1496×1051 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/07-boosting.md` | 187 | `images/07-boosting-03-train-val-auc-crisp.png` | instructional illustration | PASS | 4080×3000 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 24 | `images/08-xgb-tuning-01-parameters-imagegen.png` | instructional illustration | PASS | 1529×1029 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 81 | `images/08-xgb-tuning-02-tuning-eta-crisp.png` | instructional illustration | PASS | 4080×3000 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 114 | `images/08-xgb-tuning-03-max-depth-curves-crisp.png` | instructional illustration | PASS | 3456×2268 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/08-xgb-tuning.md` | 152 | `images/08-xgb-tuning-04-min-child-weight-curves-crisp.png` | instructional illustration | PASS | 3519×2268 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 19 | `images/09-final-model-01-comparing-validation-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 57 | `images/09-final-model-02-tuned-random-forest-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 88 | `images/09-final-model-03-xgb-validation-auc-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 111 | `images/09-final-model-04-full-train-prep-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 127 | `images/09-final-model-05-feature-matrices-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 136 | `images/09-final-model-06-dmatrix-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/09-final-model.md` | 166 | `images/09-final-model-07-final-test-auc-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 14 | `images/10-summary-01-summary-slide-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 25 | `images/10-summary-02-decision-tree-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 27 | `images/10-summary-03-overfitting-auc-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 37 | `images/10-summary-04-random-forest-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 45 | `images/10-summary-05-gradient-boosting-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
| ML | `cohorts/2026/06-trees/10-summary.md` | 47 | `images/10-summary-06-xgb-parameters-crisp.png` | instructional illustration | PASS | 1600×900 | review required: crisp/generated asset |
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
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 25 | `images/03-pretrained-models-02-imagenet-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 36 | `images/03-pretrained-models-01-keras-applications-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 54 | `images/03-pretrained-models-03-sagemaker-gpu-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 88 | `images/03-pretrained-models-04-xception-model-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 93 | `images/03-pretrained-models-05-xception-weights-download-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 108 | `images/03-pretrained-models-06-batch-shape-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 125 | `images/03-pretrained-models-07-preprocess-input-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/03-pretrained-models.md` | 152 | `images/03-pretrained-models-08-decode-predictions-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
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
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 22 | `images/07-checkpointing-01-oscillation-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 44 | `images/07-checkpointing-02-callbacks-imagegen.png` | instructional illustration | PASS | 1508×1043 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 87 | `images/07-checkpointing-03-filename-template-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 98 | `images/07-checkpointing-04-save-best-only-imagegen.png` | instructional illustration | PASS | 1508×1043 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 127 | `images/07-checkpointing-05-checkpoint-and-fit-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 135 | `images/07-checkpointing-06-checkpoint-files-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/07-checkpointing.md` | 149 | `images/07-checkpointing-07-best-model-crisp.png` | instructional illustration | PASS | 3000×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 28 | `images/08-more-layers-01-inner-layer-diagram-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 39 | `images/08-more-layers-02-activation-functions-crisp.png` | instructional illustration | PASS | 2880×2160 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 80 | `images/08-more-layers-03-relu-in-code-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 103 | `images/08-more-layers-04-tuning-sizes-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 109 | `images/08-more-layers-05-nvidia-smi-crisp.png` | instructional illustration | PASS | 3300×1794 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/08-more-layers.md` | 128 | `images/08-more-layers-06-val-accuracy-plot-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 25 | `images/09-dropout-01-motivation-logo-imagegen.png` | instructional illustration | PASS | 1696×927 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 35 | `images/09-dropout-02-hiding-input-imagegen.png` | instructional illustration | PASS | 1024×1536 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 43 | `images/09-dropout-03-frozen-neuron-imagegen.png` | instructional illustration | PASS | 1693×929 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 90 | `images/09-dropout-04-v3-diagram-imagegen.png` | instructional illustration | PASS | 1817×866 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 127 | `images/09-dropout-05-tuning-dropout-crisp.png` | instructional illustration | PASS | 3000×2076 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 137 | `images/09-dropout-07-dropout-02-vs-train-crisp.png` | instructional illustration | PASS | 3000×2076 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 154 | `images/09-dropout-06-val-accuracy-dropout-crisp.png` | instructional illustration | PASS | 3000×2076 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/09-dropout.md` | 169 | `images/09-dropout-08-no-regularization-overfit-crisp.png` | instructional illustration | PASS | 3000×2076 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 15 | `images/10-augmentation-01-generate-more-images-imagegen.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 27 | `images/10-augmentation-02-flip-rotation-shift-grids-crisp.png` | instructional illustration | PASS | 3000×2088 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 29 | `images/10-augmentation-03-zoom-grid-crisp.png` | instructional illustration | PASS | 3000×2088 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 51 | `images/10-augmentation-04-keras-parameters-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 129 | `images/10-augmentation-05-nvidia-smi-cpu-bound-crisp.png` | instructional illustration | PASS | 3300×1782 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/10-augmentation.md` | 131 | `images/10-augmentation-06-val-stuck-077-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/11-large-model.md` | 22 | `images/11-large-model-01-input-size-parameter-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/11-large-model.md` | 75 | `images/11-large-model-02-generators-shear-zoom-flip-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/11-large-model.md` | 111 | `images/11-large-model-03-checkpoint-callback-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/11-large-model.md` | 136 | `images/11-large-model-04-first-run-step-time-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/11-large-model.md` | 163 | `images/11-large-model-05-training-output-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/11-large-model.md` | 168 | `images/11-large-model-06-checkpoint-files-crisp.png` | instructional illustration | PASS | 3300×1782 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/12-using-model.md` | 36 | `images/12-using-model-01-fresh-notebook-imports-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/12-using-model.md` | 75 | `images/12-using-model-02-load-model-evaluate-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/12-using-model.md` | 98 | `images/12-using-model-03-load-img-pants-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/12-using-model.md` | 112 | `images/12-using-model-04-numpy-batch-shape-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/12-using-model.md` | 156 | `images/12-using-model-05-classes-prediction-zip-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/13-summary.md` | 9 | `images/13-summary-01-use-case-diagram-imagegen.png` | instructional illustration | PASS | 1774×887 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/13-summary.md` | 30 | `images/13-summary-03-explore-more-crisp.png` | instructional illustration | PASS | 3000×2040 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/13-summary.md` | 36 | `images/13-summary-02-final-predictions-crisp.png` | instructional illustration | PASS | 3000×2082 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/14-explore-more.md` | 5 | `images/14-explore-more-01-learning-paths-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/08-deep-learning/install.md` | 9 | `images/install-01-gpu-stack-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 25 | `images/01-intro-01-clothes-classification-use-case-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 44 | `images/01-intro-02-aws-lambda-deployment-imagegen.png` | instructional illustration | PASS | 1691×930 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 51 | `images/01-intro-03-lambda-uses-tf-lite-imagegen.png` | instructional illustration | PASS | 1835×857 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 57 | `images/01-intro-04-module-plan-crisp.png` | instructional illustration | PASS | 3000×2016 | review required: crisp/generated asset |
| ML | `cohorts/2026/09-serverless/01-intro.md` | 69 | `images/01-intro-05-module-plan-lambda-gateway-crisp.png` | instructional illustration | PASS | 3000×2016 | review required: crisp/generated asset |
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
| ML | `cohorts/2026/09-serverless/03-tensorflow-lite.md` | 221 | `images/03-tensorflow-lite-06-keras-preprocess-source-crisp.png` | instructional illustration | PASS | 3000×720 | review required: crisp/generated asset |
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
| ML | `cohorts/2026/10-kubernetes/02-tensorflow-serving.md` | 39 | `images/02-tensorflow-serving-01-saved-model-crisp.png` | instructional illustration | PASS | 2760×1530 | review required: crisp/generated asset |
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
| MLOps | `06-best-practices/README.md` | 48 | `AWS-stream-pipeline.png` | local image | PASS | 1760×1144 | review required: native/source asset |
| MLOps | `06-best-practices/README.md` | 93 | `ci_cd_zoomcamp.png` | local image | PASS | 1870×1322 | review required: native/source asset |
| MLOps | `07-project/README.md` | 104 | `https://static.streamlit.io/badges/streamlit_badge_black_white.svg` | remote | REMOTE | — | not locally checked |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 40 | `images/01-data-warehouse-and-bigquery-01-olap-vs-oltp-crisp.png` | instructional illustration | PASS | 1666×944 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 60 | `images/01-data-warehouse-and-bigquery-02-data-warehouse-diagram-imagegen.png` | instructional illustration | PASS | 1693×929 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 105 | `images/01-data-warehouse-and-bigquery-03-bigquery-cost-crisp.png` | instructional illustration | PASS | 1680×660 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 170 | `images/01-data-warehouse-and-bigquery-04-external-table-details-crisp.png` | instructional illustration | PASS | 1836×990 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 198 | `images/01-data-warehouse-and-bigquery-05-partitioning-diagram-crisp.png` | instructional illustration | PASS | 1800×1005 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 242 | `images/01-data-warehouse-and-bigquery-06-partition-pruning-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 276 | `images/01-data-warehouse-and-bigquery-07-clustering-diagram-crisp.png` | instructional illustration | PASS | 1800×1005 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/01-data-warehouse-and-bigquery.md` | 315 | `images/01-data-warehouse-and-bigquery-08-cluster-pruning-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/02-partitioning-vs-clustering.md` | 38 | `images/02-partitioning-vs-clustering-01-partitioning-options-crisp.png` | instructional illustration | PASS | 1800×900 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/02-partitioning-vs-clustering.md` | 52 | `images/02-partitioning-vs-clustering-02-clustering-basics-crisp.png` | instructional illustration | PASS | 1800×855 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/02-partitioning-vs-clustering.md` | 92 | `images/02-partitioning-vs-clustering-03-partitioning-vs-clustering-crisp.png` | instructional illustration | PASS | 1800×900 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/02-partitioning-vs-clustering.md` | 106 | `images/02-partitioning-vs-clustering-04-clustering-over-partitioning-crisp.png` | instructional illustration | PASS | 1800×855 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/02-partitioning-vs-clustering.md` | 124 | `images/02-partitioning-vs-clustering-05-automatic-reclustering-crisp.png` | instructional illustration | PASS | 1800×900 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/03-bigquery-best-practices.md` | 15 | `images/03-bigquery-best-practices-01-cost-reduction-crisp.png` | instructional illustration | PASS | 1800×600 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/03-bigquery-best-practices.md` | 44 | `images/03-bigquery-best-practices-02-query-performance-crisp.png` | instructional illustration | PASS | 1800×735 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/03-bigquery-best-practices.md` | 70 | `images/03-bigquery-best-practices-03-join-patterns-crisp.png` | instructional illustration | PASS | 1800×750 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | 13 | `images/04-internals-of-bigquery-01-architecture-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | 52 | `images/04-internals-of-bigquery-02-columnar-storage-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/04-internals-of-bigquery.md` | 74 | `images/04-internals-of-bigquery-03-dremel-tree-imagegen.png` | instructional illustration | PASS | 1672×941 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 66 | `images/05-machine-learning-in-bigquery-01-model-choice-crisp.png` | instructional illustration | PASS | 1800×1050 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 143 | `images/05-machine-learning-in-bigquery-02-feature-table-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 172 | `images/05-machine-learning-in-bigquery-03-model-evaluation-tab-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 185 | `images/05-machine-learning-in-bigquery-04-feature-info-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 212 | `images/05-machine-learning-in-bigquery-05-ml-evaluate-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 238 | `images/05-machine-learning-in-bigquery-06-ml-predict-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 266 | `images/05-machine-learning-in-bigquery-07-explain-predict-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/05-machine-learning-in-bigquery.md` | 298 | `images/05-machine-learning-in-bigquery-08-hyperparameter-tuning-crisp.png` | instructional illustration | PASS | 1836×975 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 26 | `images/06-deploying-a-machine-learning-model-01-exported-to-gcs-crisp.png` | instructional illustration | PASS | 1920×996 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 40 | `images/06-deploying-a-machine-learning-model-02-copy-model-local-crisp.png` | instructional illustration | PASS | 1884×1020 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 65 | `images/06-deploying-a-machine-learning-model-03-docker-running-crisp.png` | instructional illustration | PASS | 1884×1020 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 73 | `images/06-deploying-a-machine-learning-model-04-model-status-crisp.png` | instructional illustration | PASS | 1725×945 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 91 | `images/06-deploying-a-machine-learning-model-05-predict-crisp.png` | instructional illustration | PASS | 1725×945 | review required: crisp/generated asset |
| DE | `cohorts/2027/03-data-warehouse/06-deploying-a-machine-learning-model.md` | 96 | `images/06-deploying-a-machine-learning-model-06-predict-payment-type-2-crisp.png` | instructional illustration | PASS | 1725×945 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 32 | `images/01-introduction-to-batch-processing-01-batch-vs-streaming-imagegen.png` | instructional illustration | PASS | 1601×982 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 46 | `images/01-introduction-to-batch-processing-02-streaming-example-imagegen.png` | instructional illustration | PASS | 1133×1388 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 62 | `images/01-introduction-to-batch-processing-03-batch-job-frequencies-imagegen.png` | instructional illustration | PASS | 1254×1254 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 78 | `images/01-introduction-to-batch-processing-04-technologies-imagegen.png` | instructional illustration | PASS | 1470×1070 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 106 | `images/01-introduction-to-batch-processing-06-advantages-imagegen.png` | instructional illustration | PASS | 1117×1409 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/01-introduction-to-batch-processing.md` | 122 | `images/01-introduction-to-batch-processing-07-batch-vs-streaming-share-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/02-introduction-to-spark.md` | 26 | `images/02-introduction-to-spark-02-data-processing-engine-whiteboard-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/02-introduction-to-spark.md` | 62 | `images/02-introduction-to-spark-03-when-to-use-spark-whiteboard-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/02-introduction-to-spark.md` | 87 | `images/02-introduction-to-spark-04-typical-workflow-whiteboard-imagegen.png` | instructional illustration | PASS | 1627×967 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 22 | `images/03-installing-spark-01-install-guide-java-crisp.png` | instructional illustration | PASS | 1395×435 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 45 | `images/03-installing-spark-02-java-home-crisp.png` | instructional illustration | PASS | 1428×888 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 71 | `images/03-installing-spark-03-spark-download-page-crisp.png` | instructional illustration | PASS | 1470×915 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 80 | `images/03-installing-spark-04-spark-home-crisp.png` | instructional illustration | PASS | 1428×888 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/03-installing-spark.md` | 107 | `images/03-installing-spark-05-spark-shell-crisp.png` | instructional illustration | PASS | 1428×888 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 38 | `images/04-first-look-at-spark-01-spark-ui-crisp.png` | instructional illustration | PASS | 1440×960 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 79 | `images/04-first-look-at-spark-02-schema-problem-pandas-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 123 | `images/04-first-look-at-spark-03-schema-structtype-crisp.png` | instructional illustration | PASS | 1365×867 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 149 | `images/04-first-look-at-spark-04-partitions-slides-imagegen.png` | instructional illustration | PASS | 1402×1122 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/04-first-look-at-spark.md` | 179 | `images/04-first-look-at-spark-05-repartition-write-parquet-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 26 | `images/05-spark-dataframes-01-print-schema-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 43 | `images/05-spark-dataframes-02-select-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 108 | `images/05-spark-dataframes-03-built-in-functions-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/05-spark-dataframes.md` | 169 | `images/05-spark-dataframes-04-udf-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 44 | `images/06-preparing-taxi-data-03-printf-crisp.png` | instructional illustration | PASS | 1314×882 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 49 | `images/06-preparing-taxi-data-02-url-list-crisp.png` | instructional illustration | PASS | 1314×882 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 85 | `images/06-preparing-taxi-data-04-zcat-crisp.png` | instructional illustration | PASS | 1314×882 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 90 | `images/06-preparing-taxi-data-05-tree-raw-crisp.png` | instructional illustration | PASS | 1314×882 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 110 | `images/06-preparing-taxi-data-06-schema-strings-crisp.png` | instructional illustration | PASS | 1410×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 175 | `images/06-preparing-taxi-data-07-spark-ui-one-task-crisp.png` | instructional illustration | PASS | 1500×936 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/06-preparing-taxi-data.md` | 184 | `images/06-preparing-taxi-data-08-tree-pq-crisp.png` | instructional illustration | PASS | 1314×870 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/07-sql-with-spark.md` | 36 | `images/07-sql-with-spark-01-read-parquet-crisp.png` | instructional illustration | PASS | 1395×924 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/07-sql-with-spark.md` | 50 | `images/07-sql-with-spark-02-common-columns-crisp.png` | instructional illustration | PASS | 1395×924 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 50 | `images/08-anatomy-of-a-spark-cluster-01-spark-submit-master-imagegen.png` | instructional illustration | PASS | 1448×1086 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 56 | `images/08-anatomy-of-a-spark-cluster-02-executors-failure-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 67 | `images/08-anatomy-of-a-spark-cluster-03-executors-pull-partitions-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/08-anatomy-of-a-spark-cluster.md` | 94 | `images/08-anatomy-of-a-spark-cluster-04-s3-gcs-instead-of-hdfs-imagegen.png` | instructional illustration | PASS | 1539×1022 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/09-groupby-in-spark.md` | 38 | `images/09-groupby-in-spark-01-revenue-query-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/09-groupby-in-spark.md` | 56 | `images/09-groupby-in-spark-02-three-stages-crisp.png` | instructional illustration | PASS | 1440×984 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/09-groupby-in-spark.md` | 122 | `images/09-groupby-in-spark-03-reshuffling-whiteboard-imagegen.png` | instructional illustration | PASS | 1569×1002 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/09-groupby-in-spark.md` | 160 | `images/09-groupby-in-spark-04-shuffle-read-write-crisp.png` | instructional illustration | PASS | 1440×984 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/10-joins-in-spark.md` | 24 | `images/10-joins-in-spark-01-outer-join-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/10-joins-in-spark.md` | 61 | `images/10-joins-in-spark-02-sort-merge-join-stages-crisp.png` | instructional illustration | PASS | 1440×984 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/10-joins-in-spark.md` | 141 | `images/10-joins-in-spark-03-zones-lookup-crisp.png` | instructional illustration | PASS | 1395×930 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/10-joins-in-spark.md` | 164 | `images/10-joins-in-spark-04-broadcast-exchange-crisp.png` | instructional illustration | PASS | 1440×984 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | 60 | `images/11-operations-on-spark-rdds-01-rdd-of-rows-crisp.png` | instructional illustration | PASS | 1395×954 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | 101 | `images/11-operations-on-spark-rdds-02-map-key-value-whiteboard-imagegen.png` | instructional illustration | PASS | 1667×943 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | 181 | `images/11-operations-on-spark-rdds-03-reducebykey-chain-crisp.png` | instructional illustration | PASS | 1395×954 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | 202 | `images/11-operations-on-spark-rdds-04-todf-lost-names-crisp.png` | instructional illustration | PASS | 1395×954 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/11-operations-on-spark-rdds.md` | 256 | `images/11-operations-on-spark-rdds-06-dag-two-stages-crisp.png` | instructional illustration | PASS | 1440×1020 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | 20 | `images/12-spark-rdd-mappartition-01-map-partitions-diagram-imagegen.png` | instructional illustration | PASS | 1536×1024 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | 51 | `images/12-spark-rdd-mappartition-02-feature-columns-crisp.png` | instructional illustration | PASS | 1800×600 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | 104 | `images/12-spark-rdd-mappartition-04-partition-sizes-crisp.png` | instructional illustration | PASS | 1395×954 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | 177 | `images/12-spark-rdd-mappartition-06-model-and-yield-crisp.png` | instructional illustration | PASS | 1395×954 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/12-spark-rdd-mappartition.md` | 235 | `images/12-spark-rdd-mappartition-07-predicted-duration-crisp.png` | instructional illustration | PASS | 1395×954 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | 30 | `images/13-connecting-to-google-cloud-storage-02-upload-parquet-to-gcs-crisp.png` | instructional illustration | PASS | 1425×420 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | 35 | `images/13-connecting-to-google-cloud-storage-03-upload-progress-crisp.png` | instructional illustration | PASS | 1425×855 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | 70 | `images/13-connecting-to-google-cloud-storage-04-download-connector-jar-crisp.png` | instructional illustration | PASS | 1620×324 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | 101 | `images/13-connecting-to-google-cloud-storage-05-spark-conf-gcs-connector-crisp.png` | instructional illustration | PASS | 1500×300 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | 133 | `images/13-connecting-to-google-cloud-storage-06-spark-session-gcs-crisp.png` | instructional illustration | PASS | 1800×390 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/13-connecting-to-google-cloud-storage.md` | 146 | `images/13-connecting-to-google-cloud-storage-07-read-from-gcs-test-crisp.png` | instructional illustration | PASS | 1800×144 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | 39 | `images/14-creating-a-local-spark-cluster-01-spark-master-ui-crisp.png` | instructional illustration | PASS | 1920×306 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | 88 | `images/14-creating-a-local-spark-cluster-02-worker-registered-crisp.png` | instructional illustration | PASS | 1920×471 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | 106 | `images/14-creating-a-local-spark-cluster-03-converted-script-crisp.png` | instructional illustration | PASS | 1080×780 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | 148 | `images/14-creating-a-local-spark-cluster-04-running-script-2020-crisp.png` | instructional illustration | PASS | 1425×840 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/14-creating-a-local-spark-cluster.md` | 178 | `images/14-creating-a-local-spark-cluster-05-spark-submit-2021-crisp.png` | instructional illustration | PASS | 1425×900 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | 28 | `images/15-setting-up-a-dataproc-cluster-01-create-cluster-crisp.png` | instructional illustration | PASS | 1605×990 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | 67 | `images/15-setting-up-a-dataproc-cluster-02-submit-job-form-crisp.png` | instructional illustration | PASS | 1080×765 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | 74 | `images/15-setting-up-a-dataproc-cluster-03-job-finished-report-crisp.png` | instructional illustration | PASS | 1605×960 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/15-setting-up-a-dataproc-cluster.md` | 127 | `images/15-setting-up-a-dataproc-cluster-05-reports-in-bucket-crisp.png` | instructional illustration | PASS | 1605×990 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/16-connecting-spark-to-bigquery.md` | 40 | `images/16-connecting-spark-to-bigquery-01-connector-tutorial-crisp.png` | instructional illustration | PASS | 1290×834 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/16-connecting-spark-to-bigquery.md` | 75 | `images/16-connecting-spark-to-bigquery-02-failed-to-find-bigquery-crisp.png` | instructional illustration | PASS | 1620×720 | review required: crisp/generated asset |
| DE | `cohorts/2027/06-batch/16-connecting-spark-to-bigquery.md` | 113 | `images/16-connecting-spark-to-bigquery-03-bigquery-table-crisp.png` | instructional illustration | PASS | 1605×900 | review required: crisp/generated asset |

## Review handoff

- The machine-check snapshot contains 762 image-reference occurrences; 0 are missing or outside their repository.
- 0 active instructional references are crop-only candidates and must be checked against their retained original source before acceptance.
- The implementation agent must retain each original non-crisp source, crop only when it isolates useful content, merge adjacent screenshots on the content side in the correct orientation, and pass the original source image(s) plus any merged source reference to imagegen. A 2×/3× resized derivative must never be the only imagegen input.
- The independent reviewer must inspect crop direction/order, visual crispness, text/semantic fidelity, overlays, and every Markdown reference, then record an explicit verdict in the rollout report.

Reproduce this snapshot with: `python scripts/audit-illustrations/audit_illustrations.py --workspace-root /home/alexey/git --output docs/current-illustration-audit.md`

The selected DE scope is explicitly `published=false`; it is included because it is the current 2027 draft work scope, not because it is already live. Historical cohorts and unrelated course repositories are excluded.
