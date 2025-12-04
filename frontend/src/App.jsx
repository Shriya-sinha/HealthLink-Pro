// src/App.jsx
import { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import HealthDashboard from './components/HealthDashboard';
import './App.css';

function AppContent() {
  const { user, loading } = useAuth();
  const [isLoginForm, setIsLoginForm] = useState(true);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app-container">
      {!user ? (
        <>
          {isLoginForm ? (
            <LoginForm onToggleForm={() => setIsLoginForm(false)} />
          ) : (
            <RegisterForm onToggleForm={() => setIsLoginForm(true)} />
          )}
          <div className="preview-section">
            <div className="preview-overlay">
              <h2>Please login to access the Healthcare Portal</h2>
            </div>
          </div>
        </>
      ) : (
        <HealthDashboard />
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
