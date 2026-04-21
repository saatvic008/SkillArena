import { Link } from 'react-router-dom'

export default function MatchCard({ match }) {
  const resultColors = {
    win: 'text-arena-success',
    loss: 'text-arena-danger',
    draw: 'text-arena-warning',
  }

  return (
    <Link to={`/match/${match.id}`} className="block glass-card-hover p-5 animate-slide-up">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className={`text-sm font-bold uppercase ${resultColors[match.result]}`}>
            {match.result}
          </span>
          <span className="text-xs text-arena-500">vs {match.opponent_username || 'Unknown'}</span>
        </div>
        <span className="stat-badge">{match.source}</span>
      </div>

      <div className="flex items-center gap-4 text-sm text-arena-400">
        {match.opening_name && (
          <span className="truncate max-w-[200px]">🎯 {match.opening_name}</span>
        )}
        {match.time_control && <span>⏱ {match.time_control}</span>}
      </div>

      <p className="text-xs text-arena-600 mt-2">
        {new Date(match.played_at).toLocaleDateString('en-US', {
          year: 'numeric', month: 'short', day: 'numeric',
        })}
      </p>
    </Link>
  )
}
