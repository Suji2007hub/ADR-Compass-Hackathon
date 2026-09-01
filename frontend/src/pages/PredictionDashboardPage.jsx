/**
 * Prediction Dashboard Page
 * Displays ADR risk prediction and SHAP explanation
 */
import React, { useState, useEffect } from 'react'
import { RiskScoreCard } from '../components/RiskScoreCard'
import { SHAPVisualizer } from '../components/SHAPVisualizer'
import { getExplanation } from '../api/client'

export const PredictionDashboardPage = ({ prediction, onReset }) => {
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchExplanation = async () => {
      if (!prediction) return
      
      setLoading(true)
      setError(null)
      try {
        const exp = await getExplanation(prediction.prediction_id)
        setExplanation(exp)
      } catch (err) {
        setError('Failed to load explanation: ' + err.message)
        console.error('Error fetching explanation:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchExplanation()
  }, [prediction])

  if (!prediction) {
    return <div className="page">No prediction available</div>
  }

  return (
    <div className="page prediction-dashboard-page">
      <h2>Prediction Results</h2>

      <RiskScoreCard
        riskScore={prediction.risk_score}
        riskCategory={prediction.risk_category}
        confidence={prediction.confidence}
      />

      <div className="prediction-details">
        <p><strong>Prediction ID:</strong> {prediction.prediction_id}</p>
        <p><strong>Model Version:</strong> {prediction.model_version}</p>
      </div>

      {loading && <div className="loading">Loading explanation...</div>}
      {error && <div className="error-message">{error}</div>}

      {explanation && !loading && (
        <SHAPVisualizer explanation={explanation} />
      )}

      <div className="dashboard-actions">
        <button onClick={onReset} className="btn btn-primary">
          New Prediction
        </button>
      </div>
    </div>
  )
}

export default PredictionDashboardPage
