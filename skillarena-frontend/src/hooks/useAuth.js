import { useState, useCallback } from 'react'
import { useAuthStore } from '../store/authStore'
import client from '../api/client'

export function useAuth() {
  const { accessToken, player, setTokens, setPlayer, logout } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const login = useCallback(async (username, password) => {
    setLoading(true)
    setError(null)
    try {
      const res = await client.post('/auth/login', { username, password })
      setTokens(res.data.access_token, res.data.refresh_token)
      return true
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed')
      return false
    } finally {
      setLoading(false)
    }
  }, [setTokens])

  const register = useCallback(async (username, email, password) => {
    setLoading(true)
    setError(null)
    try {
      const res = await client.post('/auth/register', { username, email, password })
      setPlayer(res.data)
      return true
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
      return false
    } finally {
      setLoading(false)
    }
  }, [setPlayer])

  return { accessToken, player, loading, error, login, register, logout }
}
