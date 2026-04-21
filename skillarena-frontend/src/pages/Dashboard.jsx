import { useState, useRef } from 'react'
import { useFetch } from '../hooks/useFetch'
import StatsCard from '../components/StatsCard'
import MatchCard from '../components/MatchCard'
import client from '../api/client'

export default function Dashboard() {
  const { data: matchData, loading, refetch } = useFetch('/matches?limit=10')
  const [uploading, setUploading] = useState(false)
  const [fetchingLichess, setFetchingLichess] = useState(false)
  const [lichessUser, setLichessUser] = useState('')
  const [importMsg, setImportMsg] = useState('')
  const fileRef = useRef()

  const matches = matchData?.matches || []
  const total = matchData?.total || 0
  const wins = matches.filter((m) => m.result === 'win').length
  const losses = matches.filter((m) => m.result === 'loss').length

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setUploading(true)
    setImportMsg('')
    try {
      const form = new FormData()
      form.append('file', file)
      await client.post('/matches/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setImportMsg('Games imported successfully!')
      refetch()
    } catch (err) {
      setImportMsg(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  const handleLichessFetch = async () => {
    if (!lichessUser.trim()) return
    setFetchingLichess(true)
    setImportMsg('')
    try {
      await client.post('/matches/fetch/lichess', {
        lichess_username: lichessUser,
        max_games: 20,
      })
      setImportMsg('Lichess games imported!')
      setLichessUser('')
      refetch()
    } catch (err) {
      setImportMsg(err.response?.data?.detail || 'Fetch failed')
    } finally {
      setFetchingLichess(false)
    }
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-arena-400">Your chess performance at a glance</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard label="Total Games" value={total} icon="♟" />
        <StatsCard label="Wins" value={wins} icon="🏆" color="green-500" />
        <StatsCard label="Losses" value={losses} icon="💀" color="red-500" />
        <StatsCard
          label="Win Rate"
          value={total > 0 ? `${Math.round((wins / total) * 100)}%` : '—'}
          icon="📊"
        />
      </div>

      {/* Import Section */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Import Games</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-arena-400 mb-2">Upload PGN/JSON file</p>
            <input
              ref={fileRef}
              type="file"
              accept=".pgn,.json"
              onChange={handleUpload}
              className="hidden"
              id="pgn-upload"
            />
            <button
              onClick={() => fileRef.current?.click()}
              disabled={uploading}
              className="btn-secondary w-full"
              id="upload-btn"
            >
              {uploading ? 'Uploading...' : '📁 Choose File'}
            </button>
          </div>

          <div>
            <p className="text-sm text-arena-400 mb-2">Fetch from Lichess</p>
            <div className="flex gap-2">
              <input
                type="text"
                value={lichessUser}
                onChange={(e) => setLichessUser(e.target.value)}
                placeholder="Lichess username"
                className="input-field flex-1"
                id="lichess-username"
              />
              <button
                onClick={handleLichessFetch}
                disabled={fetchingLichess}
                className="btn-primary whitespace-nowrap"
                id="lichess-fetch-btn"
              >
                {fetchingLichess ? '...' : 'Fetch'}
              </button>
            </div>
          </div>
        </div>
        {importMsg && (
          <p className="mt-3 text-sm text-arena-accent">{importMsg}</p>
        )}
      </div>

      {/* Recent Matches */}
      <div>
        <h2 className="text-lg font-semibold text-white mb-4">Recent Matches</h2>
        {loading ? (
          <div className="glass-card p-12 text-center text-arena-500">Loading matches...</div>
        ) : matches.length === 0 ? (
          <div className="glass-card p-12 text-center text-arena-500">
            <p className="text-4xl mb-4">♟</p>
            <p>No games yet. Import some games to get started!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {matches.map((m) => (
              <MatchCard key={m.id} match={m} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
