"""
Appointment management views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import logging
from datetime import datetime
from django.utils import timezone
from api.models import Appointment, User, ProviderProfile, PatientProfile
from api.serializers import AppointmentSerializer, AppointmentCreateSerializer, AppointmentUpdateSerializer

logger = logging.getLogger(__name__)


class AppointmentListView(APIView):
    """Get appointments - patients see their appointments, doctors see their booked appointments"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = User.objects(id=request.user.id).first()
            
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Patients see their own appointments
            if user.role == 'patient':
                appointments = Appointment.objects(patient_id=str(user.id))
                appointments_data = [apt.to_dict() for apt in appointments]
                return Response(
                    {'appointments': appointments_data},
                    status=status.HTTP_200_OK
                )
            
            # Doctors/providers see appointments booked with them
            elif user.role == 'provider':
                appointments = Appointment.objects(provider_id=str(user.id))
                appointments_data = [apt.to_dict() for apt in appointments]
                return Response(
                    {'appointments': appointments_data},
                    status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {'error': 'Insufficient permissions'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        except Exception as e:
            logger.error(f'Error fetching appointments: {str(e)}')
            return Response(
                {'error': 'Failed to fetch appointments'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentCreateView(APIView):
    """Create new appointment (patients only)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user = User.objects(id=request.user.id).first()
            
            if not user or user.role != 'patient':
                return Response(
                    {'error': 'Only patients can book appointments'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = AppointmentCreateSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'error': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate appointment date is in the future
            apt_date = serializer.validated_data['appointment_date']
            if apt_date < timezone.now():
                return Response(
                    {'error': 'Appointment date must be in the future'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get provider
            provider = User.objects(id=serializer.validated_data['provider_id']).first()
            if not provider or provider.role != 'provider':
                return Response(
                    {'error': 'Provider not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Check for duplicate appointments (same patient, doctor, time)
            existing_apt = Appointment.objects(
                patient_id=str(user.id),
                provider_id=str(provider.id),
                appointment_date=apt_date,
                status__in=['pending', 'confirmed']
            ).first()
            
            if existing_apt:
                return Response(
                    {'error': 'You already have an appointment at this time with this doctor'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create appointment
            appointment = Appointment(
                patient_id=str(user.id),
                provider_id=str(provider.id),
                appointment_date=apt_date,
                reason=serializer.validated_data.get('reason', ''),
                status='pending',
                patient_email=user.email,
                provider_email=provider.email,
            )
            appointment.save()
            
            # Add patient to provider's patient list if not already there
            provider_profile = ProviderProfile.objects(user_id=str(provider.id)).first()
            if provider_profile and str(user.id) not in provider_profile.patients:
                provider_profile.patients.append(str(user.id))
                provider_profile.save()
            
            return Response(
                {
                    'message': 'Appointment booked successfully',
                    'appointment': appointment.to_dict()
                },
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            logger.error(f'Error creating appointment: {str(e)}')
            return Response(
                {'error': 'Failed to create appointment'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentDetailView(APIView):
    """Get, update, or cancel appointment"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, appointment_id):
        try:
            appointment = Appointment.objects(id=appointment_id).first()
            
            if not appointment:
                return Response(
                    {'error': 'Appointment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            user = User.objects(id=request.user.id).first()
            
            # Check if user is authorized to view this appointment
            if user.role == 'patient' and appointment.patient_id != str(user.id):
                return Response(
                    {'error': 'Not authorized to view this appointment'},
                    status=status.HTTP_403_FORBIDDEN
                )
            elif user.role == 'provider' and appointment.provider_id != str(user.id):
                return Response(
                    {'error': 'Not authorized to view this appointment'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return Response(
                {'appointment': appointment.to_dict()},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f'Error fetching appointment: {str(e)}')
            return Response(
                {'error': 'Failed to fetch appointment'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, appointment_id):
        """Update appointment status (doctors can confirm/complete/cancel)"""
        try:
            appointment = Appointment.objects(id=appointment_id).first()
            
            if not appointment:
                return Response(
                    {'error': 'Appointment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            user = User.objects(id=request.user.id).first()
            
            # Only provider can update appointment
            if user.role != 'provider' or appointment.provider_id != str(user.id):
                return Response(
                    {'error': 'Only the doctor can update this appointment'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = AppointmentUpdateSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'error': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            appointment.status = serializer.validated_data['status']
            if 'notes' in serializer.validated_data:
                appointment.notes = serializer.validated_data['notes']
            appointment.updated_at = timezone.now()
            appointment.save()
            
            return Response(
                {
                    'message': f'Appointment status updated to {appointment.status}',
                    'appointment': appointment.to_dict()
                },
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f'Error updating appointment: {str(e)}')
            return Response(
                {'error': 'Failed to update appointment'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, appointment_id):
        """Cancel appointment (patient or doctor can cancel)"""
        try:
            appointment = Appointment.objects(id=appointment_id).first()
            
            if not appointment:
                return Response(
                    {'error': 'Appointment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            user = User.objects(id=request.user.id).first()
            
            # Check authorization
            if user.role == 'patient' and appointment.patient_id != str(user.id):
                return Response(
                    {'error': 'Not authorized to cancel this appointment'},
                    status=status.HTTP_403_FORBIDDEN
                )
            elif user.role == 'provider' and appointment.provider_id != str(user.id):
                return Response(
                    {'error': 'Not authorized to cancel this appointment'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Cancel instead of delete
            appointment.status = 'cancelled'
            appointment.updated_at = timezone.now()
            appointment.save()
            
            return Response(
                {'message': 'Appointment cancelled successfully'},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f'Error cancelling appointment: {str(e)}')
            return Response(
                {'error': 'Failed to cancel appointment'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DoctorAppointmentsView(APIView):
    """Get all appointments for a specific doctor (public endpoint)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, doctor_id):
        """Get available time slots and appointments for a doctor"""
        try:
            doctor = User.objects(id=doctor_id).first()
            
            if not doctor or doctor.role != 'provider':
                return Response(
                    {'error': 'Doctor not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get appointments with confirmed or pending status
            appointments = Appointment.objects(
                provider_id=str(doctor.id),
                status__in=['pending', 'confirmed']
            )
            
            doctor_profile = ProviderProfile.objects(user_id=str(doctor.id)).first()
            
            return Response(
                {
                    'doctor': {
                        'id': str(doctor.id),
                        'email': doctor.email,
                        'specialty': doctor_profile.specialty if doctor_profile else '',
                        'clinic_address': doctor_profile.clinic_address if doctor_profile else '',
                        'available_hours': doctor_profile.available_hours if doctor_profile else {},
                    },
                    'appointments': [apt.to_dict() for apt in appointments],
                    'booked_count': appointments.count(),
                },
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f'Error fetching doctor appointments: {str(e)}')
            return Response(
                {'error': 'Failed to fetch doctor appointments'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
