// src/components/LoginForm.jsx
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const LoginForm = ({ onToggleForm }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);
    
    if (!result.success) {
      setError(result.error || 'Invalid credentials. Please try again.');
    }
    
    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="logo-placeholder">150 x 150</div>
      <h2>Login</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="login-btn" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <a href="#" className="forgot-link">Forgot Password?</a>
      <p className="register-link">
        New User?
        <button 
          type="button" 
          className="toggle-link" 
          onClick={onToggleForm}
        >
          Register here
        </button>
      </p>
    </div>
  );
};

export default LoginForm;
