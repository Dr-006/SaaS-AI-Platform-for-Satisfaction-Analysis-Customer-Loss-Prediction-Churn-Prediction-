// frontend/src/pages/Dashboard.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
} from 'recharts';
import { getDashboardStats, predictChurn } from '../api';

const COLORS = ['#f43f5e', '#fbbf24', '#10b981']; // High, Medium, Low
const BAR_COLOR = '#6c63ff';

const FIELDS = [
  { name:'gender',          label:'Genre',           type:'select',   opts:['Male','Female'] },
  { name:'SeniorCitizen',   label:'Senior',          type:'select',   opts:[{label:'Non',val:0},{label:'Oui',val:1}], isInt:true },
  { name:'tenure',          label:'Ancienneté (mois)',type:'number' },
  { name:'MonthlyCharges',  label:'Charges mensuelles',type:'number' },
  { name:'TotalCharges',    label:'Charges totales', type:'text' },
  { name:'Contract',        label:'Contrat',         type:'select',   opts:['Month-to-month','One year','Two year'] },
  { name:'InternetService', label:'Internet',        type:'select',   opts:['DSL','Fiber optic','No'] },
  { name:'PaymentMethod',   label:'Paiement',        type:'select',   opts:['Electronic check','Mailed check','Bank transfer (automatic)','Credit card (automatic)'] },
  { name:'TechSupport',     label:'Support tech',    type:'select',   opts:['Yes','No','No internet service'] },
  { name:'OnlineSecurity',  label:'Sécurité online', type:'select',   opts:['Yes','No','No internet service'] },
];

export default function Dashboard() {
  const [stats, setStats]       = useState(null);
  const [loading, setLoading]   = useState(true);
  const [form, setForm]         = useState({});
  const [result, setResult]     = useState(null);
  const [predLoading, setPredLoading] = useState(false);
  const navigate = useNavigate();

  const load = useCallback(async () => {
    try {
      const res = await getDashboardStats();
      setStats(res.data);
    } catch {
      /* empty DB is fine */
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const logout = () => { localStorage.removeItem('token'); navigate('/login'); };

  const handleChange = (name, value) => setForm(f => ({ ...f, [name]: value }));

  const handlePredict = async (e) => {
    e.preventDefault();
    setPredLoading(true);
    setResult(null);
    try {
      const payload = { ...form };
      FIELDS.forEach(f => {
        if (f.isInt && payload[f.name] !== undefined) payload[f.name] = parseInt(payload[f.name]);
        if (f.type === 'number' && payload[f.name] !== undefined) payload[f.name] = parseFloat(payload[f.name]);
      });
      const res = await predictChurn(payload);
      setResult(res.data);
      load(); // refresh stats
    } catch (err) {
      setResult({ error: err.response?.data?.detail || 'Erreur de prédiction' });
    } finally {
      setPredLoading(false);
    }
  };

  const riskPieData = stats?.risk_distribution || [];
  
  // Custom tooltips
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ background: 'var(--surface2)', padding: '10px 14px', border: '1px solid var(--border)', borderRadius: '8px', color: 'var(--text)' }}>
          <p style={{ margin: 0, fontWeight: 600, fontSize: '0.85rem' }}>{label || payload[0].name}</p>
          <p style={{ margin: '4px 0 0', color: payload[0].fill || 'var(--text2)', fontSize: '0.8rem' }}>
            Valeur : <span style={{fontWeight: 700}}>{payload[0].value}{payload[0].name === 'HIGH' || payload[0].name === 'MEDIUM' || payload[0].name === 'LOW' ? '%' : ''}</span>
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="layout">
      <Sidebar active="dashboard" onLogout={logout} />

      <div className="main">
        <div className="page-header">
          <div>
            <h2>Dashboard</h2>
            <p>Vue globale des prédictions et de l'activité</p>
          </div>
          <button className="btn btn-ghost btn-sm" onClick={load} id="refresh-btn">
            ↻ Rafraîchir
          </button>
        </div>

        <div className="page-content">
          {/* ─── KPIS PRINCIPAUX ─── */}
          <div className="section-title">KPIS PRINCIPAUX</div>
          <div className="stats-grid">
            <div className="stat-card purple">
              <div className="stat-label">Taux Churn Global</div>
              <div className="stat-value">
                {loading ? '—' : `${((stats?.global_churn_rate ?? 0) * 100).toFixed(1)}%`}
              </div>
              <div className="stat-sub">Moyenne globale</div>
            </div>
            <div className="stat-card green">
              <div className="stat-label">Clients Analysés</div>
              <div className="stat-value">{loading ? '—' : (stats?.total_analyzed ?? 0).toLocaleString('fr-FR')}</div>
              <div className="stat-sub">Volume total</div>
            </div>
            <div className="stat-card blue">
              <div className="stat-label">Satisfaction Client</div>
              <div className="stat-value">
                {loading ? '—' : `${stats?.customer_satisfaction_score ?? 0}%`}
              </div>
              <div className="stat-sub">
                {loading ? 'Calcul...' : `Niveau ${stats?.satisfaction_level ?? 'N/A'}`}
              </div>
            </div>
            <div className="stat-card red">
              <div className="stat-label">Haut Risque</div>
              <div className="stat-value">{loading ? '—' : (stats?.high_risk_count ?? 0).toLocaleString('fr-FR')}</div>
              <div className="stat-sub">Clients en alerte rouge</div>
            </div>
            <div className="stat-card amber">
              <div className="stat-label">Moyen Risque</div>
              <div className="stat-value">{loading ? '—' : (stats?.medium_risk_count ?? 0).toLocaleString('fr-FR')}</div>
              <div className="stat-sub">Clients à surveiller</div>
            </div>
          </div>

          {/* ─── GRAPHIQUES ─── */}
          <div className="section-title" style={{ marginTop: '32px' }}>GRAPHIQUES</div>
          <div className="grid-2" style={{ marginBottom: '24px' }}>
            
            {/* 1. Distribution churn par contrat */}
            <div className="card">
              <div className="chart-title">Distribution churn par contrat</div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={stats?.churn_by_contract || []} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={true} vertical={false} />
                  <XAxis type="number" tick={{ fill: 'var(--text2)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis dataKey="name" type="category" tick={{ fill: 'var(--text3)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Bar dataKey="value" fill={BAR_COLOR} radius={[0, 6, 6, 0]} barSize={24} name="%" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* 2. Churn par ancienneté */}
            <div className="card">
              <div className="chart-title">Churn par ancienneté</div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={stats?.churn_by_tenure || []} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <XAxis dataKey="name" tick={{ fill: 'var(--text2)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: 'var(--text3)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Bar dataKey="value" fill="#3b82f6" radius={[6, 6, 0, 0]} barSize={36} name="%" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* 3. Importance des features */}
            <div className="card">
              <div className="chart-title">Importance des features</div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={stats?.feature_importance || []} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={true} vertical={false} />
                  <XAxis type="number" tick={{ fill: 'var(--text2)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis dataKey="name" type="category" tick={{ fill: 'var(--text3)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Bar dataKey="value" fill="#8b5cf6" radius={[0, 6, 6, 0]} barSize={24} name="Importance" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* 4. Répartition des risques */}
            <div className="card">
              <div className="chart-title">Répartition des risques</div>
              <ResponsiveContainer width="100%" height={260}>
                <PieChart>
                  <Pie 
                    data={riskPieData} 
                    cx="50%" cy="50%" 
                    innerRadius={70} outerRadius={100} 
                    paddingAngle={4} 
                    dataKey="value"
                  >
                    {riskPieData.map((entry, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <RechartsTooltip content={<CustomTooltip />} />
                  <Legend iconType="circle" wrapperStyle={{ fontSize: '0.85rem', color: 'var(--text2)' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>

          </div>

          {/* ─── PREDICT FORM ─── */}
          <div className="card">
            <div className="section-title">🔮 Prédiction rapide</div>
            <form onSubmit={handlePredict}>
              <div className="grid-3">
                {FIELDS.map(f => (
                  <div className="form-group" key={f.name}>
                    <label>{f.label}</label>
                    {f.type === 'select' ? (
                      <select
                        id={`pred-${f.name}`}
                        className="form-control"
                        value={form[f.name] ?? ''}
                        onChange={e => handleChange(f.name, f.isInt ? parseInt(e.target.value) : e.target.value)}
                      >
                        <option value="">-- Choisir --</option>
                        {f.opts.map(o =>
                          typeof o === 'object'
                            ? <option key={o.val} value={o.val}>{o.label}</option>
                            : <option key={o} value={o}>{o}</option>
                        )}
                      </select>
                    ) : (
                      <input
                        id={`pred-${f.name}`}
                        type={f.type}
                        className="form-control"
                        placeholder={f.label}
                        value={form[f.name] ?? ''}
                        onChange={e => handleChange(f.name, e.target.value)}
                      />
                    )}
                  </div>
                ))}
              </div>

              <button id="predict-btn" type="submit" className="btn btn-primary" disabled={predLoading}>
                {predLoading ? <span className="spinner" /> : '⚡'}
                {predLoading ? 'Analyse...' : 'Prédire le churn'}
              </button>
            </form>

            {result && !result.error && (
              <div className={`result-box ${result.risk_level}`}>
                <div className="risk-label">Niveau de risque</div>
                <div className="risk-value">
                  {result.risk_level === 'high'   && '🔴 Risque élevé'}
                  {result.risk_level === 'medium'  && '🟡 Risque modéré'}
                  {result.risk_level === 'low'     && '🟢 Faible risque'}
                </div>
                <div className="prob-bar-wrap">
                  <div style={{ display:'flex', justifyContent:'space-between', marginBottom:4, fontSize:'0.8rem', color:'var(--text2)' }}>
                    <span>Probabilité de churn</span>
                    <span>{(result.probability * 100).toFixed(1)}%</span>
                  </div>
                  <div className="prob-bar-bg">
                    <div
                      className={`prob-bar-fill ${result.risk_level}`}
                      style={{ width: `${result.probability * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            )}

            {result?.error && (
              <div className="error-msg" style={{ marginTop: 12 }}>⚠️ {result.error}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── SHARED SIDEBAR ────────────────────────────────────────────────────
export function Sidebar({ active, onLogout }) {
  const navItems = [
    { id: 'dashboard', icon: '📊', label: 'Dashboard', to: '/dashboard' },
    { id: 'clients',   icon: '👥', label: 'Clients',   to: '/clients'   },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h1>⚡ ChurnGuard</h1>
        <p>ML Platform v1.0</p>
      </div>
      <nav className="sidebar-nav">
        {navItems.map(item => (
          <Link
            key={item.id}
            to={item.to}
            className={`nav-item ${active === item.id ? 'active' : ''}`}
            id={`nav-${item.id}`}
          >
            <span>{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
      <div className="sidebar-footer">
        <button id="logout-btn" className="nav-item" style={{color:'var(--danger)'}} onClick={onLogout}>
          <span>🚪</span> Déconnexion
        </button>
      </div>
    </aside>
  );
}
