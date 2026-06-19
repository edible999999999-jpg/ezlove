import { api } from './request'

export const login = (phone, password) =>
  api.post('/community/auth/login', { phone, password })
