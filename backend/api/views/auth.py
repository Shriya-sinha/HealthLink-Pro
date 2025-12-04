"""
Authentication views
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
import logging
from api.models import User, PatientProfile, ProviderProfile
from api.serializers import RegisterSerializer, LoginSerializer, TokenResponseSerializer
from api.authentication import generate_token
from mongoengine.errors import NotUniqueError

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    """User registration endpoint - patients only"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Only allow patient registration
            role = serializer.validated_data.get('role', 'patient')
            if role != 'patient':
                return Response(
                    {'error': 'Only patients can register. Doctors are pre-loaded in the system.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if user already exists
            if User.objects(email=serializer.validated_data['email']):
                return Response(
                    {'error': 'Email already registered'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create new user
            user = User(
                email=serializer.validated_data['email'],
                role='patient',
                consent_given=serializer.validated_data.get('consent_given', False)
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            
            # Create profile based on role
            if user.role == 'patient':
                PatientProfile(user_id=str(user.id)).save()
            elif user.role == 'provider':
                ProviderProfile(user_id=str(user.id), specialty='', license_number='').save()
            
            return Response(
                {'message': 'User registered successfully', 'user': user.to_dict()},
                status=status.HTTP_201_CREATED
            )
        
        except NotUniqueError:
            return Response(
                {'error': 'Email already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f'Registration error: {str(e)}')
            return Response(
                {'error': 'Registration failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    """User login endpoint"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Find user
            user = User.objects(email=email).first()
            
            if not user or not user.check_password(password):
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.is_active:
                return Response(
                    {'error': 'User account is inactive'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Generate token
            token = generate_token(str(user.id), user.email, user.role)
            
            response_serializer = TokenResponseSerializer({
                'token': token,
                'role': user.role,
                'message': 'Login successful'
            })
            
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f'Login error: {str(e)}')
            return Response(
                {'error': 'Login failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    """User logout endpoint"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
        )


class ProfileView(APIView):
    """Get current user profile"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = User.objects(id=request.user.id).first()
            
            if not user:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(
                user.to_dict(),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Profile fetch error: {str(e)}')
            return Response(
                {'error': 'Failed to fetch profile'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
