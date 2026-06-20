import json
import os
import random
import signal
import sys
import time
from pathlib import Path

from confluent_kafka import Producer

BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC = os.environ.get("KAFKA_TOPIC", "ecom-sessions")
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "ecom_session_schema.json"
REPORT_INTERVAL = 5

with open(SCHEMA_PATH) as f:
    schema = json.load(f)

EVENT_TYPES = schema["event_type"]["params"][0]["values"]
EVENT_TYPE_WEIGHTS = schema["event_type"]["params"][0]["weights"]
CATEGORIES = schema["product_category"]["params"][0]["values"]
CATEGORY_WEIGHTS = schema["product_category"]["params"][0]["weights"]
PRICES = schema["product_price"]["params"][0]["values"]
QUANTITIES = schema["quantity"]["params"][0]["values"]
QUANTITY_WEIGHTS = schema["quantity"]["params"][0]["weights"]
DEVICES = schema["device"]["params"][0]["values"]
DEVICE_WEIGHTS = schema["device"]["params"][0]["weights"]
OS_LIST = schema["os"]["params"][0]["values"]
OS_WEIGHTS = schema["os"]["params"][0]["weights"]
BROWSERS = schema["browser"]["params"][0]["values"]
BROWSER_WEIGHTS = schema["browser"]["params"][0]["weights"]
REFERRALS = schema["referral_source"]["params"][0]["values"]
REFERRAL_WEIGHTS = schema["referral_source"]["params"][0]["weights"]
DURATIONS = schema["page_duration_sec"]["params"][0]["values"]
MEMBER_VALUES = schema["is_member"]["params"][0]["values"]
MEMBER_WEIGHTS = schema["is_member"]["params"][0]["weights"]
CART_TOTALS = schema["cart_total"]["params"][0]["values"]
DISCOUNTS = schema["discount_pct"]["params"][0]["values"]
DISCOUNT_WEIGHTS = schema["discount_pct"]["params"][0]["weights"]

USER_POOL = [f"user_{i:04d}" for i in range(2000)]
PRODUCT_POOL = [f"prod_{i:04d}" for i in range(5000)]

running = True
session_counter = 0


def weighted_choice(values, weights):
    return random.choices(values, weights=weights, k=1)[0]


def generate_event():
    global session_counter
    session_counter += 1
    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(time.time() * 1000) % 1000:03d}Z",
        "event_id": f"evt_{session_counter:06d}",
        "user_id": random.choice(USER_POOL),
        "event_type": weighted_choice(EVENT_TYPES, EVENT_TYPE_WEIGHTS),
        "product_id": random.choice(PRODUCT_POOL),
        "product_category": weighted_choice(CATEGORIES, CATEGORY_WEIGHTS),
        "product_price": random.choice(PRICES),
        "quantity": weighted_choice(QUANTITIES, QUANTITY_WEIGHTS),
        "device": weighted_choice(DEVICES, DEVICE_WEIGHTS),
        "os": weighted_choice(OS_LIST, OS_WEIGHTS),
        "browser": weighted_choice(BROWSERS, BROWSER_WEIGHTS),
        "referral_source": weighted_choice(REFERRALS, REFERRAL_WEIGHTS),
        "page_duration_sec": random.choice(DURATIONS),
        "is_member": weighted_choice(MEMBER_VALUES, MEMBER_WEIGHTS),
        "cart_total": random.choice(CART_TOTALS),
        "discount_pct": weighted_choice(DISCOUNTS, DISCOUNT_WEIGHTS),
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
                key=event["user_id"],
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
            print(f"Sent {count:,} events | {eps:,.0f} EPS | latest: {event['event_type']} by {event['user_id']} — ${event['product_price']} {event['product_category']}")
            last_report = now

    elapsed = time.perf_counter() - start
    print(f"\nFlushing remaining messages...")
    producer.flush(timeout=10)
    eps = count / elapsed if elapsed > 0 else 0
    print(f"Done. Sent {count:,} events in {elapsed:.1f}s ({eps:,.0f} EPS)")


if __name__ == "__main__":
    main()
