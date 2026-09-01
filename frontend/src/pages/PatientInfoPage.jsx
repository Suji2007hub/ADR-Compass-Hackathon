/**
 * Patient Info Page
 * Collects patient demographics and medical history
 */
import React, { useState } from 'react'
import { useForm } from 'react-hook-form'

export const PatientInfoPage = ({ onNext, initialData }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: initialData || {
      age: '',
      sex: '',
      blood_group: '',
      weight_kg: ''
    }
  })

  const onSubmit = (data) => {
    onNext(data)
  }

  return (
    <div className="page patient-info-page">
      <h2>Patient Information</h2>
      
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="form-group">
          <label>Age (years)*</label>
          <input
            type="number"
            min="0"
            max="120"
            {...register('age', {
              required: 'Age is required',
              min: { value: 0, message: 'Age must be >= 0' },
              max: { value: 120, message: 'Age must be <= 120' }
            })}
          />
          {errors.age && <span className="error">{errors.age.message}</span>}
        </div>

        <div className="form-group">
          <label>Sex*</label>
          <select {...register('sex', { required: 'Sex is required' })}>
            <option value="">Select...</option>
            <option value="M">Male</option>
            <option value="F">Female</option>
          </select>
          {errors.sex && <span className="error">{errors.sex.message}</span>}
        </div>

        <div className="form-group">
          <label>Blood Group</label>
          <select {...register('blood_group')}>
            <option value="">Unknown</option>
            <option value="O">O</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="AB">AB</option>
          </select>
        </div>

        <div className="form-group">
          <label>Weight (kg)</label>
          <input
            type="number"
            min="20"
            max="200"
            step="0.1"
            {...register('weight_kg')}
          />
        </div>

        <button type="submit" className="btn btn-primary">
          Next: Medication Information
        </button>
      </form>
    </div>
  )
}

export default PatientInfoPage
