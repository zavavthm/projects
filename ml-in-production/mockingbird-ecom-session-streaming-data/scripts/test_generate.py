import json
import random
import sys
import time
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "ecom_session_schema.json"

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


def main():
    num_events = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"=== E-commerce Session Stream Test ({num_events} events) ===\n")

    events = [generate_event() for _ in range(num_events)]

    for i, e in enumerate(events[:10]):
        print(f"Event {i + 1}: {json.dumps(e, indent=2)}\n")

    if num_events > 10:
        print(f"... ({num_events - 10} more events generated, showing first 10)\n")

    print("=== Validation ===\n")
    valid_event_types = set(EVENT_TYPES)
    valid_categories = set(CATEGORIES)
    valid_devices = set(DEVICES)
    valid_os = set(OS_LIST)
    valid_browsers = set(BROWSERS)
    valid_referrals = set(REFERRALS)
    valid_discounts = set(DISCOUNTS)

    checks = [
        ("All timestamps are ISO 8601", all("T" in e["timestamp"] and e["timestamp"].endswith("Z") for e in events)),
        ("event_id starts with evt_", all(e["event_id"].startswith("evt_") for e in events)),
        ("user_id starts with user_", all(e["user_id"].startswith("user_") for e in events)),
        ("event_type is valid", all(e["event_type"] in valid_event_types for e in events)),
        ("product_id starts with prod_", all(e["product_id"].startswith("prod_") for e in events)),
        ("product_category is valid", all(e["product_category"] in valid_categories for e in events)),
        ("product_price in $4.99-$1299.99", all(4.99 <= e["product_price"] <= 1299.99 for e in events)),
        ("quantity is 1-5", all(1 <= e["quantity"] <= 5 for e in events)),
        ("device is valid", all(e["device"] in valid_devices for e in events)),
        ("os is valid", all(e["os"] in valid_os for e in events)),
        ("browser is valid", all(e["browser"] in valid_browsers for e in events)),
        ("referral_source is valid", all(e["referral_source"] in valid_referrals for e in events)),
        ("page_duration_sec is 3-600", all(3 <= e["page_duration_sec"] <= 600 for e in events)),
        ("is_member is boolean", all(isinstance(e["is_member"], bool) for e in events)),
        ("cart_total is $0-$2499.99", all(0 <= e["cart_total"] <= 2499.99 for e in events)),
        ("discount_pct is valid", all(e["discount_pct"] in valid_discounts for e in events)),
    ]

    all_passed = True
    for label, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_passed = False
        print(f"  [{status}] {label}")

    # Distribution check
    dist_events = [generate_event() for _ in range(10000)]

    event_type_counts = {}
    category_counts = {}
    device_counts = {}
    for e in dist_events:
        event_type_counts[e["event_type"]] = event_type_counts.get(e["event_type"], 0) + 1
        category_counts[e["product_category"]] = category_counts.get(e["product_category"], 0) + 1
        device_counts[e["device"]] = device_counts.get(e["device"], 0) + 1

    print(f"\n=== Distribution (10,000 events) ===\n")
    print("  Event Types:")
    for k, v in sorted(event_type_counts.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v} ({v / 100:.1f}%)")
    print("\n  Product Categories:")
    for k, v in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v} ({v / 100:.1f}%)")
    print("\n  Devices:")
    for k, v in sorted(device_counts.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v} ({v / 100:.1f}%)")

    # Throughput benchmark
    print(f"\n=== Throughput Benchmark (10s, no limit) ===\n")
    bench_count = 0
    start = time.perf_counter()
    deadline = start + 10.0
    while time.perf_counter() < deadline:
        for _ in range(10_000):
            generate_event()
        bench_count += 10_000
    elapsed = time.perf_counter() - start
    eps = bench_count / elapsed
    print(f"  Generated {bench_count:,} events in {elapsed:.2f}s")
    print(f"  Throughput: {eps:,.0f} events/sec (generation only, no Kafka)")

    print(f"\n=== Result: {'ALL CHECKS PASSED' if all_passed else 'SOME CHECKS FAILED'} ===")
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
