from django.urls import path
from . import views

urlpatterns = [
    path('admin/dashboard/', views.dashboard, name='admin_dashboard'),
]
