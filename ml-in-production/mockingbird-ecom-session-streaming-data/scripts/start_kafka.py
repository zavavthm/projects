import subprocess
import sys
import time
from pathlib import Path

DOCKER_DIR = Path(__file__).resolve().parent.parent.parent / "kafka-setup"


def run(cmd, **kwargs):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode != 0 and result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def main():
    print(f"Starting shared Kafka stack from {DOCKER_DIR}/docker-compose.yml ...")
    rc = run(f"docker compose -f {DOCKER_DIR}/docker-compose.yml up -d")
    if rc != 0:
        sys.exit(rc)

    print("Waiting for Kafka to be healthy...")
    for _ in range(30):
        rc = run(
            "docker exec gold-kafka kafka-broker-api-versions --bootstrap-server localhost:9092",
            capture_output=True,
        )
        if rc == 0:
            break
        time.sleep(2)
    else:
        print("Kafka failed to start within 60s", file=sys.stderr)
        sys.exit(1)

    print("Kafka is ready.")
    print("  Broker:   localhost:9092")
    print("  Kafka UI: http://localhost:8080")


if __name__ == "__main__":
    main()
