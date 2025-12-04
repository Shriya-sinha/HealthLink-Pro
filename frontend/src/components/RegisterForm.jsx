// src/components/RegisterForm.jsx
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const RegisterForm = ({ onToggleForm }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('patient');
  const [consentGiven, setConsentGiven] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    if (!consentGiven) {
      setError('You must agree to the terms and conditions.');
      return;
    }

    setLoading(true);

    const result = await register(email, password, role, consentGiven);
    
    if (!result.success) {
      setError(result.error || 'Registration failed. Please try again.');
    }
    
    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="logo-placeholder">150 x 150</div>
      <h2>Register</h2>
      
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
          minLength="6"
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          minLength="6"
        />
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="role-select"
        >
          <option value="patient">Patient</option>
          <option value="provider">Healthcare Provider</option>
        </select>
        
        <div className="consent-checkbox">
          <input
            type="checkbox"
            id="consent"
            checked={consentGiven}
            onChange={(e) => setConsentGiven(e.target.checked)}
          />
          <label htmlFor="consent">
            I agree to the terms and conditions and privacy policy
          </label>
        </div>
        
        <button type="submit" className="login-btn" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      
      <p className="register-link">
        Already have an account? 
        <button 
          type="button" 
          className="toggle-link" 
          onClick={onToggleForm}
        >
          Login here
        </button>
      </p>
    </div>
  );
};

export default RegisterForm;
