"""
Literature-derived evidence used for the synthetic blood-group experiment.

Important:
The ABO/Rh values assigned to individual records are SYNTHETIC.
They are not observed patient blood-group measurements.

The odds ratios below are literature-derived and should only be
interpreted within the evidence scope documented below.
"""

TAO_2020_ATLI_ODDS_RATIOS = {
    "A": {
        "OR": 1.832,
        "CI_low": 1.126,
        "CI_high": 2.983,
        "p": 0.015,
    },
    "B": {
        "OR": 1.751,
        "CI_low": 1.044,
        "CI_high": 2.937,
        "p": 0.034,
    },
    "AB": {
        "OR": 2.059,
        "CI_low": None,
        "CI_high": None,
        "p": 0.018,
    },
    "O": {
        "OR": 1.0,
        "CI_low": None,
        "CI_high": None,
        "p": None,
    },
}

# Indian ABO frequencies from the cited population study.
INDIA_ABO_FREQUENCY = {
    "O": 0.3712,
    "B": 0.3226,
    "A": 0.2288,
    "AB": 0.0774,
}

INDIA_RH_FREQUENCY = {
    "+": 0.9461,
    "-": 0.0539,
}

# Scope of the motivating literature.
EVIDENCE_SCOPE = {
    "drug_names": [
        "rifampin",
        "isoniazid",
        "pyrazinamide",
        "ethambutol",
    ],
    "reaction_categories": [
        "hepatic",
        "liver injury",
    ],
}