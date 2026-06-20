import subprocess
import sys

TOPIC = "ecom-sessions"
PARTITIONS = 3
REPLICATION = 1


def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout, end="")
    if result.returncode != 0 and result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def main():
    print(f"Creating topic '{TOPIC}'...")
    rc = run(
        f"docker exec gold-kafka kafka-topics "
        f"--bootstrap-server localhost:9092 "
        f"--create --topic {TOPIC} "
        f"--partitions {PARTITIONS} "
        f"--replication-factor {REPLICATION} "
        f"--if-not-exists"
    )
    if rc != 0:
        sys.exit(rc)

    print(f"Topic '{TOPIC}' created with {PARTITIONS} partitions.")
    run(
        f"docker exec gold-kafka kafka-topics "
        f"--bootstrap-server localhost:9092 "
        f"--describe --topic {TOPIC}"
    )


if __name__ == "__main__":
    main()
