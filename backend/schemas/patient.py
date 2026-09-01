"""Pydantic schema for patient demographic and medical information"""
from pydantic import BaseModel, Field
from typing import Optional


class PatientInfo(BaseModel):
    """Patient demographic and medical history"""
    age: int = Field(..., ge=0, le=120, description="Patient age in years")
    sex: str = Field(..., description="Patient sex: M or F")
    blood_group: Optional[str] = Field(None, description="Blood group: O, A, B, AB")
    weight_kg: Optional[float] = Field(None, ge=20, le=200, description="Weight in kg")
    conditions: Optional[list[str]] = Field(None, description="List of diagnosed conditions")
    
    class Config:
        example = {
            "age": 45,
            "sex": "M",
            "blood_group": "O",
            "weight_kg": 75.5,
            "conditions": ["hypertension", "diabetes"]
        }
