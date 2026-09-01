"""Prediction inference service"""
import logging
import uuid
from typing import Optional
from backend.schemas import PatientInfo, MedicationInfo, PredictionResult, RiskFactor
from backend.services.model_loader import ModelLoader

logger = logging.getLogger(__name__)


class PredictionService:
    """Handles ADR risk prediction inference"""
    
    @staticmethod
    def predict(patient: PatientInfo, medication: MedicationInfo, use_enhanced: bool = True) -> PredictionResult:
        """
        Generate ADR risk prediction for a patient-medication pair
        
        Args:
            patient: Patient demographics and medical info
            medication: Medication details
            use_enhanced: If True, use enhanced model with blood group; else baseline
            
        Returns:
            PredictionResult with risk score, category, and top contributing factors
        """
        try:
            # Generate unique prediction ID
            prediction_id = f"pred_{uuid.uuid4().hex[:12]}"
            
            # Load appropriate model
            if use_enhanced:
                model = ModelLoader.load_enhanced_model()
                model_version = "enhanced-1.0.0"
            else:
                model = ModelLoader.load_baseline_model()
                model_version = "baseline-1.0.0"
            
            # TODO: Implement actual model inference here
            # For now, return a placeholder result
            risk_score = PredictionService._generate_mock_prediction(patient, medication)
            
            # Determine risk category
            if risk_score < 0.33:
                risk_category = "low"
            elif risk_score < 0.67:
                risk_category = "moderate"
            else:
                risk_category = "high"
            
            # Generate mock top factors (in real implementation, extract from SHAP)
            top_factors = [
                RiskFactor(
                    feature_name="age",
                    contribution=0.12,
                    direction="positive"
                ),
                RiskFactor(
                    feature_name="blood_group_O",
                    contribution=0.08,
                    direction="positive" if patient.blood_group == "O" else "neutral"
                ),
                RiskFactor(
                    feature_name="drug_class",
                    contribution=0.05,
                    direction="negative"
                )
            ]
            
            return PredictionResult(
                prediction_id=prediction_id,
                risk_score=round(risk_score, 4),
                risk_category=risk_category,
                top_factors=top_factors,
                model_version=model_version,
                confidence=0.85
            )
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise
    
    @staticmethod
    def _generate_mock_prediction(patient: PatientInfo, medication: MedicationInfo) -> float:
        """Generate a mock prediction score based on simple heuristics"""
        score = 0.3  # Base score
        
        # Age factor: older patients slightly higher risk
        if patient.age > 65:
            score += 0.15
        elif patient.age > 50:
            score += 0.08
        
        # Blood group factor (simplified)
        if patient.blood_group == "O":
            score += 0.1
        
        # Ensure score stays in [0, 1]
        return min(max(score, 0.0), 1.0)
