/**
 * Formatters utility functions
 * Common formatting helpers for UI display
 */

export const formatRiskScore = (score) => {
  return (score * 100).toFixed(1) + '%'
}

export const formatConfidence = (confidence) => {
  return (confidence * 100).toFixed(0) + '%'
}

export const getRiskCategoryLabel = (category) => {
  return category.charAt(0).toUpperCase() + category.slice(1)
}

export const getRiskCategoryColor = (category) => {
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

export const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

export const truncateString = (str, length = 50) => {
  return str.length > length ? str.substring(0, length) + '...' : str
}
