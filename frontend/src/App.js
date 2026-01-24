import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';

// Backend API URL from environment variable
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [status, setStatus] = useState(null);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [healthError, setHealthError] = useState(null);
  const [isBackendOnline, setIsBackendOnline] = useState(null); // null = unknown, true = online, false = offline

  // Fetch health check
  const fetchHealth = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/health`, {
        timeout: 5000 // 5 second timeout
      });
      setHealth(response.data);
      setHealthError(null);
      setIsBackendOnline(true);
    } catch (err) {
      const errorMessage = err.code === 'ECONNABORTED' 
        ? 'Backend request timeout' 
        : err.message || 'Health check failed';
      setHealthError(`Health check failed: ${errorMessage}`);
      setIsBackendOnline(false);
      setHealth(null);
    }
  }, []);

  // Fetch API status
  const fetchStatus = async () => {
    setLoading(true);
    setError(null);
    setStatus(null); // Clear previous status
    try {
      const response = await axios.get(`${API_URL}/api/status`, {
        timeout: 5000 // 5 second timeout
      });
      
      // Log response for debugging
      console.log('API Status Response:', response.data);
      
      if (response.data && typeof response.data === 'object') {
        setStatus(response.data);
        setIsBackendOnline(true);
      } else {
        setError('API returned invalid response format');
        setIsBackendOnline(false);
      }
    } catch (err) {
      console.error('API Status Error:', err);
      const errorMessage = err.code === 'ECONNABORTED'
        ? 'Backend request timeout'
        : err.code === 'ERR_NETWORK'
        ? 'Cannot connect to backend. Make sure the backend is running on port 8000.'
        : err.response?.data?.detail || err.message || 'Failed to fetch status';
      setError(errorMessage);
      setIsBackendOnline(false);
      setStatus(null); // Clear status on error
    } finally {
      setLoading(false);
    }
  };

  // Fetch health on component mount and set up polling
  useEffect(() => {
    // Initial health check
    fetchHealth();
    
    // Poll health every 30 seconds
    const interval = setInterval(fetchHealth, 30000);
    
    return () => clearInterval(interval);
  }, [fetchHealth]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🚀 Modern DevOps Delivery System</h1>
        <p>Frontend + Backend + MongoDB Atlas</p>
        {isBackendOnline === true && (
          <p className="connection-status online">🟢 Backend Connected</p>
        )}
        {isBackendOnline === false && (
          <p className="connection-status offline">🔴 Backend Offline</p>
        )}
        {isBackendOnline === null && (
          <p className="connection-status unknown">🟡 Checking connection...</p>
        )}
      </header>

      <main className="App-main">
        <div className="status-card">
          <h2>System Status</h2>
          
          {health && (
            <div className="health-status">
              <p>
                <strong>Backend Health:</strong>{' '}
                <span className={health.status === 'healthy' ? 'status-ok' : 'status-error'}>
                  {health.status || 'unknown'}
                </span>
              </p>
              {health.database && (
                <p>
                  <strong>Database:</strong>{' '}
                  <span className={health.database === 'connected' ? 'status-ok' : 'status-error'}>
                    {health.database}
                  </span>
                </p>
              )}
              {health.timestamp && (
                <p className="timestamp">
                  Last checked: {new Date(health.timestamp).toLocaleString()}
                </p>
              )}
            </div>
          )}

          {healthError && !health && (
            <div className="error-message">
              <p>⚠️ {healthError}</p>
              <button onClick={fetchHealth} className="btn-retry">
                Retry Health Check
              </button>
            </div>
          )}

          <button 
            onClick={fetchStatus} 
            disabled={loading} 
            className="btn-primary"
            aria-label="Check API status"
          >
            {loading ? 'Loading...' : 'Check API Status'}
          </button>

          {loading && (
            <div className="loading-indicator">
              <p>⏳ Fetching API status...</p>
            </div>
          )}

          {status && (
            <div className="api-status">
              <h3>API Information</h3>
              {Object.keys(status).length > 0 ? (
                <pre>{JSON.stringify(status, null, 2)}</pre>
              ) : (
                <p className="empty-status">⚠️ API returned empty response</p>
              )}
            </div>
          )}

          {error && (
            <div className="error-message">
              <p>❌ {error}</p>
              {!isBackendOnline && (
                <p className="help-text">
                  💡 Tip: Start the backend server by running:<br />
                  <code>cd backend && python main.py</code>
                </p>
              )}
            </div>
          )}
        </div>

        <div className="info-card">
          <h2>📋 Project Info</h2>
          <ul>
            <li>✅ FastAPI Backend</li>
            <li>✅ React Frontend</li>
            <li>✅ MongoDB Atlas Database</li>
            <li>✅ Docker Compose</li>
            <li>🔄 Kubernetes (Coming Next)</li>
            <li>🔄 CI/CD Pipeline (Coming Next)</li>
          </ul>
          
          <div className="api-endpoints">
            <h3>🔗 API Endpoints</h3>
            <ul>
              <li><a href={`${API_URL}/health`} target="_blank" rel="noopener noreferrer">/health</a></li>
              <li><a href={`${API_URL}/api/status`} target="_blank" rel="noopener noreferrer">/api/status</a></li>
              <li><a href={`${API_URL}/docs`} target="_blank" rel="noopener noreferrer">/docs (Swagger UI)</a></li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
