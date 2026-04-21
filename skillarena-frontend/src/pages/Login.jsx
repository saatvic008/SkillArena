import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const { login, loading, error } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    const ok = await login(username, password)
    if (ok) navigate('/dashboard')
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="w-full max-w-md animate-slide-up">
        <div className="text-center mb-8">
          <div className="inline-flex w-16 h-16 rounded-2xl bg-gradient-to-br from-arena-accent to-purple-600 items-center justify-center shadow-glow-lg mb-4">
            <span className="text-3xl">♞</span>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-arena-400">Sign in to your SkillArena account</p>
        </div>

        <form onSubmit={handleSubmit} className="glass-card p-8 space-y-5" id="login-form">
          {error && (
            <div className="p-3 rounded-lg bg-arena-danger/10 border border-arena-danger/30 text-arena-danger text-sm">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="login-username" className="block text-sm font-medium text-arena-300 mb-2">Username</label>
            <input
              id="login-username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="input-field"
              placeholder="Enter your username"
              required
            />
          </div>

          <div>
            <label htmlFor="login-password" className="block text-sm font-medium text-arena-300 mb-2">Password</label>
            <input
              id="login-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="input-field"
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" disabled={loading} className="w-full btn-primary disabled:opacity-50" id="login-submit">
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <p className="text-center text-sm text-arena-400">
            Don't have an account?{' '}
            <Link to="/register" className="text-arena-accent hover:text-arena-300 transition-colors">
              Create one
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}
