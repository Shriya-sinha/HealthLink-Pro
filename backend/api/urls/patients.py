"""
Patient URLs
"""
from django.urls import path
from api.views.patients import (
    PatientListView, PatientDetailView, PatientUpdateView
)

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('<str:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),
    path('<str:patient_id>/update/', PatientUpdateView.as_view(), name='patient-update'),
]
