from django.urls import path
from .views import admin_dashboard, register, login,create_member


urlpatterns = [
    path('auth/register/', register),
    path('auth/login/', login),
    path('auth/create-member/', create_member),
    path('auth/dashboard/', admin_dashboard),
]
