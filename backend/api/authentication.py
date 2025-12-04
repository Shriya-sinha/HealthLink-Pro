"""
JWT Authentication for Django REST Framework
"""
import jwt
import logging
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication class
    """
    keyword = 'Bearer'
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        try:
            auth_type, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')
        
        if auth_type.lower() != self.keyword.lower():
            return None
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get('user_id')
            email = payload.get('email')
            role = payload.get('role')
            
            if not user_id:
                raise AuthenticationFailed('Invalid token')
            
            # Create a simple user object for the request
            class User:
                def __init__(self, user_id, email, role):
                    self.id = user_id
                    self.email = email
                    self.role = role
                    self.is_authenticated = True
            
            user = User(user_id, email, role)
            return (user, token)
        
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            logger.error(f'Invalid token: {str(e)}')
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            logger.error(f'Authentication error: {str(e)}')
            raise AuthenticationFailed('Authentication failed')


def generate_token(user_id: str, email: str, role: str) -> str:
    """
    Generate JWT token
    """
    payload = {
        'user_id': str(user_id),
        'email': email,
        'role': role,
    }
    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return token
