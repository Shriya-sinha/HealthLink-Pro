// src/components/HealthDashboard.jsx
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import InfoCard from './InfoCard';
import AppointmentBooking from './AppointmentBooking';
import MyAppointments from './MyAppointments';
import DoctorDashboard from './DoctorDashboard';

const HealthDashboard = () => {
  const { user, logout } = useAuth();
  const [currentView, setCurrentView] = useState('home');

  const healthInfo = [
    {
      title: 'COVID-19 Updates',
      description: 'Stay informed about the latest COVID-19 guidelines and vaccination information.'
    },
    {
      title: 'Seasonal Flu Prevention',
      description: 'Learn about steps you can take to prevent the seasonal flu and when to get vaccinated.'
    },
    {
      title: 'Mental Health Awareness',
      description: 'Explore resources and support options for maintaining good mental health.'
    }
  ];

  // Show doctor dashboard for providers
  if (user?.role === 'provider') {
    return (
      <DoctorDashboard onLogout={logout} />
    );
  }

  // Patient views
  if (currentView === 'booking') {
    return (
      <AppointmentBooking onBackToDashboard={() => setCurrentView('home')} />
    );
  }

  if (currentView === 'myappointments') {
    return (
      <MyAppointments onBackToDashboard={() => setCurrentView('home')} />
    );
  }

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h1>Healthcare Portal</h1>
        <div className="nav-links">
          <button 
            onClick={() => setCurrentView('home')} 
            className={currentView === 'home' ? 'active' : ''}
          >
            Home
          </button>
          <button 
            onClick={() => setCurrentView('booking')}
            className={currentView === 'booking' ? 'active' : ''}
          >
            Book Appointment
          </button>
          <button 
            onClick={() => setCurrentView('myappointments')}
            className={currentView === 'myappointments' ? 'active' : ''}
          >
            My Appointments
          </button>
          <button onClick={logout} className="logout-btn">Logout</button>
        </div>
      </nav>
      
      <div className="dashboard-content">
        <h2>Latest Health Information</h2>
        
        <div className="cards-container">
          {healthInfo.map((info, index) => (
            <InfoCard key={index} {...info} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default HealthDashboard;
