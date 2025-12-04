// src/components/MyAppointments.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './MyAppointments.css';

function MyAppointments({ onBackToDashboard }) {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/appointments/');
      setAppointments(response.data.appointments || []);
      setError('');
    } catch (err) {
      setError('Failed to fetch appointments. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelAppointment = async (appointmentId) => {
    if (!window.confirm('Are you sure you want to cancel this appointment?')) {
      return;
    }

    try {
      await axios.delete(`/api/appointments/${appointmentId}/`);
      setAppointments(appointments.map(apt => 
        apt.id === appointmentId ? { ...apt, status: 'cancelled' } : apt
      ));
    } catch (err) {
      setError('Failed to cancel appointment. Please try again.');
      console.error(err);
    }
  };

  const getStatusBadgeClass = (status) => {
    return `status-badge status-${status}`;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="my-appointments-container">
      <div className="appointments-header">
        <h2>My Appointments</h2>
        <button className="back-btn" onClick={onBackToDashboard}>
          ← Back to Dashboard
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading-message">Loading your appointments...</div>
      ) : appointments.length === 0 ? (
        <div className="no-appointments">
          <p>You don't have any appointments yet.</p>
          <p>Book your first appointment to get started!</p>
        </div>
      ) : (
        <div className="appointments-list">
          {appointments.map((appointment) => (
            <div key={appointment.id} className="appointment-card">
              <div className="appointment-card-header">
                <div className="appointment-info">
                  <h3>Appointment with Doctor</h3>
                  <p className="appointment-date">
                    📅 {formatDate(appointment.appointment_date)}
                  </p>
                </div>
                <span className={getStatusBadgeClass(appointment.status)}>
                  {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                </span>
              </div>

              <div className="appointment-card-body">
                {appointment.reason && (
                  <div className="appointment-detail">
                    <strong>Reason:</strong> {appointment.reason}
                  </div>
                )}

                <div className="appointment-detail">
                  <strong>Provider Email:</strong> {appointment.provider_email}
                </div>

                {appointment.notes && (
                  <div className="appointment-detail">
                    <strong>Doctor's Notes:</strong> {appointment.notes}
                  </div>
                )}

                <div className="appointment-detail">
                  <strong>Booked on:</strong> {formatDate(appointment.created_at)}
                </div>
              </div>

              {appointment.status === 'pending' && (
                <div className="appointment-card-footer">
                  <button
                    className="cancel-btn"
                    onClick={() => handleCancelAppointment(appointment.id)}
                  >
                    Cancel Appointment
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MyAppointments;
