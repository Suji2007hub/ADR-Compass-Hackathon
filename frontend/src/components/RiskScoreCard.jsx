/**
 * Risk Score Card Component
 * Displays the ADR risk score with visual indicators
 */
import React from 'react'
import '../styles/theme.css'

export const RiskScoreCard = ({ riskScore, riskCategory, confidence }) => {
  const getRiskColor = (category) => {
    switch (category) {
      case 'low':
        return '#28a745'
      case 'moderate':
        return '#ffc107'
      case 'high':
        return '#dc3545'
      default:
        return '#6c757d'
    }
  }

  const getRiskLabel = (category) => {
    return category.charAt(0).toUpperCase() + category.slice(1)
  }

  return (
    <div className="risk-score-card">
      <h2>ADR Risk Assessment</h2>
      <div className="risk-score-display">
        <div
          className="risk-score-circle"
          style={{
            borderColor: getRiskColor(riskCategory),
            color: getRiskColor(riskCategory)
          }}
        >
          <div className="risk-score-value">{(riskScore * 100).toFixed(1)}%</div>
          <div className="risk-score-label">{getRiskLabel(riskCategory)}</div>
        </div>
        {confidence && (
          <div className="confidence-badge">
            Model Confidence: {(confidence * 100).toFixed(0)}%
          </div>
        )}
      </div>
    </div>
  )
}

export default RiskScoreCard
