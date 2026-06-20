import json
import os
import random
import signal
import sys
import time
from pathlib import Path

from confluent_kafka import Producer

BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC = os.environ.get("KAFKA_TOPIC", "gold-prices")
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "gold_price_schema.json"
REPORT_INTERVAL = 5

with open(SCHEMA_PATH) as f:
    schema = json.load(f)

PRICES = schema["price"]["params"][0]["values"]
VOLUMES = schema["volume"]["params"][0]["values"]
CHANGES = schema["change_pct"]["params"][0]["values"]
MARKETS = schema["market"]["params"][0]["values"]
MARKET_WEIGHTS = schema["market"]["params"][0]["weights"]
TRADE_TYPES = schema["trade_type"]["params"][0]["values"]
TRADE_WEIGHTS = schema["trade_type"]["params"][0]["weights"]

running = True


def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]


def generate_event():
    price = random.choice(PRICES)
    spread = round(random.uniform(0.3, 1.3), 2)
    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time() * 1000) % 1000:03d}Z",
        "symbol": "XAU/USD",
        "price": price,
        "bid": round(price - spread, 2),
        "ask": round(price + spread, 2),
        "volume": random.choice(VOLUMES),
        "change_pct": random.choice(CHANGES),
        "market": weighted_choice(MARKETS, MARKET_WEIGHTS),
        "currency": "USD",
        "trade_type": weighted_choice(TRADE_TYPES, TRADE_WEIGHTS),
    }


def delivery_callback(err, msg):
    if err:
        sys.stderr.write(f"Delivery failed: {err}\n")


def main():
    global running

    producer = Producer({
        "bootstrap.servers": BROKER,
        "linger.ms": 5,
        "batch.num.messages": 10000,
        "queue.buffering.max.messages": 1000000,
        "queue.buffering.max.kbytes": 1048576,
        "compression.type": "lz4",
    })

    def shutdown(signum, frame):
        global running
        running = False

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print(f"Connected to Kafka at {BROKER}")
    print(f"Producing to topic '{TOPIC}' — full throttle (no rate limit)")
    print(f"Reporting every {REPORT_INTERVAL}s. Ctrl+C to stop.\n")

    count = 0
    start = time.perf_counter()
    last_report = start

    while running:
        event = generate_event()
        try:
            producer.produce(
                TOPIC,
                key="XAU/USD",
                value=json.dumps(event),
                callback=delivery_callback,
            )
            count += 1
        except BufferError:
            producer.poll(0.1)
            continue

        if count % 1000 == 0:
            producer.poll(0)

        now = time.perf_counter()
        if now - last_report >= REPORT_INTERVAL:
            elapsed = now - start
            eps = count / elapsed if elapsed > 0 else 0
            print(f"Sent {count:,} events | {eps:,.0f} EPS | latest: ${event['price']} @ {event['market']}")
            last_report = now

    elapsed = time.perf_counter() - start
    print(f"\nFlushing remaining messages...")
    producer.flush(timeout=10)
    eps = count / elapsed if elapsed > 0 else 0
    print(f"Done. Sent {count:,} events in {elapsed:.1f}s ({eps:,.0f} EPS)")


if __name__ == "__main__":
    main()
