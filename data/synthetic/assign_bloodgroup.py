import numpy as np
import pandas as pd

from .literature_evidence import (
    INDIA_ABO_FREQUENCY,
    INDIA_RH_FREQUENCY,
)


def assign_synthetic_bloodgroup(
    df: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Assign synthetic ABO and Rh values using published Indian
    population frequencies.

    These values are synthetic and must NOT be presented as
    observed patient blood-group measurements.
    """

    rng = np.random.default_rng(seed)

    result = df.copy()
    n = len(result)

    abo_groups = list(INDIA_ABO_FREQUENCY.keys())
    abo_probs = list(INDIA_ABO_FREQUENCY.values())

    rh_groups = list(INDIA_RH_FREQUENCY.keys())
    rh_probs = list(INDIA_RH_FREQUENCY.values())

    result["blood_group"] = rng.choice(
        abo_groups,
        size=n,
        p=abo_probs,
    )

    result["rh_factor"] = rng.choice(
        rh_groups,
        size=n,
        p=rh_probs,
    )

    result["blood_group_source"] = "literature_derived_synthetic"

    return result