"""
Provider views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import logging
from api.models import ProviderProfile, User

logger = logging.getLogger(__name__)


class ProviderListView(APIView):
    """List all providers"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            providers = ProviderProfile.objects()
            providers_data = [p.to_dict() for p in providers]
            
            return Response(
                {'providers': providers_data, 'count': len(providers_data)},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Provider list error: {str(e)}')
            return Response(
                {'error': 'Failed to fetch providers'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProviderDetailView(APIView):
    """Get provider details"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, provider_id):
        try:
            provider = ProviderProfile.objects(user_id=provider_id).first()
            
            if not provider:
                return Response(
                    {'error': 'Provider not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(
                provider.to_dict(),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Provider detail error: {str(e)}')
            return Response(
                {'error': 'Failed to fetch provider'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProviderCreateView(APIView):
    """Create provider profile"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            user = User.objects(id=request.user.id).first()
            
            # Only admins can create provider profiles for others
            if str(request.user.id) != request.data.get('user_id') and user.role != 'admin':
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if provider already exists
            if ProviderProfile.objects(user_id=request.data['user_id']):
                return Response(
                    {'error': 'Provider profile already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            provider = ProviderProfile(
                user_id=request.data['user_id'],
                specialty=request.data.get('specialty', ''),
                license_number=request.data.get('license_number', ''),
                qualifications=request.data.get('qualifications', []),
                experience_years=request.data.get('experience_years', '0'),
                clinic_address=request.data.get('clinic_address', ''),
                phone=request.data.get('phone', ''),
            )
            provider.save()
            
            return Response(
                provider.to_dict(),
                status=status.HTTP_201_CREATED
            )
        except KeyError as e:
            return Response(
                {'error': f'Missing required field: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f'Provider create error: {str(e)}')
            return Response(
                {'error': 'Failed to create provider'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProviderUpdateView(APIView):
    """Update provider profile"""
    permission_classes = [IsAuthenticated]
    
    def put(self, request, provider_id):
        try:
            user = User.objects(id=request.user.id).first()
            
            # Users can only update their own data unless they're admin
            if str(request.user.id) != provider_id and user.role != 'admin':
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            provider = ProviderProfile.objects(user_id=provider_id).first()
            
            if not provider:
                return Response(
                    {'error': 'Provider not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Update fields
            if 'specialty' in request.data:
                provider.specialty = request.data['specialty']
            if 'license_number' in request.data:
                provider.license_number = request.data['license_number']
            if 'qualifications' in request.data:
                provider.qualifications = request.data['qualifications']
            if 'experience_years' in request.data:
                provider.experience_years = request.data['experience_years']
            if 'clinic_address' in request.data:
                provider.clinic_address = request.data['clinic_address']
            if 'phone' in request.data:
                provider.phone = request.data['phone']
            if 'available_hours' in request.data:
                provider.available_hours = request.data['available_hours']
            
            provider.save()
            
            return Response(
                provider.to_dict(),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Provider update error: {str(e)}')
            return Response(
                {'error': 'Failed to update provider'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
