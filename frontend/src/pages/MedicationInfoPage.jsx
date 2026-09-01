/**
 * Medication Info Page
 * Collects medication and dosing information
 */
import React from 'react'
import { useForm } from 'react-hook-form'

export const MedicationInfoPage = ({ onNext, onBack, initialData }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: initialData || {
      drug_name: '',
      drug_class: '',
      route: 'oral',
      dose: '',
      dose_unit: 'mg',
      frequency: 'once daily',
      duration_days: ''
    }
  })

  const onSubmit = (data) => {
    onNext(data)
  }

  return (
    <div className="page medication-info-page">
      <h2>Medication Information</h2>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group">
          <label>Drug Name*</label>
          <input
            type="text"
            placeholder="e.g., Atorvastatin"
            {...register('drug_name', { required: 'Drug name is required' })}
          />
          {errors.drug_name && <span className="error">{errors.drug_name.message}</span>}
        </div>

        <div className="form-group">
          <label>Drug Class</label>
          <input
            type="text"
            placeholder="e.g., Statin"
            {...register('drug_class')}
          />
        </div>

        <div className="form-group">
          <label>Route of Administration*</label>
          <select {...register('route', { required: 'Route is required' })}>
            <option value="oral">Oral</option>
            <option value="IV">Intravenous</option>
            <option value="IM">Intramuscular</option>
            <option value="topical">Topical</option>
            <option value="inhaled">Inhaled</option>
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Dose*</label>
            <input
              type="number"
              step="0.1"
              min="0"
              placeholder="Amount"
              {...register('dose', {
                required: 'Dose is required',
                min: { value: 0, message: 'Dose must be > 0' }
              })}
            />
            {errors.dose && <span className="error">{errors.dose.message}</span>}
          </div>

          <div className="form-group">
            <label>Unit</label>
            <select {...register('dose_unit')}>
              <option value="mg">mg</option>
              <option value="mcg">mcg</option>
              <option value="mL">mL</option>
              <option value="g">g</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label>Frequency*</label>
          <input
            type="text"
            placeholder="e.g., once daily, twice daily"
            {...register('frequency', { required: 'Frequency is required' })}
          />
          {errors.frequency && <span className="error">{errors.frequency.message}</span>}
        </div>

        <div className="form-group">
          <label>Treatment Duration (days)</label>
          <input
            type="number"
            min="1"
            placeholder="Expected or actual duration"
            {...register('duration_days')}
          />
        </div>

        <div className="form-buttons">
          <button type="button" onClick={onBack} className="btn btn-secondary">
            Back
          </button>
          <button type="submit" className="btn btn-primary">
            Get Risk Prediction
          </button>
        </div>
      </form>
    </div>
  )
}

export default MedicationInfoPage
