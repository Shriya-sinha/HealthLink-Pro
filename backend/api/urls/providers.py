"""
Provider URLs
"""
from django.urls import path
from api.views.providers import (
    ProviderListView, ProviderDetailView, ProviderCreateView, ProviderUpdateView
)

urlpatterns = [
    path('', ProviderListView.as_view(), name='provider-list'),
    path('create/', ProviderCreateView.as_view(), name='provider-create'),
    path('<str:provider_id>/', ProviderDetailView.as_view(), name='provider-detail'),
    path('<str:provider_id>/update/', ProviderUpdateView.as_view(), name='provider-update'),
]
