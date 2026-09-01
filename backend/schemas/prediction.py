"""Pydantic schema for ADR risk prediction results"""
from pydantic import BaseModel, Field
from typing import Optional, List


class RiskFactor(BaseModel):
    """Single contributing factor to ADR risk (from SHAP)"""
    feature_name: str = Field(..., description="Name of the feature")
    contribution: float = Field(..., description="SHAP value contribution")
    direction: str = Field(..., description="'positive' or 'negative' — increases or decreases risk")


class PredictionResult(BaseModel):
    """ADR risk prediction output"""
    prediction_id: str = Field(..., description="Unique identifier for this prediction")
    risk_score: float = Field(..., ge=0, le=1, description="Probability of ADR (0-1)")
    risk_category: str = Field(..., description="'low', 'moderate', or 'high'")
    top_factors: List[RiskFactor] = Field(..., description="Top contributing factors")
    model_version: str = Field(..., description="Version of model used")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Model confidence in prediction")
    
    class Config:
        example = {
            "prediction_id": "pred_12345abc",
            "risk_score": 0.72,
            "risk_category": "high",
            "top_factors": [
                {
                    "feature_name": "age",
                    "contribution": 0.15,
                    "direction": "positive"
                },
                {
                    "feature_name": "blood_group_O",
                    "contribution": 0.08,
                    "direction": "positive"
                }
            ],
            "model_version": "1.0.0",
            "confidence": 0.85
        }
