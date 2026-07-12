import { type FormEvent, useEffect, useState } from 'react'
import './App.css'

type SummaryCard = {
  label: string
  value: string
  delta: string
  tone: string
}

type KPI = {
  name: string
  value: number
  target: number
}

type LeaderboardEntry = {
  name: string
  score: number
}

type DashboardData = {
  summary: SummaryCard[]
  kpis: KPI[]
  initiatives: string[]
  leaderboard: LeaderboardEntry[]
}

type CarbonLog = {
  id: number
  source: string
  amount: number
  unit: string
  date: string
}

type CSRActivity = {
  id: number
  title: string
  description: string | null
  location: string
  organizer: string
}

type Policy = {
  id: number
  title: string
  description: string | null
  version: string
  status: string
}

type User = {
  id: number
  name: string
  email: string
  role: string
  department: string | null
}

type View = 'dashboard' | 'carbon' | 'csr' | 'governance'

type AuthState = {
  isAuthenticated: boolean
  token: string | null
  user: User | null
  error: string
}

const fallbackData: DashboardData = {
  summary: [
    { label: 'Overall ESG Score', value: '84/100', delta: '+6%', tone: 'positive' },
    { label: 'Carbon Emissions', value: '12.4 tCO₂e', delta: '-8%', tone: 'positive' },
    { label: 'CSR Participation', value: '78%', delta: '+12%', tone: 'positive' },
    { label: 'Governance Status', value: 'Compliant', delta: 'On track', tone: 'neutral' },
  ],
  kpis: [
    { name: 'Energy Efficiency', value: 82, target: 90 },
    { name: 'Volunteer Hours', value: 71, target: 85 },
    { name: 'Policy Acknowledgement', value: 96, target: 100 },
  ],
  initiatives: [
    'Install rooftop solar panels across two sites',
    'Launch a city cleanup challenge for regional teams',
    'Automate compliance reminders for policy renewals',
  ],
  leaderboard: [
    { name: 'Operations', score: 92 },
    { name: 'People & Culture', score: 88 },
    { name: 'Supply Chain', score: 81 },
  ],
}

function App() {
  const [view, setView] = useState<View>('dashboard')
  const [dashboard, setDashboard] = useState<DashboardData>(fallbackData)
  const [carbonLogs, setCarbonLogs] = useState<CarbonLog[]>([])
  const [csrActivities, setCsrActivities] = useState<CSRActivity[]>([])
  const [policies, setPolicies] = useState<Policy[]>([])
  const [prompt, setPrompt] = useState('How can we improve our ESG score?')
  const [reply, setReply] = useState('AI suggestions will appear here as soon as the backend responds.')
  const [isLoading, setIsLoading] = useState(false)
  const [auth, setAuth] = useState<AuthState>({ isAuthenticated: false, token: null, user: null, error: '' })
  const [loginForm, setLoginForm] = useState({ email: 'ava@ecosphere.ai', password: 'demo123' })
  const [carbonForm, setCarbonForm] = useState({ source: 'Electricity', amount: '320', unit: 'kWh', date: '2026-06-01' })
  const [csrForm, setCsrForm] = useState({ title: 'Community Tree Planting', description: 'Planting trees with local volunteers', location: 'Abuja', organizer: 'Operations' })
  const [policyForm, setPolicyForm] = useState({ title: 'Governance Charter', description: 'Updated compliance policy', version: 'v1.4', status: 'active' })

  useEffect(() => {
    void loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/dashboard')
      if (response.ok) {
        const data = (await response.json()) as DashboardData
        setDashboard(data)
      }
    } catch {
      setDashboard(fallbackData)
    }
  }

  const loadModuleData = async () => {
    try {
      const [carbonResponse, csrResponse, policyResponse] = await Promise.all([
        fetch('http://127.0.0.1:8000/api/carbon/analytics'),
        fetch('http://127.0.0.1:8000/api/csr/activities'),
        fetch('http://127.0.0.1:8000/api/governance/policies'),
      ])

      if (carbonResponse.ok) {
        const carbonData = await carbonResponse.json()
        setCarbonLogs(carbonData.logs ?? [])
      }

      if (csrResponse.ok) {
        const csrData = await csrResponse.json()
        setCsrActivities(csrData ?? [])
      }

      if (policyResponse.ok) {
        const policyData = await policyResponse.json()
        setPolicies(policyData ?? [])
      }
    } catch {
      setAuth((current) => ({ ...current, error: 'Unable to load module data right now.' }))
    }
  }

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault()
    setAuth((current) => ({ ...current, error: '' }))

    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginForm),
      })

      if (!response.ok) {
        throw new Error('Invalid credentials')
      }

      const data = await response.json()
      setAuth({ isAuthenticated: true, token: data.access_token, user: data.user, error: '' })
      void loadModuleData()
    } catch {
      setAuth((current) => ({ ...current, error: 'Login failed. Please try the demo credentials.' }))
    }
  }

  const handleLogout = () => {
    setAuth({ isAuthenticated: false, token: null, user: null, error: '' })
    setView('dashboard')
  }

  const askCopilot = async (event: FormEvent) => {
    event.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/ai/copilot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      })

      if (response.ok) {
        const data = await response.json()
        setReply(data.reply)
      }
    } catch {
      setReply('The API is currently unavailable, so the demo response is being shown instead.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCarbonSubmit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:8000/api/carbon/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...carbonForm, amount: Number(carbonForm.amount) }),
      })

      if (response.ok) {
        void loadModuleData()
      }
    } catch {
      setAuth((current) => ({ ...current, error: 'Carbon log could not be saved.' }))
    }
  }

  const handleCSRSubmit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:8000/api/csr/activity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(csrForm),
      })

      if (response.ok) {
        void loadModuleData()
      }
    } catch {
      setAuth((current) => ({ ...current, error: 'CSR activity could not be saved.' }))
    }
  }

  const handlePolicySubmit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:8000/api/governance/policy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(policyForm),
      })

      if (response.ok) {
        void loadModuleData()
      }
    } catch {
      setAuth((current) => ({ ...current, error: 'Policy could not be saved.' }))
    }
  }

  return (
    <div className="app-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">EcoSphere AI</p>
          <h1>Turn ESG reporting into a live operating system.</h1>
          <p className="hero-copy">
            Track carbon, manage CSR, automate compliance, and surface AI-ready recommendations from one place.
          </p>
        </div>
        <div className="hero-panel">
          <span className="chip">Live dashboard</span>
          <span className="chip">AI copilots</span>
          <span className="chip">Predictive insights</span>
        </div>
      </header>

      <section className="toolbar panel">
        <div>
          <strong>{auth.user ? `Welcome back, ${auth.user.name}` : 'Demo mode'}</strong>
          <p>{auth.user ? auth.user.role : 'Use ava@ecosphere.ai / demo123 to sign in.'}</p>
        </div>
        {!auth.isAuthenticated ? (
          <button className="secondary-btn" onClick={() => setView('dashboard')}>Continue as demo</button>
        ) : (
          <button className="secondary-btn" onClick={handleLogout}>Log out</button>
        )}
      </section>

      {!auth.isAuthenticated ? (
        <section className="panel login-panel">
          <div className="panel-header">
            <h3>Sign in</h3>
            <span>Access your ESG workspace</span>
          </div>
          <form className="stack-form" onSubmit={handleLogin}>
            <input value={loginForm.email} onChange={(event) => setLoginForm({ ...loginForm, email: event.target.value })} placeholder="Email" />
            <input type="password" value={loginForm.password} onChange={(event) => setLoginForm({ ...loginForm, password: event.target.value })} placeholder="Password" />
            <button type="submit">Sign in</button>
          </form>
          {auth.error ? <p className="error-text">{auth.error}</p> : null}
        </section>
      ) : null}

      <nav className="nav-tabs">
        <button className={view === 'dashboard' ? 'active' : ''} onClick={() => setView('dashboard')}>Dashboard</button>
        <button className={view === 'carbon' ? 'active' : ''} onClick={() => setView('carbon')}>Carbon</button>
        <button className={view === 'csr' ? 'active' : ''} onClick={() => setView('csr')}>CSR</button>
        <button className={view === 'governance' ? 'active' : ''} onClick={() => setView('governance')}>Governance</button>
      </nav>

      {view === 'dashboard' ? (
        <>
          <section className="summary-grid">
            {dashboard.summary.map((card) => (
              <article className="summary-card" key={card.label}>
                <p>{card.label}</p>
                <h2>{card.value}</h2>
                <span className={`delta ${card.tone}`}>{card.delta}</span>
              </article>
            ))}
          </section>

          <section className="content-grid">
            <div className="panel">
              <div className="panel-header">
                <h3>Performance snapshot</h3>
                <span>Quarterly goal tracking</span>
              </div>
              <div className="kpi-list">
                {dashboard.kpis.map((kpi) => {
                  const percentage = Math.round((kpi.value / kpi.target) * 100)
                  return (
                    <div className="kpi-item" key={kpi.name}>
                      <div className="kpi-row">
                        <strong>{kpi.name}</strong>
                        <span>{kpi.value}% / {kpi.target}%</span>
                      </div>
                      <div className="bar-track">
                        <div className="bar-fill" style={{ width: `${Math.min(percentage, 100)}%` }} />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            <div className="panel">
              <div className="panel-header">
                <h3>Priority initiatives</h3>
                <span>Recommended next steps</span>
              </div>
              <ul className="initiative-list">
                {dashboard.initiatives.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </section>

          <section className="content-grid">
            <div className="panel">
              <div className="panel-header">
                <h3>Department leaderboard</h3>
                <span>Momentum by team</span>
              </div>
              <ul className="leaderboard-list">
                {dashboard.leaderboard.map((entry) => (
                  <li key={entry.name}>
                    <span>{entry.name}</span>
                    <strong>{entry.score}/100</strong>
                  </li>
                ))}
              </ul>
            </div>

            <div className="panel">
              <div className="panel-header">
                <h3>AI Copilot</h3>
                <span>Ask a question in plain English</span>
              </div>
              <form className="copilot-form" onSubmit={askCopilot}>
                <input value={prompt} onChange={(event) => setPrompt(event.target.value)} placeholder="Ask about emissions, compliance, or CSR" />
                <button type="submit" disabled={isLoading}>
                  {isLoading ? 'Thinking…' : 'Ask AI'}
                </button>
              </form>
              <p className="copilot-reply">{reply}</p>
            </div>
          </section>
        </>
      ) : null}

      {view === 'carbon' ? (
        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h3>Carbon log</h3>
              <span>Add a new activity</span>
            </div>
            <form className="stack-form" onSubmit={handleCarbonSubmit}>
              <input value={carbonForm.source} onChange={(event) => setCarbonForm({ ...carbonForm, source: event.target.value })} placeholder="Source" />
              <input value={carbonForm.amount} onChange={(event) => setCarbonForm({ ...carbonForm, amount: event.target.value })} placeholder="Amount" />
              <input value={carbonForm.unit} onChange={(event) => setCarbonForm({ ...carbonForm, unit: event.target.value })} placeholder="Unit" />
              <input value={carbonForm.date} onChange={(event) => setCarbonForm({ ...carbonForm, date: event.target.value })} placeholder="Date" />
              <button type="submit">Save log</button>
            </form>
          </div>
          <div className="panel">
            <div className="panel-header">
              <h3>Recent carbon entries</h3>
              <span>Stored records</span>
            </div>
            <div className="list-stack">
              {carbonLogs.map((item) => (
                <div className="list-item" key={item.id}>
                  <strong>{item.source}</strong>
                  <span>{item.amount} {item.unit} • {item.date}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      ) : null}

      {view === 'csr' ? (
        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h3>Create CSR activity</h3>
              <span>Engage employees in impact work</span>
            </div>
            <form className="stack-form" onSubmit={handleCSRSubmit}>
              <input value={csrForm.title} onChange={(event) => setCsrForm({ ...csrForm, title: event.target.value })} placeholder="Title" />
              <input value={csrForm.description} onChange={(event) => setCsrForm({ ...csrForm, description: event.target.value })} placeholder="Description" />
              <input value={csrForm.location} onChange={(event) => setCsrForm({ ...csrForm, location: event.target.value })} placeholder="Location" />
              <input value={csrForm.organizer} onChange={(event) => setCsrForm({ ...csrForm, organizer: event.target.value })} placeholder="Organizer" />
              <button type="submit">Publish activity</button>
            </form>
          </div>
          <div className="panel">
            <div className="panel-header">
              <h3>CSR activity feed</h3>
              <span>Recent community work</span>
            </div>
            <div className="list-stack">
              {csrActivities.map((item) => (
                <div className="list-item" key={item.id}>
                  <strong>{item.title}</strong>
                  <span>{item.location} • {item.organizer}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      ) : null}

      {view === 'governance' ? (
        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h3>Publish policy</h3>
              <span>Keep governance updated</span>
            </div>
            <form className="stack-form" onSubmit={handlePolicySubmit}>
              <input value={policyForm.title} onChange={(event) => setPolicyForm({ ...policyForm, title: event.target.value })} placeholder="Title" />
              <input value={policyForm.description} onChange={(event) => setPolicyForm({ ...policyForm, description: event.target.value })} placeholder="Description" />
              <input value={policyForm.version} onChange={(event) => setPolicyForm({ ...policyForm, version: event.target.value })} placeholder="Version" />
              <input value={policyForm.status} onChange={(event) => setPolicyForm({ ...policyForm, status: event.target.value })} placeholder="Status" />
              <button type="submit">Publish policy</button>
            </form>
          </div>
          <div className="panel">
            <div className="panel-header">
              <h3>Policy register</h3>
              <span>Current governance documents</span>
            </div>
            <div className="list-stack">
              {policies.map((item) => (
                <div className="list-item" key={item.id}>
                  <strong>{item.title}</strong>
                  <span>{item.version} • {item.status}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
      ) : null}
    </div>
  )
}

export default App
