// frontend/src/pages/Clients.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { getClients, createClient, deleteClient, submitFeedback } from '../api';
import { Sidebar } from './Dashboard';

export default function Clients() {
  const [clients, setClients]         = useState([]);
  const [loading, setLoading]         = useState(true);
  const [showAdd, setShowAdd]         = useState(false);
  const [showFeed, setShowFeed]       = useState(false);
  const [feedText, setFeedText]       = useState('');
  const [feedResult, setFeedResult]   = useState(null);
  const [feedLoading, setFeedLoading] = useState(false);
  const [toast, setToast]             = useState('');
  const [form, setForm]               = useState({ name:'', email:'', tenure:'', monthly_charges:'' });
  const [addLoading, setAddLoading]   = useState(false);
  const navigate = useNavigate();

  const showToast = (msg) => { setToast(msg); setTimeout(() => setToast(''), 3000); };

  const load = useCallback(async () => {
    setLoading(true);
    try { const res = await getClients(); setClients(res.data); }
    catch { /* ignore */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { load(); }, [load]);

  const logout = () => { localStorage.removeItem('token'); navigate('/login'); };

  const handleAdd = async (e) => {
    e.preventDefault();
    setAddLoading(true);
    try {
      await createClient({
        name: form.name,
        email: form.email || null,
        tenure: form.tenure ? parseInt(form.tenure) : null,
        monthly_charges: form.monthly_charges ? parseFloat(form.monthly_charges) : null,
      });
      setShowAdd(false);
      setForm({ name:'', email:'', tenure:'', monthly_charges:'' });
      showToast('✅ Client ajouté avec prédiction de churn');
      load();
    } catch (err) {
      showToast('❌ ' + (err.response?.data?.detail || 'Erreur'));
    } finally {
      setAddLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer ce client ?')) return;
    try {
      await deleteClient(id);
      showToast('🗑️ Client supprimé');
      load();
    } catch { showToast('❌ Erreur de suppression'); }
  };

  const handleFeedback = async (e) => {
    e.preventDefault();
    setFeedLoading(true);
    setFeedResult(null);
    try {
      const res = await submitFeedback(feedText);
      setFeedResult(res.data);
      setFeedText('');
      showToast('✅ Feedback enregistré');
    } catch (err) {
      showToast('❌ ' + (err.response?.data?.detail || 'Erreur'));
    } finally {
      setFeedLoading(false);
    }
  };

  const riskBadge = (prob) => {
    if (prob == null) return <span className="badge badge-neutral">—</span>;
    if (prob >= 0.65) return <span className="badge badge-danger">🔴 Élevé</span>;
    if (prob >= 0.35) return <span className="badge badge-warning">🟡 Modéré</span>;
    return <span className="badge badge-success">🟢 Faible</span>;
  };

  const sentimentBadge = (label) => {
    if (!label) return null;
    if (label === 'positive') return <span className="badge badge-success">😊 Positif</span>;
    if (label === 'negative') return <span className="badge badge-danger">😞 Négatif</span>;
    return <span className="badge badge-neutral">😐 Neutre</span>;
  };

  return (
    <div className="layout">
      <Sidebar active="clients" onLogout={logout} />

      <div className="main">
        <div className="page-header">
          <div>
            <h2>Clients</h2>
            <p>Gestion des clients et analyse de sentiment</p>
          </div>
          <div style={{ display:'flex', gap:10 }}>
            <button id="feedback-btn" className="btn btn-ghost btn-sm" onClick={() => setShowFeed(true)}>
              💬 Feedback
            </button>
            <button id="add-client-btn" className="btn btn-primary btn-sm" onClick={() => setShowAdd(true)}>
              + Ajouter client
            </button>
          </div>
        </div>

        <div className="page-content">
          {loading ? (
            <div className="empty-state"><div className="spinner" style={{margin:'0 auto',borderTopColor:'var(--accent)'}}/></div>
          ) : clients.length === 0 ? (
            <div className="empty-state">
              <span style={{ fontSize: '2.5rem' }}>👥</span>
              <p>Aucun client enregistré. Cliquez sur "Ajouter client" pour commencer.</p>
            </div>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Nom</th>
                    <th>Email</th>
                    <th>Ancienneté</th>
                    <th>Charges/mois</th>
                    <th>Risque churn</th>
                    <th>Probabilité</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {clients.map(c => (
                    <tr key={c.id}>
                      <td style={{ color:'var(--text3)', fontSize:'0.78rem' }}>#{c.id}</td>
                      <td style={{ fontWeight:600 }}>{c.name}</td>
                      <td style={{ color:'var(--text2)' }}>{c.email || '—'}</td>
                      <td>{c.tenure != null ? `${c.tenure} mois` : '—'}</td>
                      <td>{c.monthly_charges != null ? `${c.monthly_charges.toFixed(2)} $` : '—'}</td>
                      <td>{riskBadge(c.churn_probability)}</td>
                      <td>
                        {c.churn_probability != null ? (
                          <div style={{ display:'flex', alignItems:'center', gap:8 }}>
                            <div className="prob-bar-bg" style={{ width:80 }}>
                              <div
                                className={`prob-bar-fill ${c.churn_probability >= 0.65 ? 'high' : c.churn_probability >= 0.35 ? 'medium' : 'low'}`}
                                style={{ width:`${c.churn_probability * 100}%` }}
                              />
                            </div>
                            <span style={{ fontSize:'0.78rem', color:'var(--text2)' }}>
                              {(c.churn_probability * 100).toFixed(1)}%
                            </span>
                          </div>
                        ) : '—'}
                      </td>
                      <td>
                        <button
                          id={`delete-${c.id}`}
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDelete(c.id)}
                        >
                          Supprimer
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* ─── ADD CLIENT MODAL ─── */}
      {showAdd && (
        <div className="panel-overlay" onClick={() => setShowAdd(false)}>
          <div className="panel" onClick={e => e.stopPropagation()}>
            <h3>👤 Ajouter un client</h3>
            <form onSubmit={handleAdd}>
              <div className="form-group">
                <label>Nom *</label>
                <input id="client-name" className="form-control" type="text" placeholder="Jean Dupont"
                  value={form.name} onChange={e => setForm({...form, name:e.target.value})} required />
              </div>
              <div className="form-group">
                <label>Email</label>
                <input id="client-email" className="form-control" type="email" placeholder="jean@example.com"
                  value={form.email} onChange={e => setForm({...form, email:e.target.value})} />
              </div>
              <div className="grid-2">
                <div className="form-group">
                  <label>Ancienneté (mois)</label>
                  <input id="client-tenure" className="form-control" type="number" min="0" placeholder="12"
                    value={form.tenure} onChange={e => setForm({...form, tenure:e.target.value})} />
                </div>
                <div className="form-group">
                  <label>Charges mensuelles ($)</label>
                  <input id="client-charges" className="form-control" type="number" step="0.01" placeholder="65.50"
                    value={form.monthly_charges} onChange={e => setForm({...form, monthly_charges:e.target.value})} />
                </div>
              </div>
              <p style={{ fontSize:'0.78rem', color:'var(--text3)', marginBottom:16 }}>
                ⚡ Le risque de churn sera calculé automatiquement à l'ajout.
              </p>
              <div className="panel-actions">
                <button type="button" className="btn btn-ghost" onClick={() => setShowAdd(false)}>Annuler</button>
                <button id="confirm-add-btn" type="submit" className="btn btn-primary" disabled={addLoading}>
                  {addLoading ? <span className="spinner" /> : null}
                  {addLoading ? 'Ajout...' : 'Ajouter'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ─── FEEDBACK MODAL ─── */}
      {showFeed && (
        <div className="panel-overlay" onClick={() => { setShowFeed(false); setFeedResult(null); }}>
          <div className="panel" onClick={e => e.stopPropagation()}>
            <h3>💬 Analyser un feedback client</h3>
            <form onSubmit={handleFeedback}>
              <div className="form-group">
                <label>Commentaire du client</label>
                <textarea
                  id="feedback-text"
                  className="form-control"
                  rows={4}
                  placeholder="Saisissez le commentaire du client ici..."
                  value={feedText}
                  onChange={e => setFeedText(e.target.value)}
                  required
                  style={{ resize:'vertical' }}
                />
              </div>

              {feedResult && (
                <div className={`result-box ${feedResult.sentiment_label === 'positive' ? 'low' : feedResult.sentiment_label === 'negative' ? 'high' : 'medium'}`} style={{ marginBottom:16 }}>
                  <div className="risk-label">Résultat de l'analyse</div>
                  <div style={{ display:'flex', alignItems:'center', gap:10, marginTop:8 }}>
                    {sentimentBadge(feedResult.sentiment_label)}
                    <span style={{ fontSize:'0.85rem', color:'var(--text2)' }}>
                      Score : {(feedResult.sentiment_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="prob-bar-wrap" style={{ marginTop:10 }}>
                    <div className="prob-bar-bg">
                      <div
                        className={`prob-bar-fill ${feedResult.sentiment_label === 'positive' ? 'low' : feedResult.sentiment_label === 'negative' ? 'high' : 'medium'}`}
                        style={{ width:`${feedResult.sentiment_score * 100}%` }}
                      />
                    </div>
                  </div>
                </div>
              )}

              <div className="panel-actions">
                <button type="button" className="btn btn-ghost" onClick={() => { setShowFeed(false); setFeedResult(null); }}>Fermer</button>
                <button id="submit-feedback-btn" type="submit" className="btn btn-primary" disabled={feedLoading}>
                  {feedLoading ? <span className="spinner" /> : '🔍'}
                  {feedLoading ? 'Analyse...' : 'Analyser'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {toast && <div className="toast">{toast}</div>}
    </div>
  );
}
