from django.urls import path
from .views import registration_view, dashboard_view

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
]