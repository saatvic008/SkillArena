import { useFetch } from '../hooks/useFetch'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js'
import { Radar, Bar } from 'react-chartjs-2'

ChartJS.register(
  RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend,
  CategoryScale, LinearScale, BarElement
)

export default function WeaknessReport() {
  const { data: matchData } = useFetch('/matches?limit=5')
  const matchId = matchData?.matches?.[0]?.id
  const { data: report, loading, error } = useFetch(
    matchId ? `/analysis/${matchId}/report` : null
  )

  // Demo data when no report is available
  const demoScores = {
    tactical: 65, accuracy: 45, eval_control: 55,
    opening: 30, endgame: 70, time_pressure: 80,
  }
  const scores = report?.scores || demoScores
  const isDemo = !report

  const radarData = {
    labels: ['Tactical', 'Accuracy', 'Eval Control', 'Opening', 'Endgame', 'Time Pressure'],
    datasets: [{
      label: 'Weakness Score',
      data: [
        scores.tactical || 0, scores.accuracy || 0, scores.eval_control || 0,
        scores.opening || 0, scores.endgame || 0, scores.time_pressure || 0,
      ],
      backgroundColor: 'rgba(139, 92, 246, 0.2)',
      borderColor: 'rgba(139, 92, 246, 1)',
      borderWidth: 2,
      pointBackgroundColor: 'rgba(139, 92, 246, 1)',
      pointBorderColor: '#fff',
      pointHoverRadius: 6,
    }],
  }

  const radarOptions = {
    scales: {
      r: {
        beginAtZero: true,
        max: 100,
        ticks: { color: '#7c5cbf', backdropColor: 'transparent', stepSize: 25 },
        grid: { color: 'rgba(124, 92, 191, 0.2)' },
        pointLabels: { color: '#b8a3e8', font: { size: 12 } },
      },
    },
    plugins: { legend: { display: false } },
  }

  const barData = {
    labels: ['Tactical', 'Opening', 'Endgame', 'Time Mgmt', 'Accuracy', 'Eval'],
    datasets: [{
      label: 'Weakness Areas',
      data: [
        scores.tactical || 0, scores.opening || 0, scores.endgame || 0,
        scores.time_pressure || 0, scores.accuracy || 0, scores.eval_control || 0,
      ],
      backgroundColor: [
        'rgba(248, 113, 113, 0.7)', 'rgba(251, 191, 36, 0.7)',
        'rgba(52, 211, 153, 0.7)', 'rgba(139, 92, 246, 0.7)',
        'rgba(96, 165, 250, 0.7)', 'rgba(244, 114, 182, 0.7)',
      ],
      borderRadius: 8,
    }],
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Weakness Report</h1>
        <p className="text-arena-400">
          {isDemo ? 'Demo analysis — play games to see your real data' : 'AI-powered analysis of your play'}
        </p>
      </div>

      {isDemo && (
        <div className="glass-card p-4 border-arena-warning/30 bg-arena-warning/5">
          <p className="text-arena-warning text-sm">
            ⚠️ Showing sample data. Import games and request analysis to see your actual weakness report.
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Radar Chart */}
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Weakness Profile</h2>
          <div className="aspect-square max-w-md mx-auto">
            <Radar data={radarData} options={radarOptions} />
          </div>
        </div>

        {/* Bar Chart */}
        <div className="glass-card p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Area Breakdown</h2>
          <Bar
            data={barData}
            options={{
              indexAxis: 'y',
              scales: {
                x: { max: 100, grid: { color: 'rgba(124, 92, 191, 0.1)' }, ticks: { color: '#7c5cbf' } },
                y: { grid: { display: false }, ticks: { color: '#b8a3e8' } },
              },
              plugins: { legend: { display: false } },
            }}
          />
        </div>
      </div>

      {/* Recommendations */}
      <div className="glass-card p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Recommended Drills</h2>
        {report?.recommendations?.length > 0 ? (
          <div className="space-y-3">
            {report.recommendations.map((rec, i) => (
              <div key={i} className="flex items-center gap-4 p-4 bg-arena-900/50 rounded-xl border border-arena-700/50">
                <span className="w-8 h-8 rounded-lg bg-arena-accent/20 flex items-center justify-center text-arena-accent font-bold text-sm">
                  #{rec.priority}
                </span>
                <div>
                  <p className="text-white text-sm font-medium">{rec.reason}</p>
                  <p className="text-arena-500 text-xs">Drill ID: {rec.drill_id}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-arena-500">
            <p>Complete an analysis to receive personalized drill recommendations</p>
          </div>
        )}
      </div>
    </div>
  )
}
