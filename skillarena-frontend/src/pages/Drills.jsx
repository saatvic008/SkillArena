import { useState } from 'react'
import { Chessboard } from 'react-chessboard'
import { useFetch } from '../hooks/useFetch'
import client from '../api/client'

export default function Drills() {
  const [category, setCategory] = useState('')
  const params = category ? `?category=${category}` : ''
  const { data: drills, loading } = useFetch(`/drills${params}`)
  const [activeDrill, setActiveDrill] = useState(null)
  const [userMove, setUserMove] = useState('')
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const categories = [
    { value: '', label: 'All' },
    { value: 'tactic', label: '⚔️ Tactics' },
    { value: 'endgame', label: '♔ Endgame' },
    { value: 'opening', label: '📖 Opening' },
  ]

  const handleAttempt = async () => {
    if (!activeDrill || !userMove.trim()) return
    setSubmitting(true)
    try {
      const res = await client.post(`/drills/${activeDrill.id}/attempt`, {
        player_move: userMove,
        time_taken_ms: 5000,
      })
      setResult(res.data)
    } catch (err) {
      setResult({ error: err.response?.data?.detail || 'Failed' })
    } finally {
      setSubmitting(false)
    }
  }

  const difficultyStars = (d) => '★'.repeat(d) + '☆'.repeat(5 - d)

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Training Drills</h1>
        <p className="text-arena-400">Practice targeted positions to improve your weaknesses</p>
      </div>

      {/* Category Filter */}
      <div className="flex gap-2 flex-wrap">
        {categories.map((cat) => (
          <button
            key={cat.value}
            onClick={() => { setCategory(cat.value); setActiveDrill(null); setResult(null) }}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200
              ${category === cat.value
                ? 'bg-arena-accent text-white shadow-glow'
                : 'bg-arena-800 text-arena-400 hover:bg-arena-700 border border-arena-700'
              }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Drill List */}
        <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
          {loading && <div className="glass-card p-8 text-center text-arena-500">Loading drills...</div>}
          {drills?.map((drill) => (
            <button
              key={drill.id}
              onClick={() => { setActiveDrill(drill); setResult(null); setUserMove('') }}
              className={`w-full text-left p-4 rounded-xl transition-all duration-200
                ${activeDrill?.id === drill.id
                  ? 'glass-card border-arena-accent/50 shadow-glow'
                  : 'glass-card-hover'
                }`}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-white text-sm">{drill.title}</h3>
                <span className="stat-badge text-xs">{drill.category}</span>
              </div>
              <p className="text-xs text-arena-500 mb-1">{drill.description}</p>
              <span className="text-arena-accent text-xs">{difficultyStars(drill.difficulty)}</span>
            </button>
          ))}
        </div>

        {/* Active Drill Board */}
        <div>
          {activeDrill ? (
            <div className="glass-card p-6 space-y-4">
              <h3 className="text-lg font-semibold text-white">{activeDrill.title}</h3>
              <div className="flex justify-center">
                <Chessboard
                  position={activeDrill.fen_position}
                  boardWidth={350}
                  customBoardStyle={{ borderRadius: '12px', boxShadow: '0 0 30px rgba(139, 92, 246, 0.2)' }}
                  customDarkSquareStyle={{ backgroundColor: '#4c3b72' }}
                  customLightSquareStyle={{ backgroundColor: '#e8dff5' }}
                />
              </div>
              <div className="space-y-3">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={userMove}
                    onChange={(e) => setUserMove(e.target.value)}
                    placeholder="Enter your move (e.g. Nf3, e4)"
                    className="input-field flex-1"
                    id="drill-move-input"
                    onKeyDown={(e) => e.key === 'Enter' && handleAttempt()}
                  />
                  <button
                    onClick={handleAttempt}
                    disabled={submitting}
                    className="btn-primary"
                    id="drill-submit"
                  >
                    {submitting ? '...' : 'Submit'}
                  </button>
                </div>

                {result && !result.error && (
                  <div className={`p-4 rounded-xl ${result.is_correct
                    ? 'bg-arena-success/10 border border-arena-success/30'
                    : 'bg-arena-danger/10 border border-arena-danger/30'
                  }`}>
                    <p className={`font-semibold ${result.is_correct ? 'text-arena-success' : 'text-arena-danger'}`}>
                      {result.is_correct ? '✅ Correct!' : '❌ Incorrect'}
                    </p>
                    {!result.is_correct && (
                      <>
                        <p className="text-sm text-arena-400 mt-1">Correct move: <span className="font-mono text-white">{result.correct_move}</span></p>
                        {result.explanation && <p className="text-xs text-arena-500 mt-1">{result.explanation}</p>}
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="glass-card p-12 text-center text-arena-500">
              <p className="text-4xl mb-4">♞</p>
              <p>Select a drill to start training</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
