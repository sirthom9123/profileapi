from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # Root Routes
    path('', views.profile_view, name='profile'),
    path('profile_form/', views.profile_form, name='profile_form'),
]
