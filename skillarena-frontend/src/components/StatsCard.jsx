export default function StatsCard({ label, value, icon, color = 'arena-accent', subtext }) {
  return (
    <div className="glass-card-hover p-6 animate-fade-in">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-arena-400 font-medium mb-1">{label}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
          {subtext && <p className="text-xs text-arena-500 mt-1">{subtext}</p>}
        </div>
        <div className={`w-12 h-12 rounded-xl bg-${color}/10 flex items-center justify-center text-2xl`}>
          {icon}
        </div>
      </div>
    </div>
  )
}
