import os
import subprocess
import sys

MLFLOW_TRACKING_URI = "http://localhost:5000"
MODEL_NAME = "purchase-prediction"
PORT = 8000
PID_FILE = "/tmp/mlflow_serve.pid"


def get_latest_version():
    import mlflow
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = mlflow.tracking.MlflowClient()
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    if not versions:
        print(f"No versions found for model '{MODEL_NAME}'", file=sys.stderr)
        sys.exit(1)
    latest = max(versions, key=lambda v: int(v.version))
    return latest.version


def main():
    venv_bin = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "model-training", ".venv", "bin"
    ))
    venv_python = os.path.join(venv_bin, "python3")

    sys.path.insert(0, os.path.dirname(venv_python.replace("/bin/python3", "/lib")))
    os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI

    version = get_latest_version()
    model_uri = f"models:/{MODEL_NAME}/{version}"

    subprocess.run(f"kill $(cat {PID_FILE}) 2>/dev/null", shell=True)

    print(f"Deploying model: {MODEL_NAME} v{version}")
    print(f"  Model URI:  {model_uri}")
    print(f"  Port:       {PORT}")
    print(f"  Endpoint:   POST http://localhost:{PORT}/invocations")
    print(f"  Health:     GET  http://localhost:{PORT}/health")
    print()

    env = {**os.environ, "MLFLOW_TRACKING_URI": MLFLOW_TRACKING_URI, "PATH": f"{venv_bin}:{os.environ['PATH']}"}

    proc = subprocess.Popen(
        [
            venv_python, "-m", "mlflow", "models", "serve",
            "-m", model_uri,
            "--port", str(PORT),
            "--host", "0.0.0.0",
            "--no-conda",
        ],
        env=env,
    )

    with open(PID_FILE, "w") as f:
        f.write(str(proc.pid))

    print(f"MLflow serving started (PID {proc.pid})")
    print(f"Run 'python3 scripts/stop.py' to stop.")

    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait()
        print("\nServing stopped.")


if __name__ == "__main__":
    main()
