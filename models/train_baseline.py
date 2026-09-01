import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier


BASELINE_FEATURES = [
    "age",
    "sex",
    "drug_name",
    "drug_class",
    "medical_condition",
    "previous_adr",
]

TARGET = "adr_occurred"

CATEGORICAL_FEATURES = [
    "sex",
    "drug_name",
    "drug_class",
    "medical_condition",
    "previous_adr",
]


def train_model_a(
    data_path="data/processed/baseline_clean.csv",
    model_out="models/saved/model_a.pkl",
):
    df = pd.read_csv(data_path)

    required_columns = BASELINE_FEATURES + [TARGET]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    X = df[BASELINE_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            )
        ],
        remainder="passthrough",
    )

    classifier = XGBClassifier(
        eval_metric="logloss",
        random_state=42,
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )

    model.fit(X_train, y_train)

    joblib.dump(model, model_out)

    print(f"Model A saved to: {model_out}")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    return model, X_test, y_test


if __name__ == "__main__":
    train_model_a()   