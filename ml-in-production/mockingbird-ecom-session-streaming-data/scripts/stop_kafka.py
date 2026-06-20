import subprocess
import sys
from pathlib import Path

DOCKER_DIR = Path(__file__).resolve().parent.parent.parent / "kafka-setup"


def main():
    print("Stopping shared Kafka stack...")
    result = subprocess.run(
        f"docker compose -f {DOCKER_DIR}/docker-compose.yml down",
        shell=True, capture_output=True, text=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode != 0 and result.stderr:
        print(result.stderr, end="", file=sys.stderr)
        sys.exit(result.returncode)
    print("Kafka stack stopped.")


if __name__ == "__main__":
    main()
