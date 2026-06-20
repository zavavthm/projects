import subprocess
import sys

PID_FILE = "/tmp/mlflow_serve.pid"


def main():
    result = subprocess.run(f"cat {PID_FILE} 2>/dev/null", shell=True, capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print("No running MLflow serving process found.")
        return

    pid = result.stdout.strip()
    subprocess.run(f"kill {pid} 2>/dev/null", shell=True)
    subprocess.run(f"rm -f {PID_FILE}", shell=True)
    print(f"Stopped MLflow serving (PID {pid})")


if __name__ == "__main__":
    main()
