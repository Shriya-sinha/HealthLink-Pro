"""
Appointment URLs
"""
from django.urls import path
from api.views.appointments import (
    AppointmentListView,
    AppointmentCreateView,
    AppointmentDetailView,
    DoctorAppointmentsView,
)

urlpatterns = [
    path('', AppointmentListView.as_view(), name='appointment-list'),
    path('create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('<str:appointment_id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('doctor/<str:doctor_id>/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
]
