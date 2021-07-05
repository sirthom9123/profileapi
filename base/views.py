from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.utils import timezone

from .models import *
from .forms import AvatarForm, LocationForm, ProfileForm


# profile view
@login_required(login_url='login')
def profile_view(request):
    user_obj = request.user
    
    profile = None
    location = None
    avatar = None
    if user_obj:
        profile = Profile.objects.get(owner=user_obj)
        location = Location.objects.get(owner=user_obj)
        avatar = Avatar.objects.get(owner=user_obj)
        
    profile_form = ProfileForm()
    location_form = LocationForm()
    avatar_form = AvatarForm()


    context = {
        'profile': profile, 
        'location': location,
        'avatar': avatar,
        'profile_form': profile_form, 
        'location_form': location_form,
        'avatar_form': avatar_form,
        'user_obj': user_obj,
        }
    return render(request, 'base/profile.html', context)

def profile_form(request):
    user_obj = request.user
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_obj)
        location_form = LocationForm(request.POST, instance=user_obj)
        avatar_form = AvatarForm(request.POST, request.FILES, instance=user_obj)
        if profile_form.is_valid() and location_form.is_valid() and avatar_form.is_valid():
            prof_instance = profile_form.save(commit=False)
            prof_instance.owner = user_obj
            prof_instance.save()
            pic_instance = avatar_form.save(commit=False)
            pic_instance.owner = user_obj
            pic_instance.save()
            # save address, lat and lon coordinates dynamically from mapbox  
            text = location_form.cleaned_data['location'].split(',')
            data = location_form.cleaned_data['address'].split(',')
            lat = text[1]
            lon = text[0]
            address = data[0]
            city = data[1]
            # state_data = data[2].lstrip().split(',')
            state = data[2]
            country = data[3]
            Location.objects.create(
                                    owner=user_obj,
                                    address=address,
                                    city=city,
                                    state=state,
                                    country=country,
                                    postal_code=state,                                                
                                    lat=lat,
                                    lon=lon,
                                    )   
            messages.success(request, 'Your profile has been created')
            return redirect('profile')
        else: 
            messages.error(request, 'Something went wrong')
            return redirect('profile')
    else:
        return redirect('profile')
