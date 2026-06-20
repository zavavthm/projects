import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SOURCE = DATA_DIR / "user_features.csv"
TRAIN_OUT = DATA_DIR / "train.csv"
TEST_OUT = DATA_DIR / "test.csv"

LABEL = "did_purchase"
TEST_SIZE = 0.10
RANDOM_STATE = 42


def main():
    df = pd.read_csv(SOURCE)
    print(f"Loaded {len(df)} rows from {SOURCE.name}")
    print(f"Label distribution:\n{df[LABEL].value_counts().to_string()}\n")

    train_df, test_df = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df[LABEL],
    )

    train_df.to_csv(TRAIN_OUT, index=False)
    test_df.to_csv(TEST_OUT, index=False)

    print(f"Train: {len(train_df)} rows -> {TRAIN_OUT.name}")
    print(f"  {LABEL} distribution: {dict(train_df[LABEL].value_counts())}")
    print(f"Test:  {len(test_df)} rows -> {TEST_OUT.name}")
    print(f"  {LABEL} distribution: {dict(test_df[LABEL].value_counts())}")


if __name__ == "__main__":
    main()
