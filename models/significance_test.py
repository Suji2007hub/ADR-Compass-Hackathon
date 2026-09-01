import numpy as np

from sklearn.metrics import roc_auc_score


def bootstrap_auc_diff(
    y_test,
    proba_a,
    proba_b,
    n_bootstrap=2000,
    seed=42,
):
    """
    Bootstrap confidence interval for:

        AUC(Model B) - AUC(Model A)

    Positive values favor Model B.
    """

    rng = np.random.default_rng(seed)

    y_test = np.asarray(y_test)
    proba_a = np.asarray(proba_a)
    proba_b = np.asarray(proba_b)

    n = len(y_test)
    differences = []

    for _ in range(n_bootstrap):

        indices = rng.integers(
            0,
            n,
            size=n,
        )

        y_sample = y_test[indices]

        if len(np.unique(y_sample)) < 2:
            continue

        auc_a = roc_auc_score(
            y_sample,
            proba_a[indices],
        )

        auc_b = roc_auc_score(
            y_sample,
            proba_b[indices],
        )

        differences.append(
            auc_b - auc_a
        )

    differences = np.asarray(differences)

    if len(differences) == 0:
        raise ValueError(
            "No valid bootstrap samples."
        )

    ci_low, ci_high = np.percentile(
        differences,
        [2.5, 97.5],
    )

    return {
        "mean_auc_difference": float(
            differences.mean()
        ),
        "ci_95_low": float(ci_low),
        "ci_95_high": float(ci_high),
        "significant_improvement": bool(
            ci_low > 0
        ),
        "n_bootstrap": len(differences),
    }