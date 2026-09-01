/**
 * Factor Bar Component
 * Renders a single SHAP contributing factor to ADR risk
 */
import React from 'react'
import '../styles/theme.css'

export const FactorBar = ({ featureName, contribution, direction }) => {
  const getDirectionColor = (dir) => {
    return dir === 'positive' ? '#dc3545' : '#28a745'
  }

  const getDirectionLabel = (dir) => {
    if (dir === 'positive') return '↑ Increases risk'
    if (dir === 'negative') return '↓ Decreases risk'
    return '→ Neutral'
  }

  const barWidth = Math.abs(contribution) * 100

  return (
    <div className="factor-bar-container">
      <div className="factor-name">{featureName}</div>
      <div className="factor-bar-wrapper">
        <div
          className="factor-bar"
          style={{
            width: `${barWidth}%`,
            backgroundColor: getDirectionColor(direction)
          }}
        />
      </div>
      <div className="factor-info">
        <span className="factor-value">{Math.abs(contribution).toFixed(3)}</span>
        <span className="factor-direction">{getDirectionLabel(direction)}</span>
      </div>
    </div>
  )
}

export default FactorBar
