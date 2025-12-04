"""
URL Configuration for healthcare project.
"""
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'healthcare-api',
        'message': 'Backend is running'
    })

urlpatterns = [
    path('api/health/', health_check, name='health'),
    path('api/auth/', include('api.urls.auth')),
    path('api/patients/', include('api.urls.patients')),
    path('api/providers/', include('api.urls.providers')),
    path('api/appointments/', include('api.urls.appointments')),
]
