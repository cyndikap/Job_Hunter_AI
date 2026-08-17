import { useEffect, useState } from 'react'
import './App.css'
import { dashboardData } from './dashboardData'

function App() {
  const [summary, setSummary] = useState(null)
  const [applications, setApplications] = useState([])

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/dashboard/summary')
      .then((response) => response.json())
      .then((data) => {
        setSummary(data)
      })
      .catch(() => {
        setSummary(dashboardData)
      })

    fetch('http://localhost:8000/api/v1/applications/list')
      .then((response) => response.json())
      .then((data) => setApplications(data.applications))
      .catch(() => setApplications([
        { id: 1, date: '2026-08-15', company: 'Ippon Technologies', status: 'Email envoyé', score: 92, link: '#' },
        { id: 2, date: '2026-08-14', company: 'Capgemini', status: 'En attente', score: 88, link: '#' },
      ]))
  }, [])

  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Job Hunter AI</p>
          <h1>Veille emploi Data, IA & Cloud</h1>
        </div>
        <button className="primary-button">Lancer un scan</button>
      </header>

      {summary && (
        <section className="stats-grid">
          <div className="stat-card">
            <span>Jobs suivis</span>
            <strong>{summary.jobs_monitored}</strong>
          </div>
          <div className="stat-card highlight">
            <span>Très forte adéquation</span>
            <strong>{summary.high_match}</strong>
          </div>
          <div className="stat-card">
            <span>Adéquation moyenne</span>
            <strong>{summary.medium_match}</strong>
          </div>
          <div className="stat-card">
            <span>Dernier scan</span>
            <strong>{new Date(summary.last_scan).toLocaleDateString('fr-FR')}</strong>
          </div>
        </section>
      )}

      <section className="panel">
        <div className="panel-header">
          <h2>Alertes email</h2>
          <span>{summary?.alerts?.length ?? 0} notifications</span>
        </div>

        <div className="alert-list">
          {(summary?.alerts ?? []).map((alert) => (
            <article key={alert.id} className="alert-card">
              <div className="alert-top">
                <div>
                  <h3>{alert.title}</h3>
                  <p>{alert.company}</p>
                </div>
                <span className="score-badge">{alert.score}%</span>
              </div>

              <div className="alert-meta">
                <span>{alert.location ?? 'Paris / Remote'}</span>
                <span>{alert.status}</span>
                <span>{alert.date}</span>
              </div>

              <div className="skills-row">
                {(alert.skills ?? ['Azure', 'Python', 'LLM']).map((skill) => (
                  <span key={`${alert.id}-${skill}`} className="skill-pill">{skill}</span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel panel-lower">
        <div className="panel-header">
          <h2>Suivi chronologique</h2>
          <span>{applications.length} candidatures</span>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Entreprise</th>
                <th>Statut</th>
                <th>Score</th>
                <th>Lien</th>
              </tr>
            </thead>
            <tbody>
              {applications.map((application) => (
                <tr key={application.id}>
                  <td>{application.date}</td>
                  <td>{application.company}</td>
                  <td>{application.status}</td>
                  <td>{application.score}%</td>
                  <td><a href={application.link}>Voir</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

export default App
