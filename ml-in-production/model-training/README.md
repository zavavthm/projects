# Model Training — Purchase Prediction (MLflow)

Trains an XGBoost classifier to predict e-commerce purchase behavior, with full experiment tracking and model versioning via MLflow.

## Architecture

```
MLflow Tracking Server (localhost:5000)
        │
        ▼
  train_model.py
  → Logs params, metrics, artifacts
  → Registers pyfunc model with preprocessing baked in
        │
        ▼
  MLflow Model Registry: "purchase-prediction" (v1, v2, ...)
```

## Prerequisites

- Python >= 3.9
- `brew install libomp` (macOS — required by XGBoost)
- `pip install -r requirements.txt`

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start MLflow tracking server
python3 scripts/start_mlflow_server.py &

# 3. Split data (90% train, 10% test)
python3 scripts/split_data.py

# 4. Train model — logs to MLflow, registers in Model Registry
python3 scripts/train_model.py

# MLflow UI: http://localhost:5000
```

## What Gets Logged to MLflow

| Category | Items |
|----------|-------|
| **Parameters** | n_estimators, max_depth, learning_rate, subsample, colsample_bytree, train_size, test_size |
| **Metrics** | accuracy, precision, recall, f1, auc_roc |
| **Artifacts** | xgb_purchase_model.json, feature_columns.json, evaluation_report.txt |
| **Model** | Custom pyfunc wrapping preprocessing + XGBoost (registered as "purchase-prediction") |

## Model Versioning

Each `train_model.py` run creates a new version in the MLflow Model Registry. You can:
- Compare runs in the MLflow UI at `http://localhost:5000`
- Serve any version: `mlflow models serve -m "models:/purchase-prediction/3"`
- Roll back by deploying a previous version

## Scripts

| Script | Description |
|--------|-------------|
| `python3 scripts/start_mlflow_server.py` | Start MLflow tracking server |
| `python3 scripts/split_data.py` | Split data 90/10 |
| `python3 scripts/train_model.py` | Train + log + register model |
