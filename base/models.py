import uuid
import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from mapbox_location_field.models import LocationField, AddressAutoHiddenField


class Map(models.Model):
    location = LocationField(null=True, blank=True,
        map_attrs={"style": "mapbox://styles/mightysharky/cjwgnjzr004bu1dnpw8kzxa72", "center": (28.154, -25.7484)})
    address = AddressAutoHiddenField(null=True, blank=True)
    
    def __str__(self):
        return self.location


class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=MALE)
    title = models.CharField(max_length=30)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    dob = models.DateTimeField(blank=True)
    age = models.CharField(max_length=10)
    phone = models.CharField(max_length=13)
    cell = models.CharField(max_length=13)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.first_name)

    class Meta:
        ordering = ('-created',)

class Location(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_location')
    address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=30)
    offset = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    lat = models.CharField(max_length=100, blank=True, null=True)
    lon = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.owner.username}'s address"
    

    def save(self, *args, **kwargs):
        my_tz = timezone.get_default_timezone()
        date = timezone.make_aware(datetime.datetime.now(), my_tz)
        if self.offset == "" and self.description == "":
            self.offset = date.utcoffset()
            self.description = date.tzinfo()
        return super().save(*args, **kwargs)

# id
class ID(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_id', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    value = models.CharField(max_length=100, blank=True, null=True)


# Pictures
class Avatar(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_pictures', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='avatars/thumbnail', blank=True, default='profile1.png')
    medium = models.ImageField(upload_to='avatars/medium', blank=True, default='profile1.png')
    large = models.ImageField(upload_to='avatars/large', blank=True, default='profile1.png')
    nat = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.owner.username}\'s images'