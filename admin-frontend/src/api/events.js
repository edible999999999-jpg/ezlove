import { api } from './request'

export const getEvents = (params) => api.get('/community/events', params)
export const createEvent = (data) => api.post('/community/events', data)
export const resolveEvent = (id) => api.put(`/community/events/${id}/resolve`)
