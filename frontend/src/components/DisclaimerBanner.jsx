/**
 * Disclaimer Banner Component
 * Persistent warning about decision-support nature of predictions
 */
import React from 'react'
import '../styles/theme.css'

export const DisclaimerBanner = () => {
  return (
    <div className="disclaimer-banner">
      <div className="disclaimer-content">
        <strong>⚠️ Medical Decision Support Tool</strong>
        <p>
          This tool provides predictive estimates based on machine learning models.
          Predictions are not a substitute for professional medical judgment.
          Always consult with qualified healthcare providers before making treatment decisions.
        </p>
      </div>
    </div>
  )
}

export default DisclaimerBanner
