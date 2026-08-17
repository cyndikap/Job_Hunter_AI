import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'
import { apiFetch, getAuthToken } from './api'

const COLORS = ['#60a5fa', '#34d399', '#fbbf24', '#f472b6', '#a78bfa']

export default function AiInsightsPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      if (!getAuthToken()) {
        setLoading(false)
        return
      }

      try {
        const response = await apiFetch('/api/v1/analytics/dashboard')
        const payload = await response.json()
        setData(payload)
      } catch {
        setData({
          career_score: 88,
          response_rate: 68,
          interview_rate: 32,
          hire_rate: 12,
          average_response_time_days: 4.3,
          most_reactive_company: 'Ippon Technologies',
          most_efficient_source: 'APEC',
          most_demanded_technology: 'Python',
          top_opportunities: [
            { title: 'AI Engineer', company: 'Ippon Technologies', score: 92, interview_probability: 85, hire_probability: 62, published_at: '2026-08-15' },
            { title: 'Data Engineer', company: 'Capgemini', score: 88, interview_probability: 81, hire_probability: 58, published_at: '2026-08-14' },
          ],
          missing_skills: ['Azure DevOps', 'Terraform', 'Spark Streaming', 'Data Governance'],
          notifications: [
            { id: 'n-1', type: 'new_offer', title: 'Nouvelle offre pertinente' },
            { id: 'n-2', type: 'follow_up', title: 'Relance recommandée' },
          ],
        })
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  if (loading) {
    return <div className="page-shell"><div className="panel"><h2>Chargement du dashboard IA…</h2></div></div>
  }

  if (!data) {
    return <div className="page-shell"><div className="panel"><h2>Connectez-vous pour accéder à l’AI Insights.</h2></div></div>
  }

  const chartData = [
    { name: 'Réponse', value: data.response_rate },
    { name: 'Entretien', value: data.interview_rate },
    { name: 'Embauche', value: data.hire_rate },
  ]

  const lineData = [
    { month: 'Jan', score: 64 },
    { month: 'Fév', score: 70 },
    { month: 'Mar', score: 77 },
    { month: 'Avr', score: 82 },
    { month: 'Mai', score: 88 },
    { month: 'Jui', score: data.career_score },
  ]

  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI Insights</p>
          <h1>Dashboard stratégique de recherche d’emploi</h1>
        </div>
      </header>

      <section className="stats-grid">
        <div className="stat-card highlight">
          <span>Career Score</span>
          <strong>{Math.round(data.career_score)}</strong>
        </div>
        <div className="stat-card">
          <span>Taux de réponse</span>
          <strong>{data.response_rate}%</strong>
        </div>
        <div className="stat-card">
          <span>Taux entretien</span>
          <strong>{data.interview_rate}%</strong>
        </div>
        <div className="stat-card">
          <span>Temps moyen</span>
          <strong>{data.average_response_time_days}j</strong>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header"><h2>Opportunités prioritaires</h2></div>
        <div className="opportunity-grid">
          {(data.top_opportunities || []).map((offer) => (
            <article key={`${offer.company}-${offer.title}`} className="alert-card">
              <div className="alert-top">
                <div>
                  <h3>{offer.title}</h3>
                  <p>{offer.company}</p>
                </div>
                <span className="score-badge">{offer.score}%</span>
              </div>
              <div className="alert-meta">
                <span>Entretien: {offer.interview_probability}%</span>
                <span>Embauche: {offer.hire_probability}%</span>
                <span>{offer.published_at}</span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel panel-lower">
        <div className="panel-header"><h2>Analytics</h2></div>
        <div className="chart-grid">
          <div className="chart-card">
            <h3>Performance</h3>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" />
                <Tooltip />
                <Bar dataKey="value" fill="#60a5fa" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Évolution Career Score</h3>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="month" stroke="#cbd5e1" />
                <YAxis stroke="#cbd5e1" />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#34d399" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Répartition</h3>
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie data={chartData} dataKey="value" nameKey="name" outerRadius={80} label>
                  {chartData.map((entry, index) => (
                    <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="panel panel-lower">
        <div className="panel-header"><h2>Compétences manquantes</h2></div>
        <div className="skills-row">
          {(data.missing_skills || []).map((skill) => (
            <span key={skill} className="skill-pill">{skill}</span>
          ))}
        </div>
      </section>

      <section className="panel panel-lower">
        <div className="panel-header"><h2>Notifications</h2></div>
        <div className="alert-list">
          {(data.notifications || []).map((notification) => (
            <article key={notification.id} className="alert-card">
              <div className="alert-top">
                <div>
                  <h3>{notification.title}</h3>
                </div>
                <span className="score-badge">{notification.type}</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
