"""Explanation/SHAP API routes"""
from fastapi import APIRouter, HTTPException
from backend.services import ExplanationService

router = APIRouter()


@router.get("/explain/{prediction_id}")
async def get_explanation(prediction_id: str):
    """
    Get SHAP-based explanation for a prediction
    
    Args:
        prediction_id: ID of the prediction to explain
        
    Returns:
        Dictionary containing SHAP values, feature importance, and interpretation
    """
    try:
        explanation = ExplanationService.get_explanation(prediction_id)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation generation failed: {str(e)}")


@router.get("/explain/plots/{prediction_id}")
async def get_explanation_plot(prediction_id: str):
    """
    Get SHAP summary plot for a prediction
    
    Args:
        prediction_id: ID of the prediction
        
    Returns:
        Path to the generated plot image
    """
    try:
        plot_path = ExplanationService.generate_summary_plot(prediction_id)
        return {"plot_url": plot_path, "prediction_id": prediction_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plot generation failed: {str(e)}")
