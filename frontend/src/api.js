// frontend/src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
});

// Inject JWT token on every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Redirect to login on 401
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;

// ─── AUTH ─────────────────────────────────────────────
export const login = (username, password) =>
  api.post('/auth/login', { username, password });

export const getMe = () => api.get('/auth/me');

// ─── CHURN ────────────────────────────────────────────
export const predictChurn = (data) => api.post('/churn/predict', data);

// ─── FEEDBACK ─────────────────────────────────────────
export const submitFeedback = (text, customer_id = null) =>
  api.post('/feedback/', { text, customer_id });

export const getFeedbacks = () => api.get('/feedback/');

// ─── DASHBOARD ────────────────────────────────────────
export const getDashboardStats = () => api.get('/dashboard/stats');

// ─── CLIENTS ──────────────────────────────────────────
export const getClients = () => api.get('/clients/');

export const createClient = (data) => api.post('/clients/', data);

export const deleteClient = (id) => api.delete(`/clients/${id}`);
