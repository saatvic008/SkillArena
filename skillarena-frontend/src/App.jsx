import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import MatchViewer from './pages/MatchViewer'
import WeaknessReport from './pages/WeaknessReport'
import Drills from './pages/Drills'
import Leaderboard from './pages/Leaderboard'

function ProtectedRoute({ children }) {
  const token = useAuthStore((s) => s.accessToken)
  if (!token) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-arena-900">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
            <Route path="/match/:matchId" element={<ProtectedRoute><MatchViewer /></ProtectedRoute>} />
            <Route path="/report" element={<ProtectedRoute><WeaknessReport /></ProtectedRoute>} />
            <Route path="/drills" element={<ProtectedRoute><Drills /></ProtectedRoute>} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
