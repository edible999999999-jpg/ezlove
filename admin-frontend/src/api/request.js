import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
})

let isRefreshing = false
let refreshSubscribers = []

function onTokenRefreshed(newToken) {
  refreshSubscribers.forEach(cb => cb(newToken))
  refreshSubscribers = []
}

function addRefreshSubscriber(cb) {
  refreshSubscribers.push(cb)
}

function clearAuth() {
  localStorage.removeItem('community_access_token')
  localStorage.removeItem('community_refresh_token')
  localStorage.removeItem('community_worker')
  router.push('/login')
}

request.interceptors.request.use(config => {
  const token = localStorage.getItem('community_access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  response => response.data,
  async error => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      const refreshToken = localStorage.getItem('community_refresh_token')
      if (!refreshToken) {
        clearAuth()
        ElMessage.error('登录已过期，请重新登录')
        return Promise.reject(error)
      }

      if (isRefreshing) {
        return new Promise((resolve) => {
          addRefreshSubscriber((newToken) => {
            originalRequest.headers.Authorization = `Bearer ${newToken}`
            resolve(request(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const res = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/community/auth/refresh`,
          { refresh_token: refreshToken }
        )
        const newToken = res.data.access_token
        localStorage.setItem('community_access_token', newToken)
        if (res.data.refresh_token) {
          localStorage.setItem('community_refresh_token', res.data.refresh_token)
        }
        onTokenRefreshed(newToken)
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return request(originalRequest)
      } catch (refreshError) {
        clearAuth()
        ElMessage.error('登录已过期，请重新登录')
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    } else {
      ElMessage.error(error.response?.data?.detail || '请求失败')
    }
    return Promise.reject(error)
  }
)

export const api = {
  get: (url, params) => request.get(url, { params }),
  post: (url, data) => request.post(url, data),
  put: (url, data) => request.put(url, data),
  delete: (url) => request.delete(url),
}

export default request
