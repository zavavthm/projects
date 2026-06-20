import json
import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.pyfunc
import mlflow.xgboost
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MLFLOW_TRACKING_URI = "http://localhost:5000"
EXPERIMENT_NAME = "purchase-prediction"
REGISTERED_MODEL_NAME = "purchase-prediction"

LABEL = "did_purchase"
DROP_COLS = ["user_id", "purchase_count"]
CAT_COLS = ["primary_device", "primary_browser", "primary_referral", "primary_os"]


def prepare(df):
    df = df.drop(columns=DROP_COLS, errors="ignore")
    df = pd.get_dummies(df, columns=CAT_COLS, drop_first=True)
    X = df.drop(columns=[LABEL])
    y = df[LABEL]
    return X, y


class PurchasePredictionModel(mlflow.pyfunc.PythonModel):

    def load_context(self, context):
        import xgboost as xgb
        import json
        self.model = xgb.XGBClassifier()
        self.model.load_model(context.artifacts["xgb_model"])
        with open(context.artifacts["feature_columns"]) as f:
            self.feature_columns = json.load(f)
        self.cat_cols = ["primary_device", "primary_browser", "primary_referral", "primary_os"]

    def predict(self, context, model_input, params=None):
        import pandas as pd
        df = pd.DataFrame(model_input) if not isinstance(model_input, pd.DataFrame) else model_input.copy()
        for col in self.cat_cols:
            if col in df.columns:
                col_values = df[col].astype(str)
                df = df.drop(columns=[col])
                for feat_col in self.feature_columns:
                    if feat_col.startswith(f"{col}_"):
                        category = feat_col[len(f"{col}_"):]
                        df[feat_col] = (col_values == category).astype(int)
        df = df.reindex(columns=self.feature_columns, fill_value=0)
        for col in df.columns:
            df[col] = df[col].apply(lambda x: float(x) if not isinstance(x, (int, float)) else x)
        df = df.astype(float)
        predictions = self.model.predict(df)
        probabilities = self.model.predict_proba(df)[:, 1]
        return pd.DataFrame({
            "prediction": predictions,
            "probability": probabilities.round(4),
        })


def main():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    train_df = pd.read_csv(DATA_DIR / "train.csv")
    test_df = pd.read_csv(DATA_DIR / "test.csv")
    print(f"Train: {len(train_df)} rows | Test: {len(test_df)} rows\n")

    X_train, y_train = prepare(train_df)
    X_test, y_test = prepare(test_df)
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    print(f"Features: {X_train.shape[1]}")
    print(f"Train label balance: {dict(y_train.value_counts())}")
    print(f"Test label balance:  {dict(y_test.value_counts())}\n")

    params = {
        "n_estimators": 200,
        "max_depth": 5,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "eval_metric": "logloss",
        "random_state": 42,
    }

    with mlflow.start_run() as run:
        mlflow.log_params(params)
        mlflow.log_param("train_size", len(train_df))
        mlflow.log_param("test_size", len(test_df))
        mlflow.log_param("n_features", X_train.shape[1])

        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=["No Purchase", "Purchase"], zero_division=0)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("auc_roc", auc)

        print("=== Evaluation ===\n")
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1 Score:  {f1:.4f}")
        print(f"  AUC-ROC:   {auc:.4f}")
        print(f"\n  Confusion Matrix:")
        print(f"    TN={cm[0][0]}  FP={cm[0][1]}")
        print(f"    FN={cm[1][0]}  TP={cm[1][1]}")
        print(f"\n{report}")

        print("=== Top 15 Feature Importance ===\n")
        importance = model.feature_importances_
        feat_imp = sorted(zip(X_train.columns, importance), key=lambda x: -x[1])
        for name, score in feat_imp[:15]:
            bar = "█" * int(score * 100)
            print(f"  {name:30s} {score:.4f} {bar}")

        MODEL_DIR.mkdir(exist_ok=True)
        xgb_path = str(MODEL_DIR / "xgb_purchase_model.json")
        model.save_model(xgb_path)

        feature_cols_path = str(MODEL_DIR / "feature_columns.json")
        with open(feature_cols_path, "w") as f:
            json.dump(list(X_train.columns), f, indent=2)

        report_path = str(MODEL_DIR / "evaluation_report.txt")
        with open(report_path, "w") as f:
            f.write("=== Purchase Prediction Model — Evaluation Report ===\n\n")
            f.write(f"MLflow Run ID: {run.info.run_id}\n")
            f.write(f"Model: XGBoost ({params})\n")
            f.write(f"Train size: {len(train_df)} | Test size: {len(test_df)}\n")
            f.write(f"Features: {X_train.shape[1]}\n\n")
            f.write(f"Accuracy:  {acc:.4f}\nPrecision: {prec:.4f}\nRecall:    {rec:.4f}\n")
            f.write(f"F1 Score:  {f1:.4f}\nAUC-ROC:   {auc:.4f}\n\n")
            f.write(f"Confusion Matrix:\n  TN={cm[0][0]}  FP={cm[0][1]}\n  FN={cm[1][0]}  TP={cm[1][1]}\n\n")
            f.write(report)

        mlflow.log_artifact(report_path)

        artifacts = {
            "xgb_model": xgb_path,
            "feature_columns": feature_cols_path,
        }
        model_info = mlflow.pyfunc.log_model(
            artifact_path="purchase_model",
            python_model=PurchasePredictionModel(),
            artifacts=artifacts,
            pip_requirements=["xgboost>=2.0.0", "pandas>=2.0.0", "scikit-learn>=1.3.0"],
        )

        model_uri = f"runs:/{run.info.run_id}/purchase_model"
        result = mlflow.register_model(model_uri, REGISTERED_MODEL_NAME)

        print(f"\n=== MLflow ===")
        print(f"  Run ID:        {run.info.run_id}")
        print(f"  Model URI:     {model_uri}")
        print(f"  Model Version: {result.version}")
        print(f"  Tracking UI:   {MLFLOW_TRACKING_URI}")


if __name__ == "__main__":
    main()
