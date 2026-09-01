/**
 * Main App component
 * Manages multi-step form flow and state
 */
import React, { useState } from 'react'
import { DisclaimerBanner } from './components/DisclaimerBanner'
import { Stepper } from './components/Stepper'
import { PatientInfoPage } from './pages/PatientInfoPage'
import { MedicationInfoPage } from './pages/MedicationInfoPage'
import { PredictionDashboardPage } from './pages/PredictionDashboardPage'
import { predictADRRisk } from './api/client'
import './styles/theme.css'

function App() {
  const [currentStep, setCurrentStep] = useState(0)
  const [patientData, setPatientData] = useState(null)
  const [medicationData, setMedicationData] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const stepLabels = ['Patient Info', 'Medication Info', 'Results']

  const handlePatientNext = (data) => {
    setPatientData(data)
    setCurrentStep(1)
    setError(null)
  }

  const handleMedicationNext = async (data) => {
    setMedicationData(data)
    setLoading(true)
    setError(null)

    try {
      const result = await predictADRRisk(patientData, data, true)
      setPrediction(result)
      setCurrentStep(2)
    } catch (err) {
      setError('Failed to generate prediction: ' + err.message)
      console.error('Prediction error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleMedicationBack = () => {
    setCurrentStep(0)
  }

  const handleReset = () => {
    setCurrentStep(0)
    setPatientData(null)
    setMedicationData(null)
    setPrediction(null)
    setError(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>ADR Risk Prediction</h1>
        <p>Adverse Drug Reaction Risk Assessment Tool</p>
      </header>

      <DisclaimerBanner />

      <main className="app-main">
        <Stepper
          currentStep={currentStep}
          totalSteps={stepLabels.length}
          stepLabels={stepLabels}
        />

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {currentStep === 0 && (
          <PatientInfoPage
            onNext={handlePatientNext}
            initialData={patientData}
          />
        )}

        {currentStep === 1 && (
          <MedicationInfoPage
            onNext={handleMedicationNext}
            onBack={handleMedicationBack}
            initialData={medicationData}
          />
        )}

        {currentStep === 2 && (
          <PredictionDashboardPage
            prediction={prediction}
            onReset={handleReset}
          />
        )}

        {loading && (
          <div className="loading">
            <p>Generating prediction...</p>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>
          This tool is for research and decision support only. Always consult qualified healthcare providers.
        </p>
      </footer>

      <style>{`
        .app {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
          background-color: var(--bg-secondary);
        }

        .app-header {
          background: linear-gradient(135deg, var(--color-primary) 0%, #0056b3 100%);
          color: white;
          padding: 3rem 1.5rem;
          text-align: center;
          box-shadow: var(--shadow-md);
        }

        .app-header h1 {
          margin-bottom: 0.5rem;
          font-size: 2.5rem;
        }

        .app-header p {
          margin-bottom: 0;
          font-size: 1.1rem;
          opacity: 0.95;
        }

        .app-main {
          flex: 1;
          max-width: 1200px;
          width: 100%;
          margin: 0 auto;
          padding: var(--spacing-lg);
        }

        .app-footer {
          background-color: var(--color-dark);
          color: white;
          padding: var(--spacing-lg);
          text-align: center;
          font-size: var(--font-size-sm);
        }

        .app-footer p {
          margin-bottom: 0;
        }

        @media (max-width: 768px) {
          .app-header {
            padding: 2rem 1rem;
          }

          .app-header h1 {
            font-size: 1.75rem;
          }

          .app-header p {
            font-size: 1rem;
          }

          .app-main {
            padding: var(--spacing-md);
          }
        }
      `}</style>
    </div>
  )
}

export default App
