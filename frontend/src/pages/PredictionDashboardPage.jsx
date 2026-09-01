/**
 * Prediction Dashboard Page
 * Displays ADR risk prediction and model comparison
 */
import React from 'react'
import { RiskScoreCard } from '../components/RiskScoreCard'

export const PredictionDashboardPage = ({ prediction, onReset }) => {
  if (!prediction) {
    return <div className="page">No prediction available</div>
  }

  const primary = prediction.primary_prediction
  const comparison = prediction.model_comparison
  const management = prediction.risk_management
  const experimental = prediction.experimental_feature

  return (
    <div className="page prediction-dashboard-page">
      <h2>Prediction Results</h2>

      <RiskScoreCard
        riskScore={primary?.risk_score}
        riskCategory={primary?.risk_level}
        confidence={primary?.adr_probability}
      />

      <div className="prediction-details">
        <h3>Patient Information</h3>

        <p>
          <strong>Age:</strong> {prediction.patient?.age}
        </p>

        <p>
          <strong>Sex:</strong> {prediction.patient?.sex}
        </p>

        <p>
          <strong>Blood Group:</strong>{' '}
          {prediction.patient?.blood_group || 'Unknown'}
        </p>

        <p>
          <strong>Rh Factor:</strong>{' '}
          {prediction.patient?.rh_factor || 'Unknown'}
        </p>

        <h3>Medication Information</h3>

        <p>
          <strong>Drug:</strong>{' '}
          {prediction.medication?.drug_name}
        </p>

        <p>
          <strong>Drug Class:</strong>{' '}
          {prediction.medication?.drug_class}
        </p>

        <p>
          <strong>Medical Condition:</strong>{' '}
          {prediction.medication?.medical_condition}
        </p>

        <p>
          <strong>Previous ADR:</strong>{' '}
          {prediction.medication?.previous_adr === 1 ? 'Yes' : 'No'}
        </p>

        <h3>Model Prediction</h3>

        <p>
          <strong>Primary Model:</strong>{' '}
          {primary?.model_name || 'N/A'}
        </p>

        <p>
          <strong>ADR Probability:</strong>{' '}
          {primary?.adr_probability != null
            ? `${(primary.adr_probability * 100).toFixed(2)}%`
            : 'N/A'}
        </p>

        <p>
          <strong>Risk Score:</strong>{' '}
          {primary?.risk_score ?? 'N/A'}
        </p>

        <p>
          <strong>Risk Level:</strong>{' '}
          {primary?.risk_level || 'N/A'}
        </p>
      </div>

      {comparison && (
        <div className="prediction-details">
          <h3>Model Comparison</h3>

          <p>
            <strong>Model A — Baseline:</strong>{' '}
            {comparison.model_a?.probability != null
              ? `${(comparison.model_a.probability * 100).toFixed(2)}%`
              : 'N/A'}{' '}
            ({comparison.model_a?.risk_level || 'N/A'})
          </p>

          <p>
            <strong>Model B — Enhanced:</strong>{' '}
            {comparison.model_b?.probability != null
              ? `${(comparison.model_b.probability * 100).toFixed(2)}%`
              : 'N/A'}{' '}
            ({comparison.model_b?.risk_level || 'N/A'})
          </p>

          <p>
            <strong>Probability Difference:</strong>{' '}
            {comparison.probability_difference != null
              ? `${(comparison.probability_difference * 100).toFixed(2)} percentage points`
              : 'N/A'}
          </p>
        </div>
      )}

      {management && (
        <div className="prediction-details">
          <h3>{management.title}</h3>

          <ul>
            {management.actions?.map((action, index) => (
              <li key={index}>{action}</li>
            ))}
          </ul>
        </div>
      )}

      {experimental && (
        <div className="prediction-details">
          <h3>Experimental Feature</h3>

          <p>
            <strong>Blood Group:</strong>{' '}
            {experimental.blood_group || 'Unknown'}
          </p>

          <p>
            {experimental.message}
          </p>
        </div>
      )}

      {prediction.disclaimer && (
        <div className="prediction-details">
          <h3>Clinical Disclaimer</h3>

          <p>{prediction.disclaimer}</p>
        </div>
      )}

      <div className="dashboard-actions">
        <button
          onClick={onReset}
          className="btn btn-primary"
        >
          New Prediction
        </button>
      </div>
    </div>
  )
}

export default PredictionDashboardPage

