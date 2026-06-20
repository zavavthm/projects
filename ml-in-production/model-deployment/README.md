# Model Deployment — MLflow Serving

Serves the purchase prediction model from MLflow Model Registry as a REST API.

## Architecture

```
MLflow Model Registry
  "purchase-prediction" v1, v2, v3...
        │
        ▼
  mlflow models serve (uvicorn)
  Port 8000
        │
        ▼
  POST /invocations  →  { predictions: [{ prediction, probability }] }
  GET  /health
```

## Prerequisites

- MLflow tracking server running at `http://localhost:5000`
- A registered model in the "purchase-prediction" registry (run `train_model.py` first)

## Quick Start

```bash
# 1. Deploy the latest model version
python3 scripts/deploy.py

# 2. Test health
curl http://localhost:8000/health

# 3. Get a prediction
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"inputs": [{"total_events": 48, "page_view_count": 19, ...}]}'

# 4. Stop serving
python3 scripts/stop.py
```

## API

### POST `/invocations`

Request (MLflow standard format):
```json
{
  "inputs": [{
    "total_events": 48,
    "page_view_count": 19,
    "search_count": 7,
    "product_click_count": 8,
    "add_to_cart_count": 10,
    "remove_from_cart_count": 0,
    "apply_coupon_count": 3,
    "write_review_count": 0,
    "unique_products": 48,
    "unique_categories": 7,
    "avg_product_price": 281.56,
    "max_product_price": 1299.99,
    "avg_page_duration_sec": 170.46,
    "total_page_duration_sec": 8182,
    "avg_quantity": 1.69,
    "max_cart_total": 2499.99,
    "avg_cart_total": 701.45,
    "has_discount": 1,
    "max_discount_pct": 25,
    "is_member": 0,
    "add_to_cart_ratio": 0.2083,
    "search_to_cart_ratio": 1.4286,
    "primary_device": "mobile",
    "primary_browser": "Chrome",
    "primary_referral": "direct",
    "primary_os": "Android"
  }]
}
```

Response:
```json
{
  "predictions": [{
    "prediction": 1,
    "probability": 0.9473
  }]
}
```

### GET `/health`
Returns HTTP 200 when serving is ready.

## Scripts

| Script | Description |
|--------|-------------|
| `python3 scripts/deploy.py` | Serve latest model version on port 8000 |
| `python3 scripts/stop.py` | Stop the serving process |

## Deploying a Specific Version

Edit `deploy.py` or run directly:
```bash
mlflow models serve -m "models:/purchase-prediction/2" --port 8000 --no-conda
```
