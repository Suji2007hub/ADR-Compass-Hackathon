from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="ADR Risk Prediction API",
    description="Predicts adverse drug reaction risk with SHAP explainability",
    version="1.0.0"
)

# Configure CORS for frontend development and deployment
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers
from backend.routers import predict, explain

app.include_router(predict.router, prefix="/api", tags=["predictions"])
app.include_router(explain.router, prefix="/api", tags=["explanations"])


@app.get("/")
def root():
    """Health check endpoint"""
    return {"message": "ADR Risk Prediction API is running"}


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "ADR Risk Prediction API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
