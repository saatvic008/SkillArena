import { useState, useEffect } from 'react'
import client from '../api/client'

export default function Leaderboard() {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchBoard = async () => {
      try {
        const res = await client.get('/leaderboard?top=50')
        setEntries(res.data.entries || [])
      } catch {
        setEntries([])
      } finally {
        setLoading(false)
      }
    }
    fetchBoard()
  }, [])

  const rankBadge = (rank) => {
    if (rank === 1) return '🥇'
    if (rank === 2) return '🥈'
    if (rank === 3) return '🥉'
    return `#${rank}`
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Leaderboard</h1>
        <p className="text-arena-400">Top players ranked by ELO rating</p>
      </div>

      <div className="glass-card overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-arena-500">Loading leaderboard...</div>
        ) : entries.length === 0 ? (
          <div className="p-12 text-center text-arena-500">
            <p className="text-4xl mb-4">🏆</p>
            <p>No players on the leaderboard yet</p>
          </div>
        ) : (
          <table className="w-full" id="leaderboard-table">
            <thead>
              <tr className="border-b border-arena-700">
                <th className="px-6 py-4 text-left text-xs font-semibold text-arena-400 uppercase tracking-wider">Rank</th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-arena-400 uppercase tracking-wider">Player</th>
                <th className="px-6 py-4 text-right text-xs font-semibold text-arena-400 uppercase tracking-wider">ELO</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry) => (
                <tr
                  key={entry.rank}
                  className={`border-b border-arena-800/50 transition-colors hover:bg-arena-700/30
                    ${entry.rank <= 3 ? 'bg-arena-accent/5' : ''}`}
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-lg">{rankBadge(entry.rank)}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-medium text-white">{entry.username}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <span className="font-mono text-arena-accent font-semibold">{entry.elo_rating}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
