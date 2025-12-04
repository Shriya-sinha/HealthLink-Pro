// src/components/AppointmentBooking.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import './AppointmentBooking.css';

function AppointmentBooking({ onBackToDashboard }) {
  const { user } = useAuth();
  const [doctors, setDoctors] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState('');
  const [appointmentDate, setAppointmentDate] = useState('');
  const [appointmentTime, setAppointmentTime] = useState('');
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [doctorDetails, setDoctorDetails] = useState(null);

  // Fetch all doctors on component mount
  useEffect(() => {
    fetchDoctors();
  }, []);

  const fetchDoctors = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/providers/');
      setDoctors(response.data.providers || []);
      setError('');
    } catch (err) {
      setError('Failed to fetch doctors. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDoctorSelect = async (doctorId) => {
    setSelectedDoctor(doctorId);
    setDoctorDetails(null);
    
    // Fetch doctor details and their appointments
    try {
      const response = await axios.get(`/api/appointments/doctor/${doctorId}/`);
      setDoctorDetails(response.data.doctor);
    } catch (err) {
      console.error('Failed to fetch doctor details:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedDoctor || !appointmentDate || !appointmentTime) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Combine date and time
      const dateTime = `${appointmentDate}T${appointmentTime}:00Z`;
      
      const response = await axios.post('/api/appointments/create/', {
        provider_id: selectedDoctor,
        appointment_date: dateTime,
        reason: reason || '',
      });

      setSuccess('Appointment booked successfully! The doctor will confirm your appointment shortly.');
      
      // Reset form
      setSelectedDoctor('');
      setAppointmentDate('');
      setAppointmentTime('');
      setReason('');
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to book appointment. Please try again.';
      setError(errorMsg);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Get minimum date (today)
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="appointment-booking-container">
      <div className="booking-header">
        <h2>Book an Appointment</h2>
        <button className="back-btn" onClick={onBackToDashboard}>
          ← Back to Dashboard
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <form onSubmit={handleSubmit} className="booking-form">
        <div className="form-group">
          <label htmlFor="doctor">Select Doctor *</label>
          <select
            id="doctor"
            value={selectedDoctor}
            onChange={(e) => handleDoctorSelect(e.target.value)}
            disabled={loading}
            required
          >
            <option value="">Choose a doctor...</option>
            {doctors.map((doctor) => (
              <option key={doctor.user_id} value={doctor.user_id}>
                {doctor.specialty} - {doctor.clinic_address || 'Location not specified'}
              </option>
            ))}
          </select>
        </div>

        {doctorDetails && (
          <div className="doctor-details-card">
            <h3>Doctor Information</h3>
            <p><strong>Specialty:</strong> {doctorDetails.specialty}</p>
            <p><strong>Location:</strong> {doctorDetails.clinic_address}</p>
            <p><strong>Available Hours:</strong></p>
            <ul>
              {Object.entries(doctorDetails.available_hours || {}).map(([day, hours]) => (
                <li key={day}>{day}: {hours}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="form-group">
          <label htmlFor="date">Appointment Date *</label>
          <input
            type="date"
            id="date"
            value={appointmentDate}
            onChange={(e) => setAppointmentDate(e.target.value)}
            min={today}
            disabled={loading || !selectedDoctor}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="time">Appointment Time *</label>
          <input
            type="time"
            id="time"
            value={appointmentTime}
            onChange={(e) => setAppointmentTime(e.target.value)}
            disabled={loading || !selectedDoctor}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="reason">Reason for Visit</label>
          <textarea
            id="reason"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Describe your reason for visit (optional)"
            rows="4"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !selectedDoctor}
          className="submit-btn"
        >
          {loading ? 'Booking...' : 'Book Appointment'}
        </button>
      </form>
    </div>
  );
}

export default AppointmentBooking;
