const API_BASE_URL = '/api'

export const predictADRRisk = async (patient, medication) => {
  const payload = {
    age: Number(patient.age),
    sex: patient.sex,
    drug_name: medication.drug_name,
    drug_class: medication.drug_class,
    medical_condition: medication.medical_condition,
    previous_adr: Number(patient.previous_adr ?? 0),
    blood_group: patient.blood_group || null,
    rh_factor: patient.rh_factor || null
  }

  console.log('API URL:', `${API_BASE_URL}/assess`)
  console.log('API PAYLOAD:', payload)

  try {
    const response = await fetch('/api/assess', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    console.log('HTTP STATUS:', response.status)

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data?.detail || `Backend returned HTTP ${response.status}`
      )
    }

    return data
  } catch (error) {
    console.error('FETCH ERROR:', error)

    throw new Error(
      `Network error | URL: /api/assess | Message: ${
        error.message || 'Unknown error'
      }`
    )
  }
}

export const getExplanation = async (predictionId) => {
  const response = await fetch(`/api/explain/${predictionId}`)

  if (!response.ok) {
    throw new Error(`Backend returned HTTP ${response.status}`)
  }

  return response.json()
}

export const getExplanationPlot = async (predictionId) => {
  const response = await fetch(`/api/explain/plots/${predictionId}`)

  if (!response.ok) {
    throw new Error(`Backend returned HTTP ${response.status}`)
  }

  return response.json()
}

export default null