import { BrowserRouter, Link, Navigate, Route, Routes } from 'react-router-dom'
import { useEffect, useState } from 'react'
import './App.css'
import AiInsightsPage from './AiInsightsPage'
import AdminPage from './AdminPage'
import { dashboardData } from './dashboardData'
import { apiFetch, getAuthToken, setAuthToken } from './api'

function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [applications, setApplications] = useState([])
  const [opportunities, setOpportunities] = useState([])
  const [scanStatus, setScanStatus] = useState('')
  const [isScanning, setIsScanning] = useState(false)
  const [isGeneratingLinkedIn, setIsGeneratingLinkedIn] = useState(false)
  const [linkedinMessage, setLinkedinMessage] = useState('')
  const [linkedinGeneratedAt, setLinkedinGeneratedAt] = useState('')
  const [linkedinError, setLinkedinError] = useState('')
  const [authToken, setAuthTokenState] = useState(getAuthToken())
  const [authEmail, setAuthEmail] = useState('')
  const [authPassword, setAuthPassword] = useState('')
  const [authError, setAuthError] = useState('')
  const [chatInput, setChatInput] = useState('')
  const [chatMessages, setChatMessages] = useState([])
  const [isSendingChat, setIsSendingChat] = useState(false)

  const refreshDashboard = async () => {
    try {
      const [summaryResponse, applicationsResponse, opportunitiesResponse] = await Promise.all([
        apiFetch('/api/v1/dashboard/summary'),
        apiFetch('/api/v1/applications/list'),
        apiFetch('/api/v1/jobs/sample'),
      ])

      const summaryData = await summaryResponse.json()
      const applicationsData = await applicationsResponse.json()
      const opportunitiesData = await opportunitiesResponse.json()

      setSummary(summaryData)
      setApplications(applicationsData.applications || [])
      setOpportunities(opportunitiesData.jobs || [])
    } catch {
      setSummary(dashboardData)
      setApplications([
        { id: 1, date: '2026-08-15', company: 'Ippon Technologies', status: 'Email envoyé', score: 92, link: 'http://localhost:3000/jobs/1' },
        { id: 2, date: '2026-08-14', company: 'Capgemini', status: 'En attente', score: 88, link: 'http://localhost:3000/jobs/2' },
      ])
      setOpportunities([
        {
          id: 1,
          title: 'AI Engineer',
          company: 'Ippon Technologies',
          match_score: 92,
          classification: 'Très forte adéquation',
          skills: ['Azure Databricks', 'LLM', 'RAG', 'MLflow', 'Python'],
          url: 'http://localhost:3000/jobs/1',
          date: '2026-08-15',
        },
        {
          id: 2,
          title: 'Data & AI Engineer',
          company: 'Capgemini',
          match_score: 88,
          classification: 'Forte adéquation',
          skills: ['Azure', 'Python', 'SQL', 'Data Governance', 'FastAPI'],
          url: 'http://localhost:3000/jobs/2',
          date: '2026-08-14',
        },
      ])
    }
  }

  const handleLogin = async (event) => {
    event.preventDefault()
    setAuthError('')

    try {
      const response = await fetch(`${window.location.origin.replace(/:\d+$/, '')}:8000/api/v1/auth/signin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: authEmail, password: authPassword }),
      })

      const data = await response.json()
      const token = data?.access_token || data?.token || data?.session?.access_token || data?.data?.access_token

      if (!response.ok || !token) {
        throw new Error(data?.detail || 'Identifiants invalides')
      }

      setAuthToken(token)
      setAuthTokenState(token)
      setAuthPassword('')
      setAuthError('')
    } catch (error) {
      setAuthError(error.message || 'Connexion impossible.')
    }
  }

  const loadChatHistory = async () => {
    if (!authToken) return

    try {
      const response = await apiFetch('/api/v1/chat/history')
      if (!response.ok) return

      const history = await response.json()
      const formatted = (Array.isArray(history) ? history : []).map((entry) => ({
        role: 'assistant',
        content: entry.answer,
        provider: entry.provider,
      }))

      setChatMessages(formatted)
    } catch {
      setChatMessages([])
    }
  }

  const handleLogout = () => {
    setAuthToken('')
    setAuthTokenState('')
    setChatMessages([])
  }

  const handleScan = async () => {
    setIsScanning(true)
    setScanStatus('Scan en cours...')

    try {
      const response = await apiFetch('/api/v1/jobs/scan', { method: 'POST' })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data?.detail || 'Erreur lors du scan')
      }

      setScanStatus(data.message || 'Scan déclenché avec succès.')
      await refreshDashboard()
    } catch (error) {
      setScanStatus(error.message || 'Le scan a échoué.')
    } finally {
      setIsScanning(false)
    }
  }

  const handleGenerateLinkedInMessage = async () => {
    setIsGeneratingLinkedIn(true)
    setLinkedinError('')

    try {
      const selectedAlert = summary?.alerts?.[0]
      const firstOpportunity = opportunities[0]
      const payload = {
        title: selectedAlert?.title || firstOpportunity?.title || 'AI Engineer',
        company: selectedAlert?.company || firstOpportunity?.company || 'Ippon Technologies',
        location: selectedAlert?.location || firstOpportunity?.location || 'Paris / Remote',
        match_score: selectedAlert?.score || firstOpportunity?.match_score || 92,
        skills: selectedAlert?.skills || firstOpportunity?.skills || ['Azure Databricks', 'LLM', 'RAG', 'Python'],
        url: firstOpportunity?.url || selectedAlert?.url || 'https://www.ippon.fr/rejoignez-nous/',
      }

      const response = await apiFetch('/api/v1/alerts/linkedin', {
        method: 'POST',
        body: JSON.stringify(payload),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data?.detail || 'Erreur lors de la génération du message LinkedIn')
      }

      const generatedMessage = data.message || data?.generated_message || ''
      if (!generatedMessage) {
        setLinkedinMessage('')
        setLinkedinGeneratedAt('')
        setLinkedinError('Aucun message LinkedIn généré pour le moment.')
        return
      }

      setLinkedinMessage(generatedMessage)
      setLinkedinGeneratedAt(new Date().toISOString())
      setLinkedinError('')
    } catch (error) {
      setLinkedinError(error.message || 'La génération du message a échoué.')
      setLinkedinMessage('')
      setLinkedinGeneratedAt('')
    } finally {
      setIsGeneratingLinkedIn(false)
    }
  }

  const handleCopyLinkedInMessage = async () => {
    if (!linkedinMessage) return

    try {
      await navigator.clipboard.writeText(linkedinMessage)
      setLinkedinError('Message LinkedIn copié dans le presse-papiers.')
    } catch {
      setLinkedinError('Impossible de copier automatiquement. Sélectionnez le message manuellement.')
    }
  }

  const handleSendChat = async () => {
    if (!chatInput.trim() || !authToken) return

    const userMessage = { role: 'user', content: chatInput.trim() }
    setChatMessages((current) => [...current, userMessage])
    setChatInput('')
    setIsSendingChat(true)

    try {
      const response = await apiFetch('/api/v1/chat', {
        method: 'POST',
        body: JSON.stringify({ message: userMessage.content }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data?.detail || 'Erreur lors du chat IA')
      }

      const assistantMessage = {
        role: 'assistant',
        content: data.answer || 'Aucune réponse disponible.',
        provider: data.provider,
      }

      setChatMessages((current) => [...current, assistantMessage])
    } catch (error) {
      setChatMessages((current) => [
        ...current,
        { role: 'assistant', content: `Erreur: ${error.message || 'Chat IA indisponible.'}` },
      ])
    } finally {
      setIsSendingChat(false)
    }
  }

  useEffect(() => {
    refreshDashboard()
  }, [])

  useEffect(() => {
    if (authToken) {
      loadChatHistory()
    }
  }, [authToken])

  return (
    <div className="page-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Job Hunter AI</p>
          <h1>Veille emploi Data, IA & Cloud</h1>
        </div>
        <div className="topbar-actions">
          {authToken ? (
            <button className="secondary-button" onClick={handleLogout}>Déconnexion</button>
          ) : null}
          <button className="secondary-button" onClick={handleGenerateLinkedInMessage} disabled={isGeneratingLinkedIn}>
            {isGeneratingLinkedIn ? 'Génération...' : '📨 Générer un message LinkedIn'}
          </button>
          <button className="primary-button" onClick={handleScan} disabled={isScanning}>
            {isScanning ? 'Scan en cours...' : 'Lancer un scan'}
          </button>
        </div>
      </header>

      {scanStatus && (
        <div className="panel" style={{ marginBottom: '1rem', padding: '0.75rem 1rem' }}>
          <strong>{scanStatus}</strong>
        </div>
      )}

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

      {!authToken ? (
        <section className="panel auth-panel">
          <div className="panel-header">
            <h2>Connexion assistant IA</h2>
          </div>
          <form className="auth-form" onSubmit={handleLogin}>
            <label>
              Email
              <input type="email" value={authEmail} onChange={(event) => setAuthEmail(event.target.value)} placeholder="john@company.com" required />
            </label>
            <label>
              Mot de passe
              <input type="password" value={authPassword} onChange={(event) => setAuthPassword(event.target.value)} placeholder="••••••••" required />
            </label>
            {authError && <div className="status-box error-box">{authError}</div>}
            <button className="primary-button" type="submit">Se connecter</button>
          </form>
        </section>
      ) : (
        <section className="panel chat-panel">
          <div className="panel-header">
            <h2>Assistant IA</h2>
            <span>{chatMessages.length} messages</span>
          </div>

          <div className="chat-thread">
            {chatMessages.length === 0 ? (
              <div className="status-box">Démarrez une conversation avec votre assistant Job Hunter AI.</div>
            ) : (
              chatMessages.map((message, index) => (
                <div key={`${message.role}-${index}`} className={`chat-bubble ${message.role}`}>
                  <div className="bubble-role">{message.role === 'user' ? 'Vous' : 'Assistant'}</div>
                  <p>{message.content}</p>
                  {message.provider && <small>Provider: {message.provider}</small>}
                </div>
              ))
            )}
          </div>

          <div className="chat-composer">
            <textarea
              rows="3"
              value={chatInput}
              onChange={(event) => setChatInput(event.target.value)}
              placeholder="Posez une question sur votre profil, vos candidatures ou les offres qui correspondent le mieux..."
            />
            <button className="primary-button" onClick={handleSendChat} disabled={isSendingChat || !chatInput.trim()}>
              {isSendingChat ? 'Envoi...' : 'Envoyer'}
            </button>
          </div>
        </section>
      )}

      <section className="panel">
        <div className="panel-header">
          <h2>LinkedIn Outreach</h2>
          <button className="secondary-button" onClick={handleGenerateLinkedInMessage} disabled={isGeneratingLinkedIn}>
            {isGeneratingLinkedIn ? 'Génération...' : 'Régénérer'}
          </button>
        </div>

        {linkedinError && <div className="status-box error-box">{linkedinError}</div>}

        {isGeneratingLinkedIn ? (
          <div className="status-box">Génération du message LinkedIn en cours...</div>
        ) : linkedinMessage ? (
          <div className="linkedin-box">
            <p>{linkedinMessage}</p>
            {linkedinGeneratedAt && (
              <div className="linkedin-meta">
                <span>Généré le {new Date(linkedinGeneratedAt).toLocaleString('fr-FR')}</span>
              </div>
            )}
            <div className="linkedin-actions">
              <button className="secondary-button" onClick={handleCopyLinkedInMessage}>Copier</button>
              <button className="secondary-button" onClick={handleGenerateLinkedInMessage}>Régénérer</button>
            </div>
          </div>
        ) : (
          <div className="status-box">Aucun message LinkedIn généré pour le moment.</div>
        )}
      </section>

      <section className="panel panel-lower">
        <div className="panel-header">
          <h2>🎯 Opportunités détectées</h2>
          <span>{opportunities.length} postes</span>
        </div>

        <div className="job-list">
          {opportunities.map((opportunity) => (
            <article key={opportunity.id} className="alert-card">
              <div className="alert-top">
                <div>
                  <h3>{opportunity.title}</h3>
                  <p>{opportunity.company}</p>
                </div>
                <span className={`score-badge ${opportunity.match_score >= 90 ? 'excellent' : opportunity.match_score >= 85 ? 'good' : 'review'}`}>
                  {opportunity.match_score}%
                </span>
              </div>

              <div className="alert-meta">
                <span>{opportunity.classification}</span>
                <span>{opportunity.date || '2026-08-15'}</span>
              </div>

              <div className="skills-row">
                {(opportunity.skills ?? []).map((skill) => (
                  <span key={`${opportunity.id}-${skill}`} className="skill-pill">{skill}</span>
                ))}
              </div>

              <div className="opportunity-footer">
                <a href={opportunity.url || '#'} target="_blank" rel="noopener noreferrer" aria-label={`Voir l’offre ${opportunity.title} chez ${opportunity.company}`} data-testid={`opportunity-link-${opportunity.id}`}>
                  Voir l’offre
                </a>
              </div>
            </article>
          ))}
        </div>
      </section>

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

function AppShell() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <nav className="main-nav">
          <Link to="/" className="nav-link">Dashboard</Link>
          <Link to="/ai-insights" className="nav-link">AI Insights</Link>
          <Link to="/admin" className="nav-link">Admin</Link>
        </nav>

        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/ai-insights" element={<AiInsightsPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default function App() {
  return <AppShell />
}
