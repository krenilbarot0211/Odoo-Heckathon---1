import { useEffect, useState } from 'react'
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
  const [dashboard, setDashboard] = useState<DashboardData>(fallbackData)
  const [prompt, setPrompt] = useState('How can we improve our ESG score?')
  const [reply, setReply] = useState('AI suggestions will appear here as soon as the backend responds.')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/dashboard')
        if (response.ok) {
          const data = (await response.json()) as DashboardData
          setDashboard(data)
        }
      } catch {
        setDashboard(fallbackData)
      }
    }

    void loadDashboard()
  }, [])

  const askCopilot = async (event: React.FormEvent) => {
    event.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/ai/copilot', {
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
            <input
              value={prompt}
              onChange={(event) => setPrompt(event.target.value)}
              placeholder="Ask about emissions, compliance, or CSR"
            />
            <button type="submit" disabled={isLoading}>
              {isLoading ? 'Thinking…' : 'Ask AI'}
            </button>
          </form>
          <p className="copilot-reply">{reply}</p>
        </div>
      </section>
    </div>
  )
}

export default App
