# Feature Engineering (Spark Streaming)

Consumes e-commerce session events from Kafka and engineers user-level features for purchase prediction using PySpark.

## Architecture

```
Kafka Topic: ecom-sessions
        │
        ▼
  PySpark (Spark SQL + Kafka connector)
  Batch read from Kafka → Aggregate per user_id
        │
        ▼
  data/user_features.csv
  (29 features per user — ready for ML)
```

## Prerequisites

- Python >= 3.9
- Java >= 11 (OpenJDK)
- Kafka running on `localhost:9092` with data in `ecom-sessions` topic
- `pip install -r requirements.txt`

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ensure Kafka is running and has data
# (from mockingbird-ecom-session-streaming-data/)
python3 scripts/start_kafka.py
python3 scripts/produce.py  # run for a few seconds, then Ctrl+C

# 3. Run the feature pipeline
python3 scripts/spark_feature_pipeline.py

# 4. Output lands in data/user_features.csv
```

## Features (per user_id)

| Feature | Description |
|---------|-------------|
| `total_events` | Total event count |
| `page_view_count` | Page view events |
| `search_count` | Search events |
| `product_click_count` | Product click events |
| `add_to_cart_count` | Add to cart events |
| `remove_from_cart_count` | Remove from cart events |
| `purchase_count` | Purchase events |
| `apply_coupon_count` | Apply coupon events |
| `write_review_count` | Write review events |
| `unique_products` | Distinct products interacted with |
| `unique_categories` | Distinct categories browsed |
| `avg_product_price` | Average product price |
| `max_product_price` | Max product price |
| `avg_page_duration_sec` | Average page time |
| `total_page_duration_sec` | Total browsing time |
| `avg_quantity` | Average quantity per event |
| `max_cart_total` | Peak cart value |
| `avg_cart_total` | Average cart value |
| `has_discount` | Had any discount (0/1) |
| `max_discount_pct` | Highest discount |
| `is_member` | Loyalty member (0/1) |
| `primary_device` | Most used device |
| `primary_browser` | Most used browser |
| `primary_referral` | Top referral source |
| `primary_os` | Most used OS |
| `add_to_cart_ratio` | add_to_cart / total_events |
| `search_to_cart_ratio` | add_to_cart / search |
| `did_purchase` | **Label**: purchased (0/1) |

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `KAFKA_BROKER` | `localhost:9092` | Kafka bootstrap server |
| `KAFKA_TOPIC` | `ecom-sessions` | Source Kafka topic |
