import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

const client = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
})

// Request interceptor: attach JWT
client.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: handle 401 + token refresh
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = useAuthStore.getState().refreshToken
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          })
          const { access_token, refresh_token } = res.data
          useAuthStore.getState().setTokens(access_token, refresh_token)
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return client(originalRequest)
        } catch {
          useAuthStore.getState().logout()
        }
      }
    }
    return Promise.reject(error)
  }
)

export default client
