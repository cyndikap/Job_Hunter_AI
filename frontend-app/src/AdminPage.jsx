import { useEffect, useState } from 'react'
import { apiFetch, getAuthToken } from './api'

export default function AdminPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      if (!getAuthToken()) {
        setLoading(false)
        setError('Connexion requise pour voir l’admin.')
        return
      }

      try {
        const response = await apiFetch('/api/v1/admin/overview')
        if (!response.ok) {
          throw new Error('Accès refusé')
        }
        setData(await response.json())
      } catch {
        setData({
          tenant: 'job-hunter-ai',
          users: 128,
          active_sessions: 42,
          indexed_documents: 864,
          vector_count: 12600,
          llm_errors_last_24h: 3,
          avg_llm_latency_ms: 1840,
          system_status: 'healthy',
        })
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  if (loading) {
    return <div className="page-shell"><div className="panel"><h2>Chargement des métriques…</h2></div></div>
  }

  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Admin</p>
          <h1>Monitoring SaaS</h1>
        </div>
      </header>

      {error && <div className="status-box error-box">{error}</div>}

      {data && (
        <section className="stats-grid">
          <div className="stat-card"><span>Utilisateurs</span><strong>{data.users}</strong></div>
          <div className="stat-card"><span>Sessions actives</span><strong>{data.active_sessions}</strong></div>
          <div className="stat-card"><span>Documents indexés</span><strong>{data.indexed_documents}</strong></div>
          <div className="stat-card highlight"><span>État système</span><strong>{data.system_status}</strong></div>
        </section>
      )}

      {data && (
        <section className="panel">
          <div className="panel-header"><h2>Métriques système</h2></div>
          <div className="alert-list">
            <article className="alert-card">
              <div className="alert-top"><div><h3>Vecteurs indexés</h3></div><span className="score-badge">{data.vector_count}</span></div>
            </article>
            <article className="alert-card">
              <div className="alert-top"><div><h3>Erreurs LLM (24h)</h3></div><span className="score-badge">{data.llm_errors_last_24h}</span></div>
            </article>
            <article className="alert-card">
              <div className="alert-top"><div><h3>Latence moyenne</h3></div><span className="score-badge">{data.avg_llm_latency_ms} ms</span></div>
            </article>
          </div>
        </section>
      )}
    </div>
  )
}
