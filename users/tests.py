from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class UserTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(
            id="1",
            first_name="John",
            last_name="Adams",
            password="pythondjango1",
            email="example@gmail.com",
            phone="123",
            address="Bajo California",
            is_superuser=True
        )
        
        cls.group = Group.objects.create(name="Administrator")
        
        cls.refresh = RefreshToken.for_user(cls.user)
        
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()   
        
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f' Bearer {self.refresh.access_token}')
    
    def test_get_user_list(self):
        url = reverse("user-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        
    def test_get_user_detail(self):
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), self.user.first_name)
        
    def test_create_user(self):
        url = reverse("user-list")
     
        data = {
            "id": "25",
            "first_name": "Sabrina",
            "last_name": "Carpenter",
            "password": "californiasong1",
            "email": "sabrina@gmail.com",
            "phone": "567",
            "address": "Pensilvania",
            "groups":[
                1
            ]
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_put_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        
        data = {
            "id": "1",
            "first_name": "John",
            "last_name": "Adams",
            "password": "pythondjango1",
            "email": "example2@gmail.com",
            "phone": "456",
            "address": "Music Row",
            "groups": [
                1
            ]
        }
        
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "example2@gmail.com")
        self.assertEqual(response.data.get("phone"), "456")
        self.assertEqual(response.data.get("address"), "Music Row")
    
    def test_update_patch_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        
        data = {
            "address": "Music Row"
        }
        
        response = self.client.patch(url, data)
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("address"), "Music Row")
        
    def test_delete_user(self):
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        
        response = self.client.delete(url, format="json")
        
        url = reverse("user-detail", kwargs={"pk": self.user.id})

        self.user.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user.is_active)
        
    def test_validate_user_password_bad(self):
        url = reverse("user-list")
        
        data = {
            "id": "25",
            "first_name": "Sabrina",
            "last_name": "Carpenter",
            "password": "sabrina",
            "email": "sabrina@gmail.com",
            "phone": "567",
            "address": "Pensilvania",
            "groups":[
                1
            ]
        }
       
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "1 - John Adams")
        
        
        
        
        
        
        