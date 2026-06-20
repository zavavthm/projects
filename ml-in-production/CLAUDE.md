# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a new project focused on deploying and operating machine learning models in production environments.

## Project Structure

- `kafka-setup/` — Shared Docker Compose Kafka stack (Zookeeper + Kafka + Kafka UI)
  - Used by all streaming subprojects
  - Kafka UI: http://localhost:8080
- `mockingbird-gold-price-streaming/` — Mock gold price streaming pipeline (Mockingbird → Kafka)
  - Uses Tinybird Mockingbird schema format for data generation
  - Python producer with confluent-kafka (librdkafka) — full throttle, no rate limit
  - Shares Docker Compose Kafka stack from kafka-setup/
  - Topic: `gold-prices` (3 partitions)

- `mockingbird-ecom-session-streaming-data/` — Mock e-commerce session streaming pipeline (Mockingbird → Kafka)
  - Uses Tinybird Mockingbird schema format for data generation
  - Python producer with confluent-kafka (librdkafka) — full throttle, no rate limit
  - Shares Docker Compose Kafka stack from kafka-setup/
  - Topic: `ecom-sessions` (3 partitions)
  - 16 fields: session/user IDs, event types, product info, device/browser, referral, membership, cart, discounts

- `feature-engineering/` — Spark-based feature engineering pipeline
  - Consumes events from Kafka topic `ecom-sessions` via PySpark
  - Aggregates 29 user-level features for purchase prediction
  - Outputs to `data/user_features.csv`

- `mlflow/` — Shared MLflow tracking server data (SQLite + artifacts)
  - UI: http://localhost:5000

- `model-training/` — XGBoost purchase prediction model (MLflow integrated)
  - Logs params, metrics, and model artifacts to MLflow
  - Registers versioned models in MLflow Model Registry as "purchase-prediction"
  - 90/10 stratified train/test split

- `model-deployment/` — MLflow model serving
  - Serves registered model via `mlflow models serve`
  - REST API: POST `/invocations` on port 8000

## Development Setup

**Working directory:** `/Users/manik.malhotra/Downloads/P/git_projects/projects/ml-in-production`

### Subproject: mockingbird-gold-price-streaming

```bash
cd mockingbird-gold-price-streaming
pip install -r requirements.txt
python3 scripts/start_kafka.py     # Start Kafka stack (Docker)
python3 scripts/create_topic.py    # Create gold-prices topic
python3 scripts/produce.py         # Stream gold price events → Kafka
python3 scripts/consume.py             # Verify events in console
python3 scripts/test_generate.py 500   # Test without Kafka
```

### Subproject: mockingbird-ecom-session-streaming-data

```bash
cd mockingbird-ecom-session-streaming-data
pip install -r requirements.txt
python3 scripts/start_kafka.py     # Start shared Kafka stack (Docker)
python3 scripts/create_topic.py    # Create ecom-sessions topic
python3 scripts/produce.py         # Stream session events → Kafka
python3 scripts/consume.py         # Verify events in console
python3 scripts/test_generate.py 500   # Test without Kafka
```

Kafka UI: http://localhost:8080

### Subproject: feature-engineering

```bash
cd feature-engineering
pip install -r requirements.txt
python3 scripts/spark_feature_pipeline.py   # Run feature pipeline (reads from Kafka)
# Output: data/user_features.csv
```

### Subproject: model-training

```bash
cd model-training
pip install -r requirements.txt
python3 scripts/start_mlflow_server.py &   # Start MLflow server (localhost:5000)
python3 scripts/split_data.py              # Split data 90/10
python3 scripts/train_model.py             # Train + log to MLflow + register model
# MLflow UI: http://localhost:5000
```

### Subproject: model-deployment

```bash
cd model-deployment
python3 scripts/deploy.py           # Serve latest model version on port 8000
python3 scripts/stop.py             # Stop serving
# API: POST http://localhost:8000/invocations
```

## Key Conventions

Update this section with conventions decided during development (e.g., model versioning scheme, API contract format, feature store usage).
