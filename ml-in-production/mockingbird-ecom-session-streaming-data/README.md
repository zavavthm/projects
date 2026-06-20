# Mockingbird E-commerce Session Streaming Data

Mock streaming data generator simulating e-commerce user sessions, built with [Mockingbird](https://github.com/tinybirdco/mockingbird) schema conventions and streamed to a local Kafka cluster.

## Architecture

```
Mockingbird Schema (ecom_session_schema.json)
        │
        ▼
  Python Producer (produce.py)
  confluent-kafka (librdkafka) — full throttle, no rate limit
        │
        ▼
  Shared Kafka Broker (Docker — via kafka-setup/)
  Topic: ecom-sessions (3 partitions)
        │
        ▼
  Console Consumer (consume.py) / Kafka UI (localhost:8080)
```

Kafka stack is shared via `kafka-setup/` — no duplicate containers.

## Prerequisites

- Python >= 3.9
- Docker & Docker Compose
- `pip install -r requirements.txt`

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the shared Kafka stack
python3 scripts/start_kafka.py

# 3. Create the ecom-sessions topic
python3 scripts/create_topic.py

# 4. Start streaming session events (full throttle)
python3 scripts/produce.py

# 5. (In another terminal) Consume and verify
python3 scripts/consume.py
```

## Testing (without Kafka)

```bash
# Generate 500 events, validate schema, run throughput benchmark
python3 scripts/test_generate.py 500
```

## Event Schema

Each event represents a user action within an e-commerce session:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | string | ISO 8601 timestamp of the action |
| `event_id` | string | Unique event identifier (e.g. `evt_000042`) |
| `user_id` | string | User identifier from pool of 2000 users |
| `event_type` | string | `page_view` (40%), `search` (15%), `add_to_cart` (15%), `product_click` (15%), `remove_from_cart` (5%), `purchase` (5%), `apply_coupon` (3%), `write_review` (2%) |
| `product_id` | string | Product identifier from pool of 5000 products |
| `product_category` | string | `Electronics` (25%), `Clothing` (20%), `Home & Kitchen` (15%), `Books` (12%), `Sports` (10%), `Beauty` (8%), `Toys` (5%), `Grocery` (5%) |
| `product_price` | number | Product price ($4.99–$1299.99) |
| `quantity` | int | 1 (60%), 2 (25%), 3 (10%), 4 (3%), 5 (2%) |
| `device` | string | `mobile` (55%), `desktop` (35%), `tablet` (10%) |
| `os` | string | `iOS` (35%), `Android` (30%), `Windows` (20%), `macOS` (12%), `Linux` (3%) |
| `browser` | string | `Chrome` (50%), `Safari` (25%), `Firefox` (10%), `Edge` (10%), `Other` (5%) |
| `referral_source` | string | `direct` (30%), `google_search` (25%), `social_media` (15%), `email_campaign` (12%), `affiliate` (10%), `paid_ad` (8%) |
| `page_duration_sec` | number | Time on page (3–600 seconds) |
| `is_member` | boolean | Prime/loyalty member: `true` (40%), `false` (60%) |
| `cart_total` | number | Running cart total ($0–$2499.99) |
| `discount_pct` | number | Discount applied: 0% (55%), 5% (15%), 10% (12%), 15% (8%), 20% (6%), 25% (4%) |

Example event:
```json
{
  "timestamp": "2026-06-20T19:45:12.342Z",
  "event_id": "evt_000042",
  "user_id": "user_0187",
  "event_type": "add_to_cart",
  "product_id": "prod_3421",
  "product_category": "Electronics",
  "product_price": 299.99,
  "quantity": 1,
  "device": "mobile",
  "os": "iOS",
  "browser": "Safari",
  "referral_source": "google_search",
  "page_duration_sec": 45,
  "is_member": true,
  "cart_total": 299.99,
  "discount_pct": 0
}
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `KAFKA_BROKER` | `localhost:9092` | Kafka bootstrap server |
| `KAFKA_TOPIC` | `ecom-sessions` | Target Kafka topic |

## Scripts

| Script | Description |
|--------|-------------|
| `python3 scripts/produce.py` | Start the session event producer |
| `python3 scripts/consume.py` | Console consumer for verification |
| `python3 scripts/create_topic.py` | Create the ecom-sessions topic |
| `python3 scripts/start_kafka.py` | Start the shared Kafka stack |
| `python3 scripts/stop_kafka.py` | Stop the shared Kafka stack |
| `python3 scripts/test_generate.py` | Test data generation + benchmark |

## Monitoring

Kafka UI is available at **http://localhost:8080** when the stack is running. Use it to inspect topics, messages, consumer groups, and broker health.

## Sample Data

`sample_data/ecom_sessions_sample.jsonl` contains 10,000 pre-generated events in JSON Lines format for offline analysis and feature engineering.
