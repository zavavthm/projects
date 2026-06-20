import json
import random
import sys
import time
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "gold_price_schema.json"

with open(SCHEMA_PATH) as f:
    schema = json.load(f)

PRICES = schema["price"]["params"][0]["values"]
VOLUMES = schema["volume"]["params"][0]["values"]
CHANGES = schema["change_pct"]["params"][0]["values"]
MARKETS = schema["market"]["params"][0]["values"]
MARKET_WEIGHTS = schema["market"]["params"][0]["weights"]
TRADE_TYPES = schema["trade_type"]["params"][0]["values"]
TRADE_WEIGHTS = schema["trade_type"]["params"][0]["weights"]


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


def main():
    num_events = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"=== Gold Price Stream Test ({num_events} events) ===\n")

    events = [generate_event() for _ in range(num_events)]

    for i, e in enumerate(events[:10]):
        print(f"Event {i + 1}: {json.dumps(e, indent=2)}\n")

    if num_events > 10:
        print(f"... ({num_events - 10} more events generated, showing first 10)\n")

    # Validation
    print("=== Validation ===\n")
    checks = [
        ("All timestamps are ISO 8601", all("T" in e["timestamp"] and e["timestamp"].endswith("Z") for e in events)),
        ("Symbol is XAU/USD", all(e["symbol"] == "XAU/USD" for e in events)),
        ("Prices in range $1825-$2494", all(1825 <= e["price"] <= 2494 for e in events)),
        ("Bid < Price < Ask", all(e["bid"] < e["price"] < e["ask"] for e in events)),
        ("Spread (ask-bid) is $0.60-$2.60", all(0.60 <= round(e["ask"] - e["bid"], 2) <= 2.60 for e in events)),
        ("Volume is positive integer", all(isinstance(e["volume"], int) and e["volume"] > 0 for e in events)),
        ("change_pct in [-1.85, 1.85]", all(-1.85 <= e["change_pct"] <= 1.85 for e in events)),
        ("Market is valid exchange", all(e["market"] in MARKETS for e in events)),
        ("Currency is USD", all(e["currency"] == "USD" for e in events)),
        ("Trade type is valid", all(e["trade_type"] in TRADE_TYPES for e in events)),
    ]

    all_passed = True
    for label, ok in checks:
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_passed = False
        print(f"  [{status}] {label}")

    # Distribution check
    dist_events = [generate_event() for _ in range(10000)]
    market_counts = {}
    type_counts = {}
    for e in dist_events:
        market_counts[e["market"]] = market_counts.get(e["market"], 0) + 1
        type_counts[e["trade_type"]] = type_counts.get(e["trade_type"], 0) + 1

    print(f"\n=== Distribution (10,000 events) ===\n")
    print("  Markets:")
    for k, v in sorted(market_counts.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v} ({v / 100:.1f}%)")
    print("\n  Trade Types:")
    for k, v in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v} ({v / 100:.1f}%)")

    # Throughput benchmark — run for 10 seconds, no cap
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
