from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Profile, Location
from . import views



class ProfileTests(APITestCase):
    def post_profile(self, gender, title, first_name, last_name, dob, age, phone, cell):
        url = reverse('profile-list')
        print(url)
        data = {
            'gender': gender,
            'title': title,
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'age': age,
            'phone': phone,
            'cell': cell
        }
        response = self.client.post(url, data, format='json')
        return response

    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user('user01', 'user01@test.com', 'userPassowrid03')
        user.is_verified = True
        user.save()
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token.key))
        return user
        
    # Create a profile for an authorized user
    def test_post_and_get_profile(self):
        self.create_user_and_set_token_credentials()
        
        new_profile_gender = Profile.FEMALE
        new_profile_title = 'Ms'
        new_profile_first_name = 'Susan'
        new_profile_last_name = 'Doe'
        new_profile_dob = '1900-03-22T22:43:00+02:00'
        new_profile_age = '100'
        new_profile_phone = '00000000000'
        new_profile_cell = '000000000'

        response = self.post_profile(
            new_profile_gender, 
            new_profile_title, 
            new_profile_first_name, 
            new_profile_last_name, 
            new_profile_dob, 
            new_profile_age, 
            new_profile_phone, 
            new_profile_cell
        )
        import pdb ; pdb.set_trace()

        assert response.status_code == status.HTTP_201_CREATED
        assert Profile.objects.count() == 1
        saved_profile = Profile.objects.get()
        assert saved_profile.gender == new_profile_gender
        assert saved_profile.title == new_profile_title
        assert saved_profile.first_name == new_profile_first_name
        assert saved_profile.last_name == new_profile_last_name
        assert saved_profile.dob == new_profile_dob
        assert saved_profile.age == new_profile_age
        assert saved_profile.phone == new_profile_phone
        assert saved_profile.cell == new_profile_cell

        url = reverse('profile-detail', None, {saved_profile.pk})
        authorized_get_response = self.client.get(url, format='json')
        assert authorized_get_response.status_code == status.status.HTTP_200_OK
        assert authorized_get_response.data['first_name'] == new_profile_first_name

        # Cleanup credentials
        self.client.credentials()
        unauthorized_get_response = self.client.get(url, format='json')
        assert unauthorized_get_response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # Ensure we can't create a pilot without a token
    def test_post_profile_without_token(self):
        new_profile_title = 'Madame'
        new_profile_gender = Profile.FEMALE
        new_profile_first_name = 'Susan'
        new_profile_last_name = 'Doe'
        new_profile_dob = '1900-03-22T22:43:00+02:00'
        new_profile_age = '100'
        new_profile_phone = '00000000000'
        new_profile_cell = '000000000'
        response = self.post_profile(
            new_profile_gender, 
            new_profile_title, 
            new_profile_first_name, 
            new_profile_last_name, 
            new_profile_dob, 
            new_profile_age, 
            new_profile_phone, 
            new_profile_cell
        )
        print(response)
        print(Profile.objects.count())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Profile.objects.count() == 0