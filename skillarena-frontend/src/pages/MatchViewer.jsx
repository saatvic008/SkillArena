import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Chessboard } from 'react-chessboard'
import { Chess } from 'chess.js'
import { useFetch } from '../hooks/useFetch'
import { useWebSocket } from '../hooks/useWebSocket'
import EvalBar from '../components/EvalBar'

export default function MatchViewer() {
  const { matchId } = useParams()
  const { data: match, loading } = useFetch(`/matches/${matchId}`)
  const { moves: wsMoves, status, connect, disconnect } = useWebSocket(matchId)

  const [currentIndex, setCurrentIndex] = useState(-1)
  const [game] = useState(new Chess())
  const [boardPosition, setBoardPosition] = useState('start')
  const [evalScore, setEvalScore] = useState(0)

  const moves = match?.moves || []
  const activeMove = currentIndex >= 0 && currentIndex < moves.length ? moves[currentIndex] : null

  useEffect(() => {
    if (activeMove) {
      setBoardPosition(activeMove.fen_after)
      setEvalScore(activeMove.eval_score || 0)
    } else {
      setBoardPosition('start')
      setEvalScore(0)
    }
  }, [activeMove])

  // WebSocket replay: auto-advance
  useEffect(() => {
    if (wsMoves.length > 0) {
      const latestWsMove = wsMoves[wsMoves.length - 1]
      setBoardPosition(latestWsMove.fen_after)
      setEvalScore(latestWsMove.eval_score || 0)
    }
  }, [wsMoves])

  const goTo = (idx) => setCurrentIndex(idx)
  const goFirst = () => setCurrentIndex(-1)
  const goPrev = () => setCurrentIndex(Math.max(-1, currentIndex - 1))
  const goNext = () => setCurrentIndex(Math.min(moves.length - 1, currentIndex + 1))
  const goLast = () => setCurrentIndex(moves.length - 1)

  if (loading) {
    return <div className="glass-card p-12 text-center text-arena-500">Loading match...</div>
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Match Analysis</h1>
          <p className="text-arena-400 text-sm">
            vs {match?.opponent_username || 'Unknown'} •{' '}
            <span className={
              match?.result === 'win' ? 'text-arena-success' :
              match?.result === 'loss' ? 'text-arena-danger' : 'text-arena-warning'
            }>{match?.result?.toUpperCase()}</span>
            {match?.opening_name && ` • ${match.opening_name}`}
          </p>
        </div>
        <button
          onClick={status === 'disconnected' ? connect : disconnect}
          className={status === 'connected' ? 'btn-secondary' : 'btn-primary'}
          id="replay-btn"
        >
          {status === 'disconnected' && '▶ Replay'}
          {status === 'connecting' && '⏳ Connecting...'}
          {status === 'connected' && '⏹ Stop'}
          {status === 'ended' && '✅ Done'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Board + Eval */}
        <div className="lg:col-span-2 flex gap-3 justify-center">
          <EvalBar evalScore={evalScore} height={400} />
          <div className="w-[400px] h-[400px]">
            <Chessboard
              position={boardPosition}
              boardWidth={400}
              customBoardStyle={{
                borderRadius: '12px',
                boxShadow: '0 0 30px rgba(139, 92, 246, 0.2)',
              }}
              customDarkSquareStyle={{ backgroundColor: '#4c3b72' }}
              customLightSquareStyle={{ backgroundColor: '#e8dff5' }}
            />
          </div>
        </div>

        {/* Move List */}
        <div className="glass-card p-4 max-h-[440px] overflow-y-auto">
          <h3 className="text-sm font-semibold text-arena-300 mb-3 uppercase tracking-wider">Moves</h3>
          <div className="space-y-1">
            {moves.length === 0 && <p className="text-arena-500 text-sm">No moves available</p>}
            {moves.map((move, idx) => (
              <button
                key={idx}
                onClick={() => goTo(idx)}
                className={`w-full text-left px-3 py-1.5 rounded-lg text-sm font-mono transition-all duration-150 flex items-center gap-2
                  ${idx === currentIndex
                    ? 'bg-arena-accent/20 text-white border border-arena-accent/40'
                    : 'text-arena-400 hover:bg-arena-700/50 hover:text-white'
                  }
                  ${move.is_blunder ? 'border-l-2 border-l-arena-danger' : ''}
                  ${move.is_mistake ? 'border-l-2 border-l-arena-warning' : ''}
                `}
              >
                <span className="text-arena-500 w-8">{move.move_number}{move.color === 'w' ? '.' : '...'}</span>
                <span>{move.san}</span>
                {move.eval_score != null && (
                  <span className="ml-auto text-xs text-arena-500">
                    {move.eval_score > 0 ? '+' : ''}{move.eval_score.toFixed(1)}
                  </span>
                )}
                {move.is_blunder && <span className="text-arena-danger text-xs">??</span>}
                {move.is_mistake && !move.is_blunder && <span className="text-arena-warning text-xs">?</span>}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="flex justify-center gap-2">
        {['⏮', '◀', '▶', '⏭'].map((icon, i) => (
          <button
            key={i}
            onClick={[goFirst, goPrev, goNext, goLast][i]}
            className="w-12 h-12 glass-card flex items-center justify-center text-xl hover:bg-arena-700 transition-all"
          >
            {icon}
          </button>
        ))}
      </div>
    </div>
  )
}
