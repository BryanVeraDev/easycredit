from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product, ProductType
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class ProductTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        user_class = get_user_model()
        cls.user = get_user_model().objects.create_superuser(
        email="test@example.com", password="testpassword"
        )
        
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)
        
        cls.product_type = ProductType.objects.create(description="Electronics")
        
        cls.product = Product.objects.create(
            name="High-Power Blender",
            description="1000W blender, perfect for quickly preparing juices, smoothies, and shakes. It features multiple speed settings and an ergonomic design for easy use and cleaning.",
            price=59999.99,
            is_active=True,
            product_type=cls.product_type
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.product_type.delete()
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_user_str(self):
        """Prueba para el método __str__ de User"""
        expected_str = f'{self.user.id} - {self.user.first_name} {self.user.last_name}'
        self.assertEqual(str(self.user), expected_str)
        
    def test_product_str(self):
        """Prueba para el método __str__ de Product"""
        expected_str = "High-Power Blender"
        self.assertEqual(str(self.product), expected_str)

    def test_product_type_str(self):
        """Prueba para el método __str__ de ProductType"""
        expected_str = "Electronics"
        self.assertEqual(str(self.product_type), expected_str)

    def test_get_product_list(self):
        url = reverse("product-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_product_detail(self):
        url = reverse("product-detail", kwargs={"pk": self.product.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_create_product(self):
        url = reverse("product-list")
        data = {
            "name": "New Product",
            "description": "New Description",
            "price": 199.99,
            "is_active": True,
            "product_type": self.product_type.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_update_product(self):
        url = reverse("product-detail", kwargs={"pk": self.product.id})
        data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 149.99,
            "is_active": False,
            "product_type": self.product_type.id
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_partial_update_product(self):
        url = reverse("product-detail", kwargs={"pk": self.product.id})
        data = {"price": 89.99}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], str(data["price"]))

    def test_delete_product(self):
        url = reverse("product-detail", kwargs={"pk": self.product.id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)