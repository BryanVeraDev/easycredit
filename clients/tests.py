from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class ClientTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
    
        cls.user = get_user_model().objects.create_superuser(
        email="test@example.com", password="testpassword"
        )
        
        cls.client_test = Client.objects.create(
            id="1",
            first_name="Olivia",
            last_name="Rodrigo",
            email="isa@gmail.com",
            phone="123",
            address="Murrieta"
        )
        
        cls.refresh = RefreshToken.for_user(cls.user)
        
    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.client_test.delete()   
        
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f' Bearer {self.refresh.access_token}')
        
    def test_get_client_list(self):
        url = reverse("client-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        
    def test_get_client_detail(self):
        url = reverse("client-detail", kwargs={"pk": self.client_test.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("first_name"), self.client_test.first_name)
        
    def test_create_client(self):
        url = reverse("client-list")
     
        data = {
            "id": "25",
            "first_name": "Sabrina",
            "last_name": "Carpenter",
            "email": "sabrina@gmail.com",
            "phone": "567",
            "address": "Pensilvania"
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update_put_client(self):
        url = reverse("client-detail", kwargs={"pk": self.client_test.id})
        
        data = {
            "id": "1",
            "first_name": "Olivia",
            "last_name": "Rodrigo",
            "email": "liv@gmail.com",
            "phone": "456",
            "address": "California"
        }
        
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("email"), "liv@gmail.com")
        self.assertEqual(response.data.get("phone"), "456")
        self.assertEqual(response.data.get("address"), "California")
        
    def test_update_patch_client(self):
        url = reverse("client-detail", kwargs={"pk": self.client_test.id})
        
        data = {
            "address": "California"
        }
        
        response = self.client.patch(url, data)
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("address"), "California")
        
    def test_delete_client(self):
        url = reverse("client-detail", kwargs={"pk": self.client_test.id})
        
        response = self.client.delete(url, format="json")
        
        self.client_test.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.client_test.is_active)
        
    def test_user_string_representation(self):
        self.assertEqual(str(self.client_test), "1 - Olivia Rodrigo")
    
        