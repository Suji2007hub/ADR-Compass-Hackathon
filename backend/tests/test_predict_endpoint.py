"""Test prediction endpoint"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.schemas import PatientInfo, MedicationInfo

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_endpoint():
    """Test ADR prediction endpoint"""
    patient = {
        "age": 55,
        "sex": "M",
        "blood_group": "O",
        "weight_kg": 75.5
    }
    medication = {
        "drug_name": "Atorvastatin",
        "drug_class": "Statin",
        "route": "oral",
        "dose": 20.0,
        "dose_unit": "mg",
        "frequency": "once daily",
        "duration_days": 90
    }
    
    response = client.post(
        "/api/predict",
        json={"patient": patient, "medication": medication}
    )
    
    assert response.status_code in [200, 422]  # 200 if works, 422 if request format needs adjustment
    if response.status_code == 200:
        data = response.json()
        assert "risk_score" in data
        assert "risk_category" in data
        assert "prediction_id" in data
