import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function Navbar() {
  const { accessToken, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="sticky top-0 z-50 glass-card border-b border-arena-700/50 rounded-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-arena-accent to-purple-600 flex items-center justify-center shadow-glow group-hover:shadow-glow-lg transition-all duration-300">
              <span className="text-white font-bold text-lg">♞</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-arena-accent to-arena-300 bg-clip-text text-transparent">
              SkillArena
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {accessToken ? (
              <>
                <NavLink to="/dashboard">Dashboard</NavLink>
                <NavLink to="/drills">Drills</NavLink>
                <NavLink to="/report">Analysis</NavLink>
                <NavLink to="/leaderboard">Leaderboard</NavLink>
                <button
                  onClick={handleLogout}
                  className="ml-4 px-4 py-2 text-sm text-arena-400 hover:text-white border border-arena-700 rounded-lg hover:border-arena-accent transition-all duration-200"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <NavLink to="/leaderboard">Leaderboard</NavLink>
                <Link to="/login" className="btn-primary text-sm px-4 py-2">
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

function NavLink({ to, children }) {
  return (
    <Link
      to={to}
      className="px-4 py-2 text-sm text-arena-400 hover:text-white rounded-lg hover:bg-arena-700/50 transition-all duration-200"
    >
      {children}
    </Link>
  )
}
