import subprocess
import sys
from pathlib import Path

MLFLOW_DIR = Path(__file__).resolve().parent.parent.parent / "mlflow"


def main():
    MLFLOW_DIR.mkdir(exist_ok=True)
    db_uri = f"sqlite:///{MLFLOW_DIR}/mlflow.db"
    artifact_root = str(MLFLOW_DIR / "mlartifacts")

    print(f"Starting MLflow server...")
    print(f"  Backend:   {db_uri}")
    print(f"  Artifacts: {artifact_root}")
    print(f"  UI:        http://localhost:5000")
    print(f"  Ctrl+C to stop.\n")

    try:
        proc = subprocess.Popen([
            sys.executable, "-m", "mlflow", "server",
            "--backend-store-uri", db_uri,
            "--default-artifact-root", artifact_root,
            "--port", "5000",
            "--host", "0.0.0.0",
        ])
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()
        print("\nMLflow server stopped.")


if __name__ == "__main__":
    main()
