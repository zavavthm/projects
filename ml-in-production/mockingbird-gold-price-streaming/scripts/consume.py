import subprocess
import signal
import sys

TOPIC = "gold-prices"


def main():
    print(f"Consuming from topic '{TOPIC}'... (Ctrl+C to stop)\n")

    try:
        proc = subprocess.Popen(
            f"docker exec gold-kafka kafka-console-consumer "
            f"--bootstrap-server localhost:9092 "
            f"--topic {TOPIC} "
            f"--from-beginning "
            f"--property print.timestamp=true",
            shell=True,
        )
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()
        print("\nConsumer stopped.")


if __name__ == "__main__":
    main()
