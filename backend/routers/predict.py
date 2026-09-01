"""Prediction API routes"""
from fastapi import APIRouter, HTTPException
from backend.schemas import PatientInfo, MedicationInfo, PredictionResult
from backend.services import PredictionService

router = APIRouter()


@router.post("/predict", response_model=PredictionResult)
async def predict_adr_risk(patient: PatientInfo, medication: MedicationInfo, use_enhanced: bool = True) -> PredictionResult:
    """
    Predict ADR risk for a given patient-medication combination
    
    Args:
        patient: Patient demographic and medical information
        medication: Medication details
        use_enhanced: Whether to use enhanced model (with blood group) or baseline
        
    Returns:
        PredictionResult containing risk score, category, and top contributing factors
    """
    try:
        prediction = PredictionService.predict(patient, medication, use_enhanced=use_enhanced)
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
