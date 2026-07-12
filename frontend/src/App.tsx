import { type FormEvent, useEffect, useState } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000/api'

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

type Report = {
  report_id: string
  title: string
  summary: string
  recommendations: string[]
}

type AnalyticsData = {
  emissions_trend: Array<{ month: string; value: number }>
  csr_trend: Array<{ month: string; value: number }>
  governance_health: number
}

type Badge = {
  name: string
  icon: string
  description: string
  unlocked: boolean
  progress?: number
}

type Challenge = {
  name: string
  icon: string
  description: string
  progress: number
  reward_xp: number
}

type GamificationData = {
  xp: number
  level: number
  xp_into_level: number
  xp_per_level: number
  badges: Badge[]
  challenges: Challenge[]
  leaderboard: LeaderboardEntry[]
}

type User = {
  id: number
  name: string
  email: string
  role: string
  department: string | null
  permissions?: string[]
}

type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
}

type View = 'dashboard' | 'environmental' | 'social' | 'governance' | 'gamification' | 'reports' | 'settings'

type AuthState = {
  isAuthenticated: boolean
  token: string | null
  user: User | null
  error: string
}

const NAV_ITEMS: Array<{ key: View; label: string; icon: string }> = [
  { key: 'dashboard', label: 'Dashboard', icon: '📊' },
  { key: 'environmental', label: 'Environmental', icon: '🌱' },
  { key: 'social', label: 'Social', icon: '👥' },
  { key: 'governance', label: 'Governance', icon: '🏛' },
  { key: 'gamification', label: 'Gamification', icon: '🏆' },
  { key: 'reports', label: 'Reports', icon: '📈' },
  { key: 'settings', label: 'Settings', icon: '⚙' },
]

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

const fallbackGamification: GamificationData = {
  xp: 0,
  level: 1,
  xp_into_level: 0,
  xp_per_level: 150,
  badges: [
    { name: 'ESG Rookie', icon: '🌱', description: 'Log your first ESG action', unlocked: false },
    { name: 'Carbon Tracker', icon: '📉', description: 'Log 5+ carbon entries', unlocked: false, progress: 0 },
    { name: 'Community Champion', icon: '🤝', description: 'Run 3+ CSR activities', unlocked: false, progress: 0 },
    { name: 'Policy Guardian', icon: '🛡', description: 'Publish 2+ active policies', unlocked: false, progress: 0 },
  ],
  challenges: [
    { name: 'Zero Waste Week', icon: '🌳', description: 'Log carbon data every day this week', progress: 0, reward_xp: 100 },
    { name: 'Volunteer Sprint', icon: '🩸', description: 'Organize or join 3 CSR activities', progress: 0, reward_xp: 150 },
    { name: 'Compliance Streak', icon: '🏛', description: 'Keep all policies active and up to date', progress: 0, reward_xp: 120 },
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
  const [report, setReport] = useState<Report | null>(null)
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [gamification, setGamification] = useState<GamificationData>(fallbackGamification)
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: "Hi! I'm the EcoSphere AI Copilot. Ask me about emissions, CSR, compliance, or your ESG score." },
  ])
  const [chatInput, setChatInput] = useState('How can we improve our ESG score?')
  const [isChatLoading, setIsChatLoading] = useState(false)
  const [auth, setAuth] = useState<AuthState>({ isAuthenticated: false, token: null, user: null, error: '' })
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login')
  const [loginForm, setLoginForm] = useState({ email: '', password: '' })
  const [registerForm, setRegisterForm] = useState({ name: '', email: '', password: '', role: 'employee' })
  const [carbonForm, setCarbonForm] = useState({ source: 'Electricity', amount: '320', unit: 'kWh', date: '2026-06-01' })
  const [csrForm, setCsrForm] = useState({ title: 'Community Tree Planting', description: 'Planting trees with local volunteers', location: 'Abuja', organizer: 'Operations' })
  const [policyForm, setPolicyForm] = useState({ title: 'Governance Charter', description: 'Updated compliance policy', version: 'v1.4', status: 'active' })
  const [notifyOn, setNotifyOn] = useState(true)

  useEffect(() => {
    void loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const response = await fetch(`${API_BASE}/dashboard`)
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
      const [carbonResponse, csrResponse, policyResponse, reportResponse, analyticsResponse, gamificationResponse] = await Promise.all([
        fetch(`${API_BASE}/carbon/analytics`),
        fetch(`${API_BASE}/csr/activities`),
        fetch(`${API_BASE}/governance/policies`),
        fetch(`${API_BASE}/reports/generate`),
        fetch(`${API_BASE}/reports/analytics`),
        fetch(`${API_BASE}/gamification/summary`),
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

      if (reportResponse.ok) {
        const reportData = await reportResponse.json()
        setReport(reportData)
      }

      if (analyticsResponse.ok) {
        const analyticsData = await analyticsResponse.json()
        setAnalytics(analyticsData)
      }

      if (gamificationResponse.ok) {
        const gamificationData = await gamificationResponse.json()
        setGamification(gamificationData)
      }

      void loadDashboard()
    } catch {
      setAuth((current) => ({ ...current, error: 'Unable to load module data right now.' }))
    }
  }

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault()
    setAuth((current) => ({ ...current, error: '' }))

    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
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
      setAuth((current) => ({ ...current, error: 'Login failed. Please check your credentials.' }))
    }
  }

  const handleLogout = () => {
    setAuth({ isAuthenticated: false, token: null, user: null, error: '' })
    setView('dashboard')
  }

  const handleRegister = async (event: FormEvent) => {
    event.preventDefault()
    setAuth((current) => ({ ...current, error: '' }))

    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(registerForm),
      })

      if (!response.ok) {
        throw new Error('Registration failed')
      }

      const data = await response.json()
      setAuth({ isAuthenticated: true, token: data.access_token, user: data.user, error: '' })
      void loadModuleData()
    } catch {
      setAuth((current) => ({ ...current, error: 'Registration failed. Please try again.' }))
    }
  }

  const sendChatMessage = async (event: FormEvent) => {
    event.preventDefault()
    const trimmed = chatInput.trim()
    if (!trimmed || isChatLoading) return

    const nextMessages: ChatMessage[] = [...chatMessages, { role: 'user', content: trimmed }]
    setChatMessages(nextMessages)
    setChatInput('')
    setIsChatLoading(true)

    try {
      const response = await fetch(`${API_BASE}/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: nextMessages }),
      })

      if (response.ok) {
        const data = await response.json()
        setChatMessages((current) => [...current, { role: 'assistant', content: data.reply }])
      } else {
        const errorData = await response.json().catch(() => null)
        const detail = errorData?.detail ?? 'The AI Copilot is currently unavailable.'
        setChatMessages((current) => [...current, { role: 'assistant', content: detail }])
      }
    } catch {
      setChatMessages((current) => [
        ...current,
        { role: 'assistant', content: 'The API is currently unavailable, so no live response could be generated.' },
      ])
    } finally {
      setIsChatLoading(false)
    }
  }

  const handleCarbonSubmit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      const response = await fetch(`${API_BASE}/carbon/log`, {
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
      const response = await fetch(`${API_BASE}/csr/activity`, {
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
      const response = await fetch(`${API_BASE}/governance/policy`, {
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

  // Recent activity feed derived from real records, newest first.
  const recentActivity = [
    ...carbonLogs.map((log) => ({
      icon: '🏭',
      text: `${log.amount} ${log.unit} of ${log.source} logged`,
      key: `carbon-${log.id}`,
    })),
    ...csrActivities.map((item) => ({
      icon: '✔',
      text: `${item.organizer} launched '${item.title}'`,
      key: `csr-${item.id}`,
    })),
    ...policies.map((item) => ({
      icon: '📝',
      text: `Policy '${item.title}' is ${item.status}`,
      key: `policy-${item.id}`,
    })),
  ].slice(-6).reverse()

  const xpPercentage = Math.min(100, Math.round((gamification.xp_into_level / gamification.xp_per_level) * 100))

  // ---- Unauthenticated: centered auth card ----
  if (!auth.isAuthenticated) {
    return (
      <div className="auth-shell">
        <div className="auth-card">
          <p className="eyebrow">EcoSphere AI</p>
          <h1>Turn ESG reporting into a live operating system.</h1>
          <p className="hero-copy">
            Track carbon, manage CSR, automate compliance, and level up your team with built-in ESG gamification.
          </p>

          <div className="auth-toggle">
            <button className={authMode === 'login' ? 'active' : ''} onClick={() => setAuthMode('login')}>Sign in</button>
            <button className={authMode === 'register' ? 'active' : ''} onClick={() => setAuthMode('register')}>Create account</button>
          </div>

          {authMode === 'login' ? (
            <form className="stack-form" onSubmit={handleLogin}>
              <input value={loginForm.email} onChange={(event) => setLoginForm({ ...loginForm, email: event.target.value })} placeholder="Email" />
              <input type="password" value={loginForm.password} onChange={(event) => setLoginForm({ ...loginForm, password: event.target.value })} placeholder="Password" />
              <button type="submit">Sign in</button>
            </form>
          ) : (
            <form className="stack-form" onSubmit={handleRegister}>
              <input value={registerForm.name} onChange={(event) => setRegisterForm({ ...registerForm, name: event.target.value })} placeholder="Full name" />
              <input value={registerForm.email} onChange={(event) => setRegisterForm({ ...registerForm, email: event.target.value })} placeholder="Email" />
              <input type="password" value={registerForm.password} onChange={(event) => setRegisterForm({ ...registerForm, password: event.target.value })} placeholder="Password" />
              <select value={registerForm.role} onChange={(event) => setRegisterForm({ ...registerForm, role: event.target.value })}>
                <option value="administrator">Administrator</option>
                <option value="esg_manager">ESG Manager</option>
                <option value="department_manager">Department Manager</option>
                <option value="employee">Employee</option>
                <option value="auditor">Auditor</option>
              </select>
              <button type="submit">Create account</button>
            </form>
          )}
          {auth.error ? <p className="error-text">{auth.error}</p> : null}
        </div>
      </div>
    )
  }

  // ---- Authenticated: sidebar shell ----
  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">🌍 EcoSphere</div>
        <nav className="side-nav">
          {NAV_ITEMS.map((item) => (
            <button
              key={item.key}
              className={view === item.key ? 'active' : ''}
              onClick={() => setView(item.key)}
            >
              <span className="side-icon">{item.icon}</span>
              {item.label}
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div className="xp-mini">
            <span>Lvl {gamification.level}</span>
            <div className="bar-track bar-track-sm">
              <div className="bar-fill" style={{ width: `${xpPercentage}%` }} />
            </div>
          </div>
        </div>
      </aside>

      <div className="main">
        <header className="topbar">
          <div>
            <strong>{NAV_ITEMS.find((item) => item.key === view)?.label}</strong>
            <p>Welcome back, {auth.user?.name} · {auth.user?.role.replace('_', ' ')}</p>
          </div>
          <button className="secondary-btn" onClick={handleLogout}>Log out</button>
        </header>

        <div className="content">
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
                    <h3>🕒 Recent activity</h3>
                    <span>Latest logged records</span>
                  </div>
                  <div className="list-stack">
                    {recentActivity.length ? (
                      recentActivity.map((item) => (
                        <div className="list-item list-item-icon" key={item.key}>
                          <span>{item.icon}</span>
                          <span>{item.text}</span>
                        </div>
                      ))
                    ) : (
                      <p className="muted">No activity yet — log a carbon entry or CSR activity to get started.</p>
                    )}
                  </div>
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
                    <h3>⚡ Quick actions</h3>
                    <span>Jump into a module</span>
                  </div>
                  <div className="quick-actions">
                    <button onClick={() => setView('environmental')}>🏭 Log carbon data</button>
                    <button onClick={() => setView('gamification')}>🏆 Start a challenge</button>
                    <button onClick={() => setView('reports')}>📄 View reports</button>
                  </div>
                </div>
              </section>

              <section className="content-grid">
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

                <div className="panel chat-panel">
                  <div className="panel-header">
                    <h3>AI Copilot</h3>
                    <span>Chat about emissions, compliance, or CSR</span>
                  </div>
                  <div className="chat-history">
                    {chatMessages.map((message, index) => (
                      <div key={index} className={`chat-bubble chat-bubble-${message.role}`}>
                        {message.content}
                      </div>
                    ))}
                    {isChatLoading ? <div className="chat-bubble chat-bubble-assistant chat-bubble-loading">Thinking…</div> : null}
                  </div>
                  <form className="copilot-form" onSubmit={sendChatMessage}>
                    <input
                      value={chatInput}
                      onChange={(event) => setChatInput(event.target.value)}
                      placeholder="Ask about emissions, compliance, or CSR"
                    />
                    <button type="submit" disabled={isChatLoading || !chatInput.trim()}>
                      {isChatLoading ? 'Thinking…' : 'Send'}
                    </button>
                  </form>
                </div>
              </section>
            </>
          ) : null}

          {view === 'environmental' ? (
            <section className="content-grid">
              <div className="panel">
                <div className="panel-header">
                  <h3>📈 Emission trend</h3>
                  <span>Rolling 3-month view</span>
                </div>
                <div className="list-stack">
                  {analytics?.emissions_trend.map((item) => (
                    <div className="list-item" key={item.month}>
                      <strong>{item.month}</strong>
                      <span>{item.value.toFixed(1)} tCO₂e</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="panel">
                <div className="panel-header">
                  <h3>Log carbon data</h3>
                  <span>Record a new activity</span>
                </div>
                <form className="stack-form" onSubmit={handleCarbonSubmit}>
                  <input value={carbonForm.source} onChange={(event) => setCarbonForm({ ...carbonForm, source: event.target.value })} placeholder="Source" />
                  <input value={carbonForm.amount} onChange={(event) => setCarbonForm({ ...carbonForm, amount: event.target.value })} placeholder="Amount" />
                  <input value={carbonForm.unit} onChange={(event) => setCarbonForm({ ...carbonForm, unit: event.target.value })} placeholder="Unit" />
                  <input value={carbonForm.date} onChange={(event) => setCarbonForm({ ...carbonForm, date: event.target.value })} placeholder="Date" />
                  <button type="submit">Save log</button>
                </form>
              </div>
              <div className="panel panel-wide">
                <div className="panel-header">
                  <h3>Carbon transactions</h3>
                  <span>Stored records</span>
                </div>
                <div className="table-wrap">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Source</th>
                        <th>Amount</th>
                        <th>Unit</th>
                        <th>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {carbonLogs.map((item) => (
                        <tr key={item.id}>
                          <td>{item.source}</td>
                          <td>{item.amount}</td>
                          <td>{item.unit}</td>
                          <td>{item.date}</td>
                        </tr>
                      ))}
                      {!carbonLogs.length ? (
                        <tr><td colSpan={4} className="muted">No carbon transactions logged yet.</td></tr>
                      ) : null}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          ) : null}

          {view === 'social' ? (
            <section className="content-grid">
              <div className="panel">
                <div className="panel-header">
                  <h3>Participation trend</h3>
                  <span>Volunteer activity growth</span>
                </div>
                <div className="list-stack">
                  {analytics?.csr_trend.map((item) => (
                    <div className="list-item" key={item.month}>
                      <strong>{item.month}</strong>
                      <span>{item.value}% participation</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="panel">
                <div className="panel-header">
                  <h3>+ New activity</h3>
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
              <div className="panel panel-wide">
                <div className="panel-header">
                  <h3>CSR activity feed</h3>
                  <span>Recent community work</span>
                </div>
                <div className="card-row">
                  {csrActivities.map((item) => (
                    <div className="mini-card" key={item.id}>
                      <strong>{item.title}</strong>
                      <span>{item.description}</span>
                      <span className="muted">{item.location} • {item.organizer}</span>
                    </div>
                  ))}
                  {!csrActivities.length ? <p className="muted">No CSR activities published yet.</p> : null}
                </div>
              </div>
            </section>
          ) : null}

          {view === 'governance' ? (
            <section className="content-grid">
              <div className="panel">
                <div className="panel-header">
                  <h3>Governance health</h3>
                  <span>Current compliance pulse</span>
                </div>
                <div className="list-item">
                  <strong>{analytics?.governance_health ?? 0}%</strong>
                  <span>Overall governance readiness</span>
                </div>
              </div>
              <div className="panel">
                <div className="panel-header">
                  <h3>Publish policy</h3>
                  <span>Keep governance updated</span>
                </div>
                <form className="stack-form" onSubmit={handlePolicySubmit}>
                  <input value={policyForm.title} onChange={(event) => setPolicyForm({ ...policyForm, title: event.target.value })} placeholder="Title" />
                  <input value={policyForm.description} onChange={(event) => setPolicyForm({ ...policyForm, description: event.target.value })} placeholder="Description" />
                  <input value={policyForm.version} onChange={(event) => setPolicyForm({ ...policyForm, version: event.target.value })} placeholder="Version" />
                  <select value={policyForm.status} onChange={(event) => setPolicyForm({ ...policyForm, status: event.target.value })}>
                    <option value="draft">Draft</option>
                    <option value="active">Active</option>
                    <option value="retired">Retired</option>
                  </select>
                  <button type="submit">Publish policy</button>
                </form>
              </div>
              <div className="panel panel-wide">
                <div className="panel-header">
                  <h3>Policy register</h3>
                  <span>Current governance documents</span>
                </div>
                <div className="table-wrap">
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Title</th>
                        <th>Version</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {policies.map((item) => (
                        <tr key={item.id}>
                          <td>{item.title}</td>
                          <td>{item.version}</td>
                          <td><span className={`status-pill status-${item.status}`}>{item.status}</span></td>
                        </tr>
                      ))}
                      {!policies.length ? (
                        <tr><td colSpan={3} className="muted">No policies published yet.</td></tr>
                      ) : null}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          ) : null}

          {view === 'gamification' ? (
            <>
              <section className="panel xp-panel">
                <div className="xp-header">
                  <div>
                    <p className="eyebrow">Your progress</p>
                    <h2>Level {gamification.level}</h2>
                  </div>
                  <div className="xp-total">{gamification.xp} XP total</div>
                </div>
                <div className="bar-track bar-track-lg">
                  <div className="bar-fill" style={{ width: `${xpPercentage}%` }} />
                </div>
                <span className="muted">{gamification.xp_into_level} / {gamification.xp_per_level} XP to level {gamification.level + 1}</span>
              </section>

              <section className="content-grid">
                <div className="panel panel-wide">
                  <div className="panel-header">
                    <h3>🏆 Badges</h3>
                    <span>Unlocked by real ESG activity</span>
                  </div>
                  <div className="badge-grid">
                    {gamification.badges.map((badge) => (
                      <div className={`badge-card ${badge.unlocked ? 'unlocked' : ''}`} key={badge.name}>
                        <span className="badge-icon">{badge.icon}</span>
                        <strong>{badge.name}</strong>
                        <span className="muted">{badge.description}</span>
                        {badge.progress !== undefined && !badge.unlocked ? (
                          <div className="bar-track bar-track-sm">
                            <div className="bar-fill" style={{ width: `${badge.progress}%` }} />
                          </div>
                        ) : (
                          <span className={`status-pill ${badge.unlocked ? 'status-active' : 'status-draft'}`}>
                            {badge.unlocked ? 'Unlocked' : 'Locked'}
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              </section>

              <section className="content-grid">
                <div className="panel panel-wide">
                  <div className="panel-header">
                    <h3>Active challenges</h3>
                    <span>Complete for bonus XP</span>
                  </div>
                  <div className="card-row">
                    {gamification.challenges.map((challenge) => (
                      <div className="mini-card challenge-card" key={challenge.name}>
                        <div className="challenge-title">
                          <span>{challenge.icon}</span>
                          <strong>{challenge.name}</strong>
                        </div>
                        <span className="muted">{challenge.description}</span>
                        <div className="bar-track bar-track-sm">
                          <div className="bar-fill" style={{ width: `${challenge.progress}%` }} />
                        </div>
                        <div className="challenge-footer">
                          <span className="muted">{challenge.progress}% complete</span>
                          <span className="xp-chip">+{challenge.reward_xp} XP</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="panel">
                  <div className="panel-header">
                    <h3>Leaderboard</h3>
                    <span>Top teams this quarter</span>
                  </div>
                  <ul className="leaderboard-list">
                    {gamification.leaderboard.map((entry, index) => (
                      <li key={entry.name}>
                        <span>{index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${index + 1}`} {entry.name}</span>
                        <strong>{entry.score}/100</strong>
                      </li>
                    ))}
                  </ul>
                </div>
              </section>
            </>
          ) : null}

          {view === 'reports' ? (
            <>
              {report ? (
                <section className="panel report-panel">
                  <div className="panel-header">
                    <h3>{report.title}</h3>
                    <span>{report.report_id}</span>
                  </div>
                  <p>{report.summary}</p>
                  <ul className="initiative-list">
                    {report.recommendations.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </section>
              ) : (
                <section className="panel">
                  <p className="muted">No report generated yet.</p>
                </section>
              )}
              <section className="content-grid">
                <div className="panel">
                  <div className="panel-header">
                    <h3>Emissions trend</h3>
                    <span>Environmental report</span>
                  </div>
                  <div className="list-stack">
                    {analytics?.emissions_trend.map((item) => (
                      <div className="list-item" key={item.month}>
                        <strong>{item.month}</strong>
                        <span>{item.value.toFixed(1)} tCO₂e</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="panel">
                  <div className="panel-header">
                    <h3>CSR participation trend</h3>
                    <span>Social report</span>
                  </div>
                  <div className="list-stack">
                    {analytics?.csr_trend.map((item) => (
                      <div className="list-item" key={item.month}>
                        <strong>{item.month}</strong>
                        <span>{item.value}% participation</span>
                      </div>
                    ))}
                  </div>
                </div>
              </section>
            </>
          ) : null}

          {view === 'settings' ? (
            <section className="content-grid">
              <div className="panel">
                <div className="panel-header">
                  <h3>Profile</h3>
                  <span>Your account details</span>
                </div>
                <div className="list-stack">
                  <div className="list-item"><strong>Name</strong><span>{auth.user?.name}</span></div>
                  <div className="list-item"><strong>Email</strong><span>{auth.user?.email}</span></div>
                  <div className="list-item"><strong>Role</strong><span>{auth.user?.role}</span></div>
                  <div className="list-item"><strong>Department</strong><span>{auth.user?.department ?? 'Unassigned'}</span></div>
                </div>
              </div>
              <div className="panel">
                <div className="panel-header">
                  <h3>Notifications</h3>
                  <span>Manage alert preferences</span>
                </div>
                <label className="toggle-row">
                  <span>Email me about new compliance issues and challenges</span>
                  <input type="checkbox" checked={notifyOn} onChange={(event) => setNotifyOn(event.target.checked)} />
                </label>
              </div>
              <div className="panel panel-wide">
                <div className="panel-header">
                  <h3>ESG configuration</h3>
                  <span>Departments &amp; categories tracked in this workspace</span>
                </div>
                <div className="card-row">
                  {['Sales', 'Manufacturing', 'Logistics', 'Corporate', 'R&D'].map((dept) => (
                    <span className="chip" key={dept}>{dept}</span>
                  ))}
                </div>
              </div>
            </section>
          ) : null}
        </div>
      </div>
    </div>
  )
}

export default App
