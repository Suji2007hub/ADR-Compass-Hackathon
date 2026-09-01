/**
 * Stepper Component
 * Multi-step form navigation
 */
import React from 'react'
import '../styles/theme.css'

export const Stepper = ({ currentStep, totalSteps, stepLabels, onStepChange }) => {
  return (
    <div className="stepper-container">
      <div className="steps">
        {stepLabels.map((label, idx) => (
          <div
            key={idx}
            className={`step ${idx === currentStep ? 'active' : ''} ${idx < currentStep ? 'completed' : ''}`}
            onClick={() => onStepChange && onStepChange(idx)}
          >
            <div className="step-number">{idx + 1}</div>
            <div className="step-label">{label}</div>
          </div>
        ))}
      </div>
      <div className="step-indicator">
        Step {currentStep + 1} of {totalSteps}
      </div>
    </div>
  )
}

export default Stepper
