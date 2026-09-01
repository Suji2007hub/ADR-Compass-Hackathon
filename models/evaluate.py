import numpy as np

from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_model(model, X_test, y_test):

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "accuracy": float(
            accuracy_score(y_test, y_pred)
        ),
        "precision": float(
            precision_score(
                y_test,
                y_pred,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                y_test,
                y_pred,
                zero_division=0,
            )
        ),
        "f1": float(
            f1_score(
                y_test,
                y_pred,
                zero_division=0,
            )
        ),
        "roc_auc": float(
            roc_auc_score(y_test, y_proba)
        ),
        "pr_auc": float(
            average_precision_score(
                y_test,
                y_proba,
            )
        ),
        "confusion_matrix": confusion_matrix(
            y_test,
            y_pred,
        ).tolist(),
    }