// src/context/AuthContext.jsx
import { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

// Configure axios base URL from environment
// In Docker: uses relative paths, Vite proxy handles /api routing
// In local dev: uses relative paths
const API_URL = '/';
axios.defaults.baseURL = API_URL;

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if token exists in localStorage on mount
    const token = localStorage.getItem('token');
    if (token) {
      // Validate token (in production, verify with backend)
      try {
        const userData = JSON.parse(localStorage.getItem('user'));
        setUser(userData);
        // Set authorization header
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/auth/login/', { email, password });
      
      const { token, role } = response.data;
      const userData = {
        email: email,
        role: role
      };

      localStorage.setItem('token', token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      
      // Set authorization header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response?.data?.error || error.message };
    }
  };

  const register = async (email, password, role = 'patient', consentGiven = false) => {
    try {
      const response = await axios.post('/api/auth/register/', {
        email,
        password,
        role,
        consent_given: consentGiven
      });
      
      // Auto-login after successful registration
      return await login(email, password);
    } catch (error) {
      const errorMessage = error.response?.data?.error?.email 
        ? 'Email already registered' 
        : error.response?.data?.error || 'Registration failed';
      return { success: false, error: errorMessage };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, register, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
