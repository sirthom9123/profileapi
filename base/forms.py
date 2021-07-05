from django import forms
from django.forms import widgets

from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'gender', 
            'title',  
            'first_name',
            'last_name',
            'dob', 
            'age', 
            'phone', 
            'cell',
            )

        widgets = {
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
"""
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('owner', 'lat', 'lon', 'offset', 'description')
"""


class LocationForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = '__all__'
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control js-mapbox-input-location-field'}),
        }
        labels = {'location': ''}



class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        exclude = ('owner', 'nat')