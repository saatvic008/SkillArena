import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Register() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { register, loading, error } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    const ok = await register(username, email, password)
    if (ok) navigate('/login')
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="w-full max-w-md animate-slide-up">
        <div className="text-center mb-8">
          <div className="inline-flex w-16 h-16 rounded-2xl bg-gradient-to-br from-arena-accent to-purple-600 items-center justify-center shadow-glow-lg mb-4">
            <span className="text-3xl">♞</span>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Join SkillArena</h1>
          <p className="text-arena-400">Create your account and start improving</p>
        </div>

        <form onSubmit={handleSubmit} className="glass-card p-8 space-y-5" id="register-form">
          {error && (
            <div className="p-3 rounded-lg bg-arena-danger/10 border border-arena-danger/30 text-arena-danger text-sm">
              {error}
            </div>
          )}

          <div>
            <label htmlFor="reg-username" className="block text-sm font-medium text-arena-300 mb-2">Username</label>
            <input id="reg-username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="input-field" placeholder="Choose a username" required minLength={3} />
          </div>

          <div>
            <label htmlFor="reg-email" className="block text-sm font-medium text-arena-300 mb-2">Email</label>
            <input id="reg-email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="input-field" placeholder="your@email.com" required />
          </div>

          <div>
            <label htmlFor="reg-password" className="block text-sm font-medium text-arena-300 mb-2">Password</label>
            <input id="reg-password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="input-field" placeholder="Min 8 characters" required minLength={8} />
          </div>

          <button type="submit" disabled={loading} className="w-full btn-primary disabled:opacity-50" id="register-submit">
            {loading ? 'Creating account...' : 'Create Account'}
          </button>

          <p className="text-center text-sm text-arena-400">
            Already have an account?{' '}
            <Link to="/login" className="text-arena-accent hover:text-arena-300 transition-colors">Sign in</Link>
          </p>
        </form>
      </div>
    </div>
  )
}
