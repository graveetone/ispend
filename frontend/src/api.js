import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
})

// Transactions
export const fetchTransactions = ({ transaction_type, date } = {}) => {
  const params = {}
  if (transaction_type) params.transaction_type = transaction_type
  if (date) params.date = date
  return api.get('/api/v1/transactions/', { params }).then(r => r.data)
}

export const createTransaction = (payload) => api.post('/api/v1/transactions/', payload).then(r => r.data)
export const getTransaction = (id) => api.get(`/api/v1/transactions/${id}/`).then(r => r.data)
export const updateTransaction = (id, payload) => api.patch(`/api/v1/transactions/${id}/`, payload).then(r => r.data)
export const deleteTransaction = (id) => api.delete(`/api/v1/transactions/${id}/`).then(r => r.status === 204)

// Plans
export const editPlan = (payload) => api.post('/api/v1/plans/', payload).then(r => r.data)

// Month summary
export const getMonthSummary = (month) => api.get(`/api/v1/months/${month}`).then(r => r.data)

export const getMonthTransactions = (month) => api.get(`/api/v1/months/${month}`).then(r => r.data)
export const getCategories = (transaction_type) => api.get(`/api/v1/categories`, { params: { transaction_type } }).then(r => r.data)


export default api