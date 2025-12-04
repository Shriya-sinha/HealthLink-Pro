"""
Serializers for API requests/responses
"""
from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=['patient', 'provider', 'admin'], default='patient')
    consent_given = serializers.BooleanField(default=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    created_at = serializers.DateTimeField()


class TokenResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    role = serializers.CharField()
    message = serializers.CharField(default='Login successful')


class PatientProfileSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    wellness_goals = serializers.JSONField(required=False)
    appointments = serializers.ListField(required=False)
    health_data = serializers.JSONField(required=False)
    medical_history = serializers.ListField(required=False)
    allergies = serializers.ListField(required=False)
    medications = serializers.ListField(required=False)


class ProviderProfileSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    specialty = serializers.CharField()
    license_number = serializers.CharField()
    qualifications = serializers.ListField(required=False)
    experience_years = serializers.CharField(required=False)
    clinic_address = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    available_hours = serializers.JSONField(required=False)
    patients = serializers.ListField(required=False)


class AppointmentSerializer(serializers.Serializer):
    """Serializer for appointment creation and updates"""
    id = serializers.CharField(required=False)
    patient_id = serializers.CharField()
    provider_id = serializers.CharField()
    appointment_date = serializers.DateTimeField()
    reason = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=['pending', 'confirmed', 'completed', 'cancelled'],
        default='pending',
        required=False
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    patient_email = serializers.EmailField(required=False)
    provider_email = serializers.EmailField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)


class AppointmentCreateSerializer(serializers.Serializer):
    """Simplified serializer for appointment creation by patients"""
    provider_id = serializers.CharField()
    appointment_date = serializers.DateTimeField()
    reason = serializers.CharField(allow_blank=True)


class AppointmentUpdateSerializer(serializers.Serializer):
    """Serializer for appointment status updates"""
    status = serializers.ChoiceField(choices=['pending', 'confirmed', 'completed', 'cancelled'])
    notes = serializers.CharField(required=False, allow_blank=True)
