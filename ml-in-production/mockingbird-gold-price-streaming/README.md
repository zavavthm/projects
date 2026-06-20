# Mockingbird Gold Price Streaming

Mock streaming data generator simulating real-time gold market prices, built with [Mockingbird](https://github.com/tinybirdco/mockingbird) schema conventions and streamed to a local Kafka cluster.

## Architecture

```
Mockingbird Schema (gold_price_schema.json)
        │
        ▼
  Python Producer (produce.py)
  confluent-kafka (librdkafka) — full throttle, no rate limit
        │
        ▼
  Local Kafka Broker (Docker — shared via kafka-setup/)
  Topic: gold-prices (3 partitions)
        │
        ▼
  Console Consumer (consume.py) / Kafka UI (localhost:8080)
```

## Prerequisites

- Python >= 3.9
- Docker & Docker Compose
- `pip install -r requirements.txt`

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the Kafka stack
python3 scripts/start_kafka.py

# 3. Create the gold-prices topic
python3 scripts/create_topic.py

# 4. Start streaming gold price events (full throttle)
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

Each event represents a gold market tick:

| Field        | Type    | Description                                     |
|-------------|---------|--------------------------------------------------|
| `timestamp` | string  | ISO 8601 timestamp of the tick                   |
| `symbol`    | string  | Always `XAU/USD`                                 |
| `price`     | number  | Gold price per troy ounce ($1825–$2493 range)    |
| `bid`       | number  | Bid price (price minus spread)                   |
| `ask`       | number  | Ask price (price plus spread)                    |
| `volume`    | number  | Trade volume (120–65000 units)                   |
| `change_pct`| number  | Price change percentage (-1.85% to +1.85%)       |
| `market`    | string  | Exchange: COMEX (40%), LBMA (30%), SGE (15%), TOCOM (10%), MCX (5%) |
| `currency`  | string  | Always `USD`                                     |
| `trade_type`| string  | spot (60%), futures (30%), options (10%)          |

Example event:
```json
{
  "timestamp": "2026-06-20T14:32:15.342Z",
  "symbol": "XAU/USD",
  "price": 2305.80,
  "bid": 2305.25,
  "ask": 2306.35,
  "volume": 4500,
  "change_pct": 0.12,
  "market": "COMEX",
  "currency": "USD",
  "trade_type": "spot"
}
```

## Configuration

| Environment Variable | Default         | Description            |
|---------------------|-----------------|------------------------|
| `KAFKA_BROKER`      | `localhost:9092` | Kafka bootstrap server |
| `KAFKA_TOPIC`       | `gold-prices`    | Target Kafka topic     |

## Scripts

| Script                          | Description                              |
|--------------------------------|------------------------------------------|
| `python3 scripts/produce.py`   | Start the gold price producer            |
| `python3 scripts/start_kafka.py` | Start the Docker Kafka stack           |
| `python3 scripts/stop_kafka.py`  | Stop the Docker Kafka stack            |
| `python3 scripts/create_topic.py` | Create the gold-prices topic          |
| `python3 scripts/test_generate.py` | Test data generation + benchmark     |
| `python3 scripts/consume.py` | Console consumer for verification |

## Monitoring

Kafka UI is available at **http://localhost:8080** when the stack is running. Use it to inspect topics, messages, consumer groups, and broker health.

## Migrating to Confluent Cloud

A template config is provided at `config/kafka-destination.json`. Fill in your Confluent Cloud credentials to switch from local Kafka to a managed cluster.
