import os
from dotenv import load_dotenv

load_dotenv()

# Model paths
MODEL_DIR = os.getenv("MODEL_DIR", "models/saved")
BASELINE_MODEL_PATH = os.path.join(MODEL_DIR, "baseline_model.pkl")
ENHANCED_MODEL_PATH = os.path.join(MODEL_DIR, "enhanced_model.pkl")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# SHAP configuration
SHAP_NUM_FEATURES = int(os.getenv("SHAP_NUM_FEATURES", 10))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
