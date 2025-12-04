// src/components/DoctorDashboard.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './DoctorDashboard.css';

function DoctorDashboard({ onLogout }) {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [updateStatus, setUpdateStatus] = useState('');
  const [updateNotes, setUpdateNotes] = useState('');
  const [showUpdateModal, setShowUpdateModal] = useState(false);

  useEffect(() => {
    fetchAppointments();
    // Refresh appointments every 30 seconds
    const interval = setInterval(fetchAppointments, 30000);
    return () => clearInterval(interval);
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

  const handleOpenUpdateModal = (appointment) => {
    setSelectedAppointment(appointment);
    setUpdateStatus(appointment.status);
    setUpdateNotes(appointment.notes || '');
    setShowUpdateModal(true);
  };

  const handleCloseUpdateModal = () => {
    setShowUpdateModal(false);
    setSelectedAppointment(null);
    setUpdateStatus('');
    setUpdateNotes('');
  };

  const handleUpdateAppointment = async () => {
    if (!selectedAppointment) return;

    try {
      const response = await axios.put(
        `/api/appointments/${selectedAppointment.id}/`,
        {
          status: updateStatus,
          notes: updateNotes,
        }
      );

      // Update local state
      setAppointments(appointments.map(apt =>
        apt.id === selectedAppointment.id ? response.data.appointment : apt
      ));

      handleCloseUpdateModal();
    } catch (err) {
      setError('Failed to update appointment. Please try again.');
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

  const upcomingAppointments = appointments.filter(apt =>
    new Date(apt.appointment_date) > new Date() &&
    ['pending', 'confirmed'].includes(apt.status)
  );

  const pastAppointments = appointments.filter(apt =>
    new Date(apt.appointment_date) <= new Date() ||
    apt.status === 'completed'
  );

  const pendingCount = appointments.filter(apt => apt.status === 'pending').length;
  const confirmedCount = appointments.filter(apt => apt.status === 'confirmed').length;

  return (
    <div className="doctor-dashboard-container">
      <header className="doctor-header">
        <div className="doctor-welcome">
          <h1>Doctor's Dashboard</h1>
          <p>{user?.email}</p>
        </div>
        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="stats-section">
        <div className="stat-card">
          <div className="stat-number">{pendingCount}</div>
          <div className="stat-label">Pending Appointments</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{confirmedCount}</div>
          <div className="stat-label">Confirmed Appointments</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{appointments.length}</div>
          <div className="stat-label">Total Appointments</div>
        </div>
      </div>

      {loading ? (
        <div className="loading-message">Loading appointments...</div>
      ) : (
        <>
          {upcomingAppointments.length > 0 && (
            <section className="appointments-section">
              <h2>📅 Upcoming Appointments</h2>
              <div className="appointments-grid">
                {upcomingAppointments.map((appointment) => (
                  <div key={appointment.id} className="appointment-card">
                    <div className="appointment-card-top">
                      <span className={getStatusBadgeClass(appointment.status)}>
                        {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                      </span>
                      <div className="appointment-time">
                        {formatDate(appointment.appointment_date)}
                      </div>
                    </div>

                    <div className="appointment-card-content">
                      <div className="patient-info">
                        <strong>Patient Email:</strong> {appointment.patient_email}
                      </div>
                      {appointment.reason && (
                        <div className="patient-reason">
                          <strong>Reason:</strong> {appointment.reason}
                        </div>
                      )}
                      {appointment.notes && (
                        <div className="doctor-notes">
                          <strong>Notes:</strong> {appointment.notes}
                        </div>
                      )}
                    </div>

                    <div className="appointment-card-footer">
                      <button
                        className="action-btn update-btn"
                        onClick={() => handleOpenUpdateModal(appointment)}
                      >
                        Update Status
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {pastAppointments.length > 0 && (
            <section className="appointments-section past-section">
              <h2>✓ Past Appointments</h2>
              <div className="appointments-grid">
                {pastAppointments.slice(0, 5).map((appointment) => (
                  <div key={appointment.id} className="appointment-card past-card">
                    <div className="appointment-card-top">
                      <span className={getStatusBadgeClass(appointment.status)}>
                        {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                      </span>
                      <div className="appointment-time">
                        {formatDate(appointment.appointment_date)}
                      </div>
                    </div>

                    <div className="appointment-card-content">
                      <div className="patient-info">
                        <strong>Patient Email:</strong> {appointment.patient_email}
                      </div>
                      {appointment.reason && (
                        <div className="patient-reason">
                          <strong>Reason:</strong> {appointment.reason}
                        </div>
                      )}
                      {appointment.notes && (
                        <div className="doctor-notes">
                          <strong>Notes:</strong> {appointment.notes}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {appointments.length === 0 && (
            <div className="no-appointments">
              <p>No appointments booked yet.</p>
            </div>
          )}
        </>
      )}

      {showUpdateModal && selectedAppointment && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Update Appointment</h3>
              <button className="close-btn" onClick={handleCloseUpdateModal}>×</button>
            </div>

            <div className="modal-body">
              <div className="appointment-detail">
                <strong>Patient:</strong> {selectedAppointment.patient_email}
              </div>
              <div className="appointment-detail">
                <strong>Date & Time:</strong> {formatDate(selectedAppointment.appointment_date)}
              </div>
              {selectedAppointment.reason && (
                <div className="appointment-detail">
                  <strong>Reason:</strong> {selectedAppointment.reason}
                </div>
              )}

              <div className="form-group">
                <label htmlFor="status">Status</label>
                <select
                  id="status"
                  value={updateStatus}
                  onChange={(e) => setUpdateStatus(e.target.value)}
                >
                  <option value="pending">Pending</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="notes">Notes for Patient</label>
                <textarea
                  id="notes"
                  value={updateNotes}
                  onChange={(e) => setUpdateNotes(e.target.value)}
                  placeholder="Add any notes or instructions for the patient..."
                  rows="4"
                />
              </div>
            </div>

            <div className="modal-footer">
              <button className="cancel-btn" onClick={handleCloseUpdateModal}>
                Cancel
              </button>
              <button className="save-btn" onClick={handleUpdateAppointment}>
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DoctorDashboard;
