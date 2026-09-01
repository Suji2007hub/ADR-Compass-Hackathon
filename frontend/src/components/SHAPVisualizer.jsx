/**
 * SHAP Visualizer Component
 * Renders SHAP explanation output
 */
import React from 'react'
import { FactorBar } from './FactorBar'
import '../styles/theme.css'

export const SHAPVisualizer = ({ explanation }) => {
  if (!explanation) {
    return <div className="shap-visualizer">No explanation available</div>
  }

  return (
    <div className="shap-visualizer">
      <h3>Feature Importance (SHAP)</h3>
      
      <div className="shap-section">
        <h4>Top Contributing Factors</h4>
        <div className="factors-list">
          {explanation.shap_values && explanation.shap_values.map((factor, idx) => (
            <FactorBar
              key={idx}
              featureName={factor.feature}
              contribution={factor.value}
              direction={factor.value > 0 ? 'positive' : 'negative'}
            />
          ))}
        </div>
      </div>

      {explanation.interpretation && (
        <div className="shap-section interpretation">
          <h4>Interpretation</h4>
          <p>{explanation.interpretation}</p>
        </div>
      )}

      {explanation.feature_importance?.global && (
        <div className="shap-section">
          <h4>Global Feature Importance</h4>
          <div className="feature-importance-grid">
            {Object.entries(explanation.feature_importance.global).map(([feature, importance]) => (
              <div key={feature} className="importance-item">
                <span className="feature-name">{feature}</span>
                <span className="importance-value">{(importance * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default SHAPVisualizer
