import uuid
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from ..models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class CustomRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
    
        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain Alphanumeric characters')
        return attrs



class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('key', 'user')

    def get_user_type(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        username = serializer_data.get('username')
        return {
            'username': username,
        }



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = (
            'url',
            'pk',
            'owner',
            'gender', 
            'title',  
            'first_name',
            'last_name',
            'dob', 
            'age', 
            'phone', 
            'cell', 
            )



class LocationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    coordinate = serializers.HyperlinkedRelatedField(read_only=True, view_name='coordinates-detail')

    class Meta:
        model = Location
        fields = (
            'url',
            'pk',
            'address', 
            'city', 
            'state', 
            'country', 
            'postal_code', 
            'offset', 
            'desription',
            'lat', 
            'lon',
            'owner', 
            )



class IdSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = ID
        fields = ('url', 'pk', 'owner', 'name', 'value',)

class AvatarSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Avatar
        fields = ('url', 'pk', 'owner', 'thumbnail', 'medium', 'large', 'nat',)

