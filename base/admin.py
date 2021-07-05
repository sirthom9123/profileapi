from django.contrib import admin
from mapbox_location_field.admin import MapAdmin 

from .models import *

admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Avatar)
admin.site.register(Map, MapAdmin)