"""
Patient views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import logging
from api.models import PatientProfile, User

logger = logging.getLogger(__name__)


class PatientListView(APIView):
    """List all patients (provider only)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = User.objects(id=request.user.id).first()
            
            # Only providers and admins can view patients
            if user.role not in ['provider', 'admin']:
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            patients = PatientProfile.objects()
            patients_data = [p.to_dict() for p in patients]
            
            return Response(
                {'patients': patients_data, 'count': len(patients_data)},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Patient list error: {str(e)}')
            return Response(
                {'error': 'Failed to fetch patients'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientDetailView(APIView):
    """Get patient details"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, patient_id):
        try:
            user = User.objects(id=request.user.id).first()
            
            patient = PatientProfile.objects(user_id=patient_id).first()
            
            if not patient:
                return Response(
                    {'error': 'Patient not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Users can only view their own data unless they're admin
            if str(request.user.id) != patient_id and user.role != 'admin':
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return Response(
                patient.to_dict(),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Patient detail error: {str(e)}')
            return Response(
                {'error': 'Failed to fetch patient'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientUpdateView(APIView):
    """Update patient profile"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, patient_id):
        try:
            user = User.objects(id=request.user.id).first()
            
            # Users can only update their own data unless they're admin
            if str(request.user.id) != patient_id and user.role != 'admin':
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            patient = PatientProfile.objects(user_id=patient_id).first()
            
            if not patient:
                return Response(
                    {'error': 'Patient not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Update fields
            if 'wellness_goals' in request.data:
                patient.wellness_goals = request.data['wellness_goals']
            if 'health_data' in request.data:
                patient.health_data = request.data['health_data']
            if 'medical_history' in request.data:
                patient.medical_history = request.data['medical_history']
            if 'allergies' in request.data:
                patient.allergies = request.data['allergies']
            if 'medications' in request.data:
                patient.medications = request.data['medications']
            
            patient.save()
            
            return Response(
                patient.to_dict(),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Patient update error: {str(e)}')
            return Response(
                {'error': 'Failed to update patient'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
