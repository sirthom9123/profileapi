import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, status, views, permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import Token
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth.models import User

from .serializers import *
from ..models import *
from .permission import IsCurrentUserOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ProfileListAPIView(generics.ListCreateAPIView):
    throttle_scope = 'profile'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'
    ordering_fields = ('last_name',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCurrentUserOwnerOrReadOnly)


class LocationListAPIView(generics.ListCreateAPIView):
    throttle_scope = 'location'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    name = 'location'
    search_fields = ('city', 'state', 'country')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LocationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    name = 'location-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCurrentUserOwnerOrReadOnly, )

class AvatarListAPIView(generics.ListCreateAPIView):
    throttle_scope = 'avatar'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    name = 'avatars'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AvatarDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    name = 'avatar-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCurrentUserOwnerOrReadOnly)



class IDListAPIView(generics.ListCreateAPIView):
    throttle_scope = 'id'
    throttle_classes = (ScopedRateThrottle,)
    queryset = ID.objects.all()
    serializer_class = IdSerializer
    name = 'id-list'
    ordering_fields = ('name',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class IDDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ID.objects.all()
    serializer_class = IdSerializer
    name = 'id-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCurrentUserOwnerOrReadOnly)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'profile-list': reverse(ProfileListAPIView.name, request=request),
            'location': reverse(LocationListAPIView.name, request=request),
            'avatars': reverse(AvatarListAPIView.name, request=request),
            'id-list': reverse(IDListAPIView.name, request=request),
            })



