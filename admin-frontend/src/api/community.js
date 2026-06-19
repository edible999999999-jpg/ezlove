import { api } from './request'

export const getDashboard = () => api.get('/community/dashboard')
export const getElders = (params) => api.get('/community/elders', params)
export const createElder = (data) => api.post('/community/elders', data)
export const updateElder = (id, data) => api.put(`/community/elders/${id}`, data)
export const getElder = (id) => api.get(`/community/elders/${id}`)
