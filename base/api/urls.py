from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
urlpatterns = router.urls

urlpatterns = [
    # Root Routes
    path('', views.ApiRoot.as_view(), name='home'),

    path('profile/', views.ProfileListAPIView.as_view(), name='profile-list'),
    path('profile/<pk>/', views.ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('location/', views.LocationListAPIView.as_view(), name='location'),
    path('location/<pk>/', views.LocationDetailAPIView.as_view(), name='location-detail'),
    path('avatars/', views.AvatarListAPIView.as_view(), name='avatars'),
    path('avatars/<pk>/', views.AvatarDetailAPIView.as_view(), name='avatar-detail'),
    path('id/', views.IDListAPIView.as_view(), name='id-list'),
    path('id/<pk>/', views.IDDetailAPIView.as_view(), name='id-detail'),
]
