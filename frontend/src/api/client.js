/**
 * API client for communicating with the backend
 * Handles all HTTP requests to the ADR prediction API
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Predict ADR risk for a patient-medication pair
 * @param {Object} patient - Patient demographics and medical info
 * @param {Object} medication - Medication details
 * @param {boolean} useEnhanced - Use enhanced model with blood group
 * @returns {Promise<Object>} Prediction result with risk score, category, and factors
 */
export const predictADRRisk = async (patient, medication, useEnhanced = true) => {
  try {
    const response = await client.post('/predict', {
      patient,
      medication,
      use_enhanced: useEnhanced
    })
    return response.data
  } catch (error) {
    console.error('Error calling predict endpoint:', error)
    throw error
  }
}

/**
 * Get SHAP-based explanation for a prediction
 * @param {string} predictionId - ID of the prediction to explain
 * @returns {Promise<Object>} SHAP explanation with feature importance
 */
export const getExplanation = async (predictionId) => {
  try {
    const response = await client.get(`/explain/${predictionId}`)
    return response.data
  } catch (error) {
    console.error('Error fetching explanation:', error)
    throw error
  }
}

/**
 * Get SHAP summary plot for a prediction
 * @param {string} predictionId - ID of the prediction
 * @returns {Promise<Object>} Plot URL
 */
export const getExplanationPlot = async (predictionId) => {
  try {
    const response = await client.get(`/explain/plots/${predictionId}`)
    return response.data
  } catch (error) {
    console.error('Error fetching explanation plot:', error)
    throw error
  }
}

export default client
