from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import joblib
import pandas as pd


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="ADR-Compass API",
    description="ADR risk prediction and risk-management API",
    version="1.0.0",
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_A_PATH = BASE_DIR / "models" / "saved" / "model_a.pkl"
MODEL_B_PATH = BASE_DIR / "models" / "saved" / "model_b.pkl"


# ============================================================
# LOAD MODELS
# ============================================================

if not MODEL_A_PATH.exists():
    raise FileNotFoundError(f"Model A not found: {MODEL_A_PATH}")

if not MODEL_B_PATH.exists():
    raise FileNotFoundError(f"Model B not found: {MODEL_B_PATH}")


model_a = joblib.load(MODEL_A_PATH)
model_b = joblib.load(MODEL_B_PATH)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class PredictionRequest(BaseModel):
    age: float
    sex: str
    drug_name: str
    drug_class: str
    medical_condition: str
    previous_adr: int
    blood_group: str | None = None
    rh_factor: str | None = None


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(probability: float):

    if probability < 0.30:
        return "Low"

    elif probability < 0.60:
        return "Moderate"

    return "High"


# ============================================================
# RISK MANAGEMENT
# ============================================================

def get_risk_management(risk_level: str):

    if risk_level == "Low":

        return {
            "title": "Routine monitoring",
            "actions": [
                "Continue routine clinical monitoring.",
                "Review known adverse reactions associated with the medication.",
                "Educate the patient about symptoms that should be reported.",
            ],
        }

    elif risk_level == "Moderate":

        return {
            "title": "Enhanced monitoring recommended",
            "actions": [
                "Consider closer monitoring for adverse reactions.",
                "Review previous ADR history and concomitant medications.",
                "Monitor for clinically relevant symptoms associated with the medication.",
                "Consider healthcare-professional review if symptoms develop.",
            ],
        }

    return {
        "title": "Healthcare-professional review recommended",
        "actions": [
            "Flag the patient for clinical review.",
            "Consider enhanced monitoring for adverse reactions.",
            "Review medication history, interactions and patient-specific risk factors.",
            "Any medication decision should be made by a qualified healthcare professional.",
        ],
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {
        "message": "ADR-Compass API is running",
        "status": "healthy",
        "endpoints": [
            "POST /assess",
            "POST /predict/model-a",
            "POST /predict/model-b",
        ],
    }


# ============================================================
# COMPLETE ASSESSMENT
# ============================================================

@app.post("/assess")
def assess_patient(request: PredictionRequest):

    # --------------------------------------------------------
    # MODEL A INPUT
    # --------------------------------------------------------

    input_model_a = pd.DataFrame([
        {
            "age": request.age,
            "sex": request.sex,
            "drug_name": request.drug_name,
            "drug_class": request.drug_class,
            "medical_condition": request.medical_condition,
            "previous_adr": request.previous_adr,
        }
    ])

    # --------------------------------------------------------
    # MODEL B INPUT
    # --------------------------------------------------------

    input_model_b = pd.DataFrame([
        {
            "age": request.age,
            "sex": request.sex,
            "drug_name": request.drug_name,
            "drug_class": request.drug_class,
            "medical_condition": request.medical_condition,
            "previous_adr": request.previous_adr,
            "blood_group": request.blood_group,
            "rh_factor": request.rh_factor,
        }
    ])

    # --------------------------------------------------------
    # MODEL A
    # --------------------------------------------------------

    probability_a = float(
        model_a.predict_proba(input_model_a)[0][1]
    )

    risk_a = get_risk_level(probability_a)

    # --------------------------------------------------------
    # MODEL B
    # --------------------------------------------------------

    probability_b = float(
        model_b.predict_proba(input_model_b)[0][1]
    )

    risk_b = get_risk_level(probability_b)

    # --------------------------------------------------------
    # PRIMARY PREDICTION
    # --------------------------------------------------------

    primary_probability = probability_b
    primary_risk = risk_b

    # --------------------------------------------------------
    # RISK MANAGEMENT
    # --------------------------------------------------------

    management = get_risk_management(primary_risk)

    # --------------------------------------------------------
    # MODEL DIFFERENCE
    # --------------------------------------------------------

    probability_difference = probability_b - probability_a

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {

        "patient": {
            "age": request.age,
            "sex": request.sex,
            "blood_group": request.blood_group,
            "rh_factor": request.rh_factor,
        },

        "medication": {
            "drug_name": request.drug_name,
            "drug_class": request.drug_class,
            "medical_condition": request.medical_condition,
            "previous_adr": request.previous_adr,
        },

        "primary_prediction": {
            "model": "Model B",
            "model_name": "XGBoost (enhanced)",
            "adr_probability": round(primary_probability, 4),
            "risk_score": round(primary_probability * 100),
            "risk_level": primary_risk,
        },

        "model_comparison": {

            "model_a": {
                "name": "Model A — Baseline",
                "probability": round(probability_a, 4),
                "risk_level": risk_a,
            },

            "model_b": {
                "name": "Model B — Enhanced",
                "probability": round(probability_b, 4),
                "risk_level": risk_b,
            },

            "probability_difference": round(
                probability_difference,
                4,
            ),
        },

        "risk_management": management,

        "experimental_feature": {

            "blood_group": request.blood_group,
            "rh_factor": request.rh_factor,

            "message": (
                "Blood-group and Rh information are experimental "
                "features of Model B. They should not be interpreted "
                "as confirmed causal clinical factors."
            ),
        },

        "disclaimer": (
            "This system is a clinical decision-support prototype "
            "and is not a diagnostic or prescribing system. "
            "Predictions require review by a qualified healthcare professional."
        ),
    }


# ============================================================
# MODEL A ENDPOINT
# ============================================================

@app.post("/predict/model-a")
def predict_model_a(request: PredictionRequest):

    input_data = pd.DataFrame([
        {
            "age": request.age,
            "sex": request.sex,
            "drug_name": request.drug_name,
            "drug_class": request.drug_class,
            "medical_condition": request.medical_condition,
            "previous_adr": request.previous_adr,
        }
    ])

    probability = float(
        model_a.predict_proba(input_data)[0][1]
    )

    return {
        "model": "Model A",
        "adr_probability": round(probability, 4),
        "risk_score": round(probability * 100),
        "risk_level": get_risk_level(probability),
    }


# ============================================================
# MODEL B ENDPOINT
# ============================================================

@app.post("/predict/model-b")
def predict_model_b(request: PredictionRequest):

    input_data = pd.DataFrame([
        {
            "age": request.age,
            "sex": request.sex,
            "drug_name": request.drug_name,
            "drug_class": request.drug_class,
            "medical_condition": request.medical_condition,
            "previous_adr": request.previous_adr,
            "blood_group": request.blood_group,
            "rh_factor": request.rh_factor,
        }
    ])

    probability = float(
        model_b.predict_proba(input_data)[0][1]
    )

    return {
        "model": "Model B",
        "model_name": "XGBoost (enhanced)",
        "adr_probability": round(probability, 4),
        "risk_score": round(probability * 100),
        "risk_level": get_risk_level(probability),
        "blood_group_note": (
            "Blood-group information in Model B is experimental "
            "and should not be treated as clinical patient-level evidence."
        ),
    }