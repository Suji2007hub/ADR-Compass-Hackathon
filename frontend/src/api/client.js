/**
 * API client for ADR-Compass
 */

import axios from 'axios'

// Render backend URL
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  'https://adr-compass-hackathon.onrender.com'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000,
})

/**
 * Complete ADR risk assessment
 *
 * Sends patient + medication information
 * to Model A and Model B through /assess.
 */
export const predictADRRisk = async (
  patient,
  medication,
  useEnhanced = true
) => {
  try {
    const payload = {
      age: Number(patient.age),
      sex: patient.sex,

      drug_name: medication.drug_name,
      drug_class: medication.drug_class,
      medical_condition: medication.medical_condition,
      previous_adr: Number(medication.previous_adr ?? 0),

      blood_group: useEnhanced
        ? medication.blood_group ?? patient.blood_group ?? null
        : null,

      rh_factor: useEnhanced
        ? medication.rh_factor ?? patient.rh_factor ?? null
        : null,
    }

    console.log('Sending assessment:', payload)

    const response = await client.post('/assess', payload)

    console.log('Assessment response:', response.data)

    return response.data
  } catch (error) {
    console.error('ADR assessment failed:', error)

    if (error.response) {
      throw new Error(
        `Backend error (${error.response.status}): ${
          error.response.data?.detail || 'Unable to complete assessment'
        }`
      )
    }

    if (error.request) {
      throw new Error(
        'Unable to connect to the ADR-Compass backend. Please check that the backend is deployed and running.'
      )
    }

    throw new Error(error.message || 'Unable to generate prediction')
  }
}

/**
 * Optional explanation endpoint.
 *
 * Kept for compatibility with the dashboard.
 */
export const getExplanation = async (predictionId) => {
  try {
    const response = await client.get(`/explain/${predictionId}`)
    return response.data
  } catch (error) {
    console.error('Explanation request failed:', error)

    if (error.response) {
      throw new Error(
        `Explanation error (${error.response.status}): ${
          error.response.data?.detail || 'Explanation unavailable'
        }`
      )
    }

    throw new Error('Unable to retrieve explanation')
  }
}

/**
 * Optional SHAP plot endpoint.
 */
export const getExplanationPlot = async (predictionId) => {
  try {
    const response = await client.get(
      `/explain/plots/${predictionId}`
    )

    return response.data
  } catch (error) {
    console.error('Explanation plot request failed:', error)

    if (error.response) {
      throw new Error(
        `Explanation plot error (${error.response.status})`
      )
    }

    throw new Error('Unable to retrieve explanation plot')
  }
}

export default client