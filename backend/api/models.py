"""
MongoDB models using MongoEngine
"""
from mongoengine import Document, StringField, BooleanField, DateTimeField, DictField, ListField, EmailField
from datetime import datetime
import bcrypt


class User(Document):
    """User document for MongoDB"""
    email = EmailField(unique=True, required=True)
    password_hash = StringField(required=True)
    role = StringField(default='patient', choices=['patient', 'provider', 'admin'])
    consent_given = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)
    
    meta = {
        'collection': 'users',
        'indexes': ['email', 'created_at']
    }
    
    def set_password(self, password: str):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify password"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
        }


class PatientProfile(Document):
    """Patient profile document"""
    user_id = StringField(required=True, unique=True)
    wellness_goals = DictField(default={})
    appointments = ListField(DictField(), default=[])
    health_data = DictField(default={})
    medical_history = ListField(StringField(), default=[])
    allergies = ListField(StringField(), default=[])
    medications = ListField(StringField(), default=[])
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'patient_profiles',
        'indexes': ['user_id', 'created_at']
    }
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'wellness_goals': self.wellness_goals,
            'appointments': self.appointments,
            'health_data': self.health_data,
            'medical_history': self.medical_history,
            'allergies': self.allergies,
            'medications': self.medications,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class ProviderProfile(Document):
    """Provider/Doctor profile document"""
    user_id = StringField(required=True, unique=True)
    specialty = StringField(required=True)
    license_number = StringField(required=True, unique=True)
    qualifications = ListField(StringField(), default=[])
    experience_years = StringField(default='0')
    clinic_address = StringField(default='')
    phone = StringField(default='')
    available_hours = DictField(default={})
    patients = ListField(StringField(), default=[])  # List of patient user_ids
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'provider_profiles',
        'indexes': ['user_id', 'specialty', 'created_at']
    }
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'specialty': self.specialty,
            'license_number': self.license_number,
            'qualifications': self.qualifications,
            'experience_years': self.experience_years,
            'clinic_address': self.clinic_address,
            'phone': self.phone,
            'available_hours': self.available_hours,
            'patients': self.patients,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class Appointment(Document):
    """Appointment booking document"""
    patient_id = StringField(required=True)  # User ID of patient
    provider_id = StringField(required=True)  # User ID of provider/doctor
    appointment_date = DateTimeField(required=True)  # Date and time of appointment
    reason = StringField(default='')  # Reason for appointment
    status = StringField(default='pending', choices=['pending', 'confirmed', 'completed', 'cancelled'])
    notes = StringField(default='')  # Additional notes
    patient_email = StringField(default='')  # Email of patient (for reference)
    provider_email = StringField(default='')  # Email of provider (for reference)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'appointments',
        'indexes': ['patient_id', 'provider_id', 'appointment_date', 'status', 'created_at']
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'patient_id': self.patient_id,
            'provider_id': self.provider_id,
            'appointment_date': self.appointment_date.isoformat(),
            'reason': self.reason,
            'status': self.status,
            'notes': self.notes,
            'patient_email': self.patient_email,
            'provider_email': self.provider_email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
