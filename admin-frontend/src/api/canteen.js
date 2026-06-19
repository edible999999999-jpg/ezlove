import { api } from './request'
import request from './request'

export const submitCanteen = (formData) =>
  request.post('/community/canteen/submit', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
export const getCanteenRecords = () => api.get('/community/canteen/records')
export const getCanteenRecord = (id) => api.get(`/community/canteen/records/${id}`)
export const correctCanteenRecord = (id, data) =>
  api.put(`/community/canteen/records/${id}`, data)
