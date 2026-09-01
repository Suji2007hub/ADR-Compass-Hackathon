"""Pydantic schema for medication information"""
from pydantic import BaseModel, Field
from typing import Optional


class MedicationInfo(BaseModel):
    """Medication details for ADR risk assessment"""
    drug_name: str = Field(..., description="Name of the drug/medication")
    drug_class: Optional[str] = Field(None, description="Therapeutic drug class (e.g., Statin, ACE inhibitor)")
    route: str = Field(..., description="Route of administration: oral, IV, IM, topical, etc.")
    dose: float = Field(..., gt=0, description="Dose amount")
    dose_unit: str = Field(..., description="Unit of dose: mg, mcg, mL, etc.")
    frequency: str = Field(..., description="Frequency: daily, twice daily, weekly, etc.")
    duration_days: Optional[int] = Field(None, ge=1, description="Expected or actual treatment duration in days")
    
    class Config:
        example = {
            "drug_name": "Atorvastatin",
            "drug_class": "Statin",
            "route": "oral",
            "dose": 20.0,
            "dose_unit": "mg",
            "frequency": "once daily",
            "duration_days": 90
        }
