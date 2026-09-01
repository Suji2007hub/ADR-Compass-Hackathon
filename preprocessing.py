import requests
import pandas as pd
from pathlib import Path
import time


API_URL = "https://api.fda.gov/drug/event.json"

OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "baseline_clean.csv"

# Start small.
# Once this works, increase to 5000.
TOTAL_RECORDS = 500

BATCH_SIZE = 100


# ============================================================
# REACTION CATEGORIZATION
# ============================================================

def categorize_reaction(reaction):

    reaction = str(reaction).lower()

    hepatic_terms = [
        "hepatitis",
        "hepatic",
        "liver",
        "jaundice",
        "bilirubin",
        "transaminase",
        "alanine aminotransferase",
        "aspartate aminotransferase",
    ]

    dermatologic_terms = [
        "rash",
        "urticaria",
        "dermatitis",
        "pruritus",
        "skin",
        "erythema",
        "angioedema",
    ]

    cardiac_terms = [
        "tachycardia",
        "bradycardia",
        "arrhythmia",
        "cardiac",
        "myocardial",
        "palpitation",
    ]

    renal_terms = [
        "renal",
        "kidney",
        "nephritis",
        "creatinine",
        "proteinuria",
    ]

    neurological_terms = [
        "headache",
        "seizure",
        "convulsion",
        "dizziness",
        "neuropathy",
        "tremor",
        "syncope",
    ]

    gastrointestinal_terms = [
        "nausea",
        "vomiting",
        "diarrhea",
        "abdominal",
        "constipation",
        "gastric",
    ]

    if any(x in reaction for x in hepatic_terms):
        return "hepatic"

    if any(x in reaction for x in dermatologic_terms):
        return "dermatologic"

    if any(x in reaction for x in cardiac_terms):
        return "cardiac"

    if any(x in reaction for x in renal_terms):
        return "renal"

    if any(x in reaction for x in neurological_terms):
        return "neurological"

    if any(x in reaction for x in gastrointestinal_terms):
        return "gastrointestinal"

    return "other"


# ============================================================
# FETCH FAERS
# ============================================================

def fetch_faers(total_records=5000):

    reports = []

    print("Fetching targeted FAERS data from openFDA...")

    search_query = (
        "patient.drug.medicinalproduct:"
        "(RIFAMPIN OR RIFAMPICIN OR ISONIAZID OR "
        "PYRAZINAMIDE OR ETHAMBUTOL)"
    )

    for skip in range(0, total_records, BATCH_SIZE):

        limit = min(
            BATCH_SIZE,
            total_records - skip
        )

        params = {
            "search": search_query,
            "limit": limit,
            "skip": skip
        }

        print(
            f"Requesting targeted records "
            f"{skip} - {skip + limit}"
        )

        try:

            response = requests.get(
                API_URL,
                params=params,
                timeout=60
            )

            print(
                "HTTP status:",
                response.status_code
            )

            response.raise_for_status()

            data = response.json()

            batch = data.get(
                "results",
                []
            )

            reports.extend(batch)

            print(
                f"Retrieved {len(batch)} records"
            )

            if len(batch) < limit:
                print("No more matching records available.")
                break

        except requests.exceptions.HTTPError as e:

            print(
                "API request failed:",
                e
            )

            print(
                "Response:",
                response.text[:500]
            )

            break

        except requests.exceptions.RequestException as e:

            print(
                "Network error:",
                e
            )

            break

        time.sleep(0.5)

    print(
        f"Total targeted reports retrieved: "
        f"{len(reports)}"
    )

    return reports
# ============================================================
# CLEAN DATASET
# ============================================================

def process_reports(reports):

    rows = []

    for report in reports:
        patient = report.get("patient", {})

        case_id = report.get("safetyreportid")
        age = patient.get("patientonsetage")
        sex = patient.get("patientsex")

        reactions = patient.get("reaction", [])
        reaction_names = []

        for reaction in reactions:
            term = reaction.get("reactionmeddrapt")

            if term:
                reaction_names.append(term)

        if not reaction_names:
            continue

        drugs = patient.get("drug", [])

        for drug in drugs:

            # 1 = Primary suspect
            if str(drug.get("drugcharacterization")) != "1":
                continue

            drug_name = drug.get("medicinalproduct")

            if not drug_name:
                continue

            drug_name = str(drug_name).upper().strip()

            indication = drug.get("drugindication")

            for reaction in reaction_names:

                rows.append({
                    "case_id": case_id,
                    "age": age,
                    "sex": sex,
                    "drug_name": drug_name,
                    "medical_condition": indication,
                    "reaction": reaction,
                    "reaction_category": categorize_reaction(reaction),
                    "serious": report.get("serious", "0"),
                    "patient_death": bool(
                        patient.get("patientdeath")
                    )
                })

    return pd.DataFrame(rows)

def clean_dataset(df):

    print("Cleaning dataset...")

    df = df.copy()

    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )

    df.loc[
        (df["age"] < 0) |
        (df["age"] > 120),
        "age"
    ] = pd.NA

    df["age"] = (
        df["age"]
        .fillna(
            df["age"].median()
        )
    )

    # --------------------------------------------------------
    # SEX
    # --------------------------------------------------------

    df["sex"] = (
        df["sex"]
        .fillna("0")
        .astype(str)
    )

    df["sex"] = df["sex"].replace({

        "1": "M",

        "2": "F",

        "3": "UNKNOWN",

        "0": "UNKNOWN",

        "nan": "UNKNOWN"

    })

    # --------------------------------------------------------
    # DRUG
    # --------------------------------------------------------

    df["drug_name"] = (
        df["drug_name"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # --------------------------------------------------------
    # MEDICAL CONDITION
    # --------------------------------------------------------

    df["medical_condition"] = (
        df["medical_condition"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # --------------------------------------------------------
    # REACTION
    # --------------------------------------------------------

    df["reaction"] = (
        df["reaction"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    df = df.drop_duplicates()

    # --------------------------------------------------------
    # TARGET
    #
    # 1 = hepatic reaction
    # 0 = non-hepatic reaction
    #
    # IMPORTANT:
    # This is a reaction-category classification task.
    # It does NOT mean FAERS contains true healthy controls.
    # --------------------------------------------------------

    df["adr_occurred"] = (
        df["reaction_category"]
        == "hepatic"
    ).astype(int)

    # --------------------------------------------------------
    # DRUG CLASS
    # --------------------------------------------------------

    df["drug_class"] = (
        df["drug_name"]
        .apply(
            classify_drug
        )
    )

    # --------------------------------------------------------
    # PREVIOUS ADR
    # --------------------------------------------------------

    df["previous_adr"] = 0

    return df


# ============================================================
# DRUG CLASSIFICATION
# ============================================================

def classify_drug(drug):

    drug = str(drug).lower()

    anti_tb = [
        "rifampin",
        "rifampicin",
        "isoniazid",
        "pyrazinamide",
        "ethambutol"
    ]

    antibiotics = [
        "amoxicillin",
        "azithromycin",
        "ciprofloxacin",
        "doxycycline",
        "metronidazole",
        "clarithromycin",
        "cephalexin",
        "ceftriaxone"
    ]

    nsaids = [
        "ibuprofen",
        "naproxen",
        "diclofenac",
        "aspirin"
    ]

    statins = [
        "atorvastatin",
        "simvastatin",
        "rosuvastatin",
        "pravastatin"
    ]

    if any(x in drug for x in anti_tb):
        return "anti_tb"

    if any(x in drug for x in antibiotics):
        return "antibiotic"

    if any(x in drug for x in nsaids):
        return "nsaid"

    if any(x in drug for x in statins):
        return "statin"

    return "other"


# ============================================================
# BUILD DATASET
# ============================================================

def build_dataset():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    reports = fetch_faers()

    if not reports:

        print(
            "No FAERS reports retrieved."
        )

        return

    df = process_reports(
        reports
    )

    print()
    print(
        "Rows before cleaning:",
        len(df)
    )

    df = clean_dataset(
        df
    )

    print(
        "Rows after cleaning:",
        len(df)
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(
        "================================"
    )

    print(
        "Dataset created successfully!"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print(
        "Shape:",
        df.shape
    )

    print()
    print(
        "Target distribution:"
    )

    print(
        df["adr_occurred"]
        .value_counts()
    )

    print()
    print(
        "Reaction categories:"
    )

    print(
        df["reaction_category"]
        .value_counts()
    )

    print()
    print(
        "Drug classes:"
    )

    print(
        df["drug_class"]
        .value_counts()
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    build_dataset()