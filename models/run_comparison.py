import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from models.train_baseline import BASELINE_FEATURES, TARGET
from models.train_enhanced import ENHANCED_FEATURES
from models.significance_test import bootstrap_auc_diff


def main():

    DATA_PATH = "data/processed/final_dataset.csv"

    df = pd.read_csv(DATA_PATH)

    # ---------------------------------------------------------
    # Same train/test split for both models
    # ---------------------------------------------------------

    train_idx, test_idx = train_test_split(
        np.arange(len(df)),
        test_size=0.20,
        stratify=df[TARGET],
        random_state=42,
    )

    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]

    X_test_a = test_df[BASELINE_FEATURES]
    X_test_b = test_df[ENHANCED_FEATURES]

    y_test = test_df[TARGET]

    # ---------------------------------------------------------
    # Load trained models
    # ---------------------------------------------------------

    import joblib

    model_a = joblib.load(
        "models/saved/model_a.pkl"
    )

    model_b = joblib.load(
        "models/saved/model_b.pkl"
    )

    # ---------------------------------------------------------
    # Predictions
    # ---------------------------------------------------------

    proba_a = model_a.predict_proba(
        X_test_a
    )[:, 1]

    proba_b = model_b.predict_proba(
        X_test_b
    )[:, 1]

    # ---------------------------------------------------------
    # AUC comparison
    # ---------------------------------------------------------

    from sklearn.metrics import roc_auc_score

    auc_a = roc_auc_score(
        y_test,
        proba_a
    )

    auc_b = roc_auc_score(
        y_test,
        proba_b
    )

    print()
    print("================================")
    print("MODEL COMPARISON")
    print("================================")

    print(
        f"Model A ROC-AUC: {auc_a:.4f}"
    )

    print(
        f"Model B ROC-AUC: {auc_b:.4f}"
    )

    print(
        f"Difference (B - A): {auc_b - auc_a:.4f}"
    )

    # ---------------------------------------------------------
    # Bootstrap significance test
    # ---------------------------------------------------------

    result = bootstrap_auc_diff(
        y_test,
        proba_a,
        proba_b,
        n_bootstrap=2000,
        seed=42,
    )

    print()
    print("BOOTSTRAP TEST")
    print("================================")

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )


if __name__ == "__main__":
    main()