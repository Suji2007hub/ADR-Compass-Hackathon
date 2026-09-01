"""Model loading and initialization service"""
import pickle
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ModelLoader:
    """Handles loading and caching trained models"""
    
    _baseline_model = None
    _enhanced_model = None
    
    @classmethod
    def load_baseline_model(cls):
        """Load baseline model (no blood group feature)"""
        if cls._baseline_model is None:
            try:
                from backend.config import BASELINE_MODEL_PATH
                if os.path.exists(BASELINE_MODEL_PATH):
                    with open(BASELINE_MODEL_PATH, 'rb') as f:
                        cls._baseline_model = pickle.load(f)
                    logger.info(f"Loaded baseline model from {BASELINE_MODEL_PATH}")
                else:
                    logger.warning(f"Baseline model not found at {BASELINE_MODEL_PATH}")
                    # Return a mock/placeholder model for demo purposes
                    cls._baseline_model = {"status": "placeholder"}
            except Exception as e:
                logger.error(f"Error loading baseline model: {e}")
                cls._baseline_model = {"status": "error", "message": str(e)}
        return cls._baseline_model
    
    @classmethod
    def load_enhanced_model(cls):
        """Load enhanced model (includes blood group feature)"""
        if cls._enhanced_model is None:
            try:
                from backend.config import ENHANCED_MODEL_PATH
                if os.path.exists(ENHANCED_MODEL_PATH):
                    with open(ENHANCED_MODEL_PATH, 'rb') as f:
                        cls._enhanced_model = pickle.load(f)
                    logger.info(f"Loaded enhanced model from {ENHANCED_MODEL_PATH}")
                else:
                    logger.warning(f"Enhanced model not found at {ENHANCED_MODEL_PATH}")
                    # Return a mock/placeholder model for demo purposes
                    cls._enhanced_model = {"status": "placeholder"}
            except Exception as e:
                logger.error(f"Error loading enhanced model: {e}")
                cls._enhanced_model = {"status": "error", "message": str(e)}
        return cls._enhanced_model
    
    @classmethod
    def clear_cache(cls):
        """Clear cached models (useful for testing)"""
        cls._baseline_model = None
        cls._enhanced_model = None
