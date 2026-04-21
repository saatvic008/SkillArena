export default function EvalBar({ evalScore, height = 300 }) {
  // evalScore in centipawns, clamped to [-10, 10]
  const clamped = Math.max(-10, Math.min(10, evalScore || 0))
  const whitePercent = ((clamped + 10) / 20) * 100

  return (
    <div className="w-6 rounded-lg overflow-hidden border border-arena-700" style={{ height }}>
      <div
        className="w-full bg-slate-800 transition-all duration-500 ease-out"
        style={{ height: `${100 - whitePercent}%` }}
      />
      <div
        className="w-full bg-slate-200 transition-all duration-500 ease-out"
        style={{ height: `${whitePercent}%` }}
      />
    </div>
  )
}
