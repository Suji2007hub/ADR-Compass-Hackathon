# Project Structure Setup Summary

## ✅ Complete Directory Structure Created

### Backend (FastAPI) — `/backend/`
- **main.py** — FastAPI application entry point with CORS setup and route registration
- **config.py** — Configuration management (model paths, API settings, environment variables)
- **.env.example** — Environment variable template
- **requirements.txt** — Python dependencies (FastAPI, Uvicorn, Pydantic, XGBoost, SHAP, etc.)

#### Subdirectories:
- **routers/** — API route handlers
  - `predict.py` — POST /api/predict endpoint for ADR risk prediction
  - `explain.py` — GET /api/explain/{prediction_id} and /api/explain/plots/{prediction_id} endpoints
  - `__init__.py`

- **schemas/** — Pydantic request/response models
  - `patient.py` — PatientInfo schema (age, sex, blood_group, weight, conditions)
  - `medication.py` — MedicationInfo schema (drug_name, drug_class, route, dose, frequency, duration)
  - `prediction.py` — PredictionResult schema (risk_score, risk_category, top_factors, confidence)
  - `__init__.py`

- **services/** — Business logic layer
  - `model_loader.py` — ModelLoader class for loading baseline and enhanced models
  - `prediction_service.py` — PredictionService class for inference
  - `explanation_service.py` — ExplanationService class for SHAP explanations
  - `__init__.py`

- **tests/** — Unit tests
  - `test_predict_endpoint.py` — Test health check and prediction endpoints

### Frontend (React/Vite) — `/frontend/`
- **package.json** — Node.js dependencies (React, Axios, react-hook-form, Vite)
- **vite.config.js** — Vite configuration with API proxy
- **index.html** — HTML entry point
- **.env.example** — Environment variable template (VITE_API_BASE_URL)
- **.gitignore** — Git ignore rules for Node modules and build artifacts

#### Subdirectories:
- **src/main.jsx** — React application entry point

- **src/App.jsx** — Main app component with multi-step form state management

- **src/api/** — API communication
  - `client.js` — Axios client with predictADRRisk(), getExplanation(), getExplanationPlot() functions

- **src/components/** — Reusable UI components
  - `DisclaimerBanner.jsx` — Persistent medical disclaimer
  - `RiskScoreCard.jsx` — Risk score display with visual indicator
  - `FactorBar.jsx` — Individual SHAP feature contribution bar
  - `SHAPVisualizer.jsx` — SHAP explanation visualization
  - `Stepper.jsx` — Multi-step form navigation

- **src/pages/** — Page components for each step
  - `PatientInfoPage.jsx` — Step 1: Patient demographics input form
  - `MedicationInfoPage.jsx` — Step 2: Medication details input form
  - `PredictionDashboardPage.jsx` — Step 3: Results with SHAP explanations

- **src/styles/** — CSS styling
  - `theme.css` — Comprehensive theme with CSS variables, component styles, responsive design

- **src/utils/** — Helper functions
  - `formatters.js` — Formatting functions for risk scores, confidence, dates, etc.

- **public/** — Static assets
  - `assets/` — Placeholder for images/logos

### Project Root
- **README.md** — Complete project documentation with setup, deployment, and API reference
- **docker-compose.yml** — Docker Compose configuration for running backend + frontend together
- **.gitignore** — Root-level Git ignore rules (Python, Node.js, data, models, environments)

---

## 📋 Ownership & Development Map

| Folder | Owner | Responsibility |
|--------|-------|-----------------|
| `docs/` | Member 1 | Documentation, research references, data dictionary |
| `data/`, `preprocessing/` | Member 2 | Data loading, cleaning, feature engineering |
| `models/` | Member 3 | Model training, evaluation, significance testing |
| `explainability/` | Member 4 | SHAP analysis, feature importance, case explanations |
| `backend/` | Member 5 | FastAPI service, API routes, inference pipelines |
| `frontend/` | Member 5 (or co-owned) | React UI, forms, result visualization |
| `pitch/`, `notebooks/` | Everyone | Presentation, exploratory analysis |

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Configure Environment
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env as needed

# Frontend
cp frontend/.env.example frontend/.env.local
# Adjust VITE_API_BASE_URL if needed
```

### 3. Run Servers
**Terminal 1:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

**Visit:** http://localhost:5173

---

## 🔌 API Contract (Backend ↔ Frontend)

### Patient Information
```json
{
  "age": 45,
  "sex": "M",
  "blood_group": "O",
  "weight_kg": 75.5,
  "conditions": ["hypertension"]
}
```

### Medication Information
```json
{
  "drug_name": "Atorvastatin",
  "drug_class": "Statin",
  "route": "oral",
  "dose": 20.0,
  "dose_unit": "mg",
  "frequency": "once daily",
  "duration_days": 90
}
```

### Prediction Response
```json
{
  "prediction_id": "pred_12345abc",
  "risk_score": 0.72,
  "risk_category": "high",
  "top_factors": [
    {
      "feature_name": "age",
      "contribution": 0.15,
      "direction": "positive"
    }
  ],
  "model_version": "enhanced-1.0.0",
  "confidence": 0.85
}
```

---

## 📂 File Checklist

### Backend
- ✅ main.py
- ✅ config.py
- ✅ requirements.txt
- ✅ .env.example
- ✅ routers/__init__.py, predict.py, explain.py
- ✅ schemas/__init__.py, patient.py, medication.py, prediction.py
- ✅ services/__init__.py, model_loader.py, prediction_service.py, explanation_service.py
- ✅ tests/test_predict_endpoint.py

### Frontend
- ✅ package.json
- ✅ vite.config.js
- ✅ index.html
- ✅ .env.example
- ✅ .gitignore
- ✅ src/main.jsx
- ✅ src/App.jsx
- ✅ src/api/client.js
- ✅ src/components/ (5 components)
- ✅ src/pages/ (3 pages)
- ✅ src/styles/theme.css
- ✅ src/utils/formatters.js
- ✅ public/assets/

### Root
- ✅ README.md
- ✅ docker-compose.yml
- ✅ .gitignore

---

## 🎯 Next Steps

1. **Install dependencies** and verify both servers start without errors
2. **Test API endpoints** using the Swagger UI at `http://localhost:8000/docs`
3. **Verify CORS** by checking browser console when frontend calls backend
4. **Implement actual model inference** in backend/services/prediction_service.py (currently uses mock)
5. **Implement SHAP integration** in backend/services/explanation_service.py
6. **Add real patient/medication data** to backend/services/model_loader.py paths
7. **Configure CI/CD** and deployment for production

---

## 📝 Notes

- **Placeholder Models**: The backend currently uses mock predictions. Replace `PredictionService._generate_mock_prediction()` with actual model inference once trained models are available.
- **CORS Setup**: Allows `localhost:5173` and `localhost:3000` by default. Update `.env` for production.
- **Git LFS**: Consider using Git LFS for large model artifacts in `models/saved/`.
- **Data Privacy**: Ensure compliance with HIPAA or equivalent regulations when handling patient data.
- **Disclaimer**: The app includes a persistent medical disclaimer banner emphasizing decision-support nature.

