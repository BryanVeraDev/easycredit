from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from .models import Credit, Client, ClientCreditProduct, Payment, InterestRate
from products.models import Product, ProductType 
from clients.models import Client 
from users.models import User
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken

class CreditTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            id="1090147891",
            first_name="John",
            last_name="Adams",
            password="pythondjango1",
            email="example1@gmail.com",
            phone="123",
            address="Bajo California",
            is_superuser=True
        )

        cls.group, created = Group.objects.get_or_create(name="Administrator")
        
        cls.refresh = RefreshToken.for_user(cls.user)

        cls.client_user = Client.objects.create(
            id="123456789012",
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            phone="123456789",
            address="Main Street 1"
        )
        
        cls.interest_rate = InterestRate.objects.create(
            percentage=5.5,
        )
        
        cls.product_type = ProductType.objects.create(
            description="Electronics"
        )
        
        cls.product1 = Product.objects.create(
            name="Product 1",
            description="Science fiction",
            price=Decimal("100.00"),
            product_type=cls.product_type
        )

        cls.product2 = Product.objects.create(
            name="Product 2",
            description="Sooner or later",
            price=Decimal("100.00"),
            product_type=cls.product_type
        )
        

        cls.credit_data = {
            "description": "Crédito Prueba",
            "total_amount": Decimal("0.00"),
            "no_installment": 12,
            "penalty_rate": Decimal("2.5"),
            "interest_rate": cls.interest_rate,
            "client": cls.client_user,
            "products": [
                {"id_product": cls.product1.id, "quantity": 2},
                {"id_product": cls.product2.id, "quantity": 1}
            ]
        }

        cls.credit = Credit.objects.create(
            description=cls.credit_data["description"],
            total_amount=cls.credit_data["total_amount"],
            no_installment=cls.credit_data["no_installment"],
            penalty_rate=cls.credit_data["penalty_rate"],
            interest_rate=cls.credit_data["interest_rate"],
            client=cls.credit_data["client"]
        )

        for product_data in cls.credit_data["products"]:
            product = Product.objects.get(id=product_data["id_product"])
            ClientCreditProduct.objects.create(
                id_credit=cls.credit,
                id_product=product,
                quantity=product_data["quantity"]
            )

    
    @classmethod
    def tearDownClass(cls):
        ClientCreditProduct.objects.filter(id_credit=cls.credit).delete()
        Credit.objects.filter(client=cls.client_user).delete()
        cls.group.delete()
        cls.user.delete()
        cls.client_user.delete()       
        cls.interest_rate.delete()
        cls.product1.delete()
        cls.product2.delete()
        cls.product_type.delete()
        cls.credit.delete()
        super().tearDownClass()
    
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f' Bearer {self.refresh.access_token}')
        self.url_template = reverse("credit-list") + "clients/{}/"

    #Test for Credit
    def test_calculate_total_amount(self):
        total_amount = self.credit.calculate_total_amount()
        self.assertEqual(total_amount, Decimal("300.00"))

    def test_validate_penalty_rate_positive(self):
        credit = Credit.objects.create(
                description="Crédito Negativo",
                total_amount="1000.00",
                no_installment=12,
                penalty_rate="-1.0",
                interest_rate=self.interest_rate,
                client=self.client_user
        )

        with self.assertRaises(ValidationError):
            credit.full_clean()
    
    def test_get_credit_list(self):
        url = reverse("credit-list")
        
        response = self.client.get(url, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)
        
    def test_get_credit_detail(self):
        url = reverse("credit-detail", kwargs={"pk": self.credit.id})
        
        response = self.client.get(url, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("description"), "Crédito Prueba")
        
    def test_get_credit_detail_valid_client(self):
        url = self.url_template.format(self.client_user.id)
        
        response = self.client.get(url, format="json")
    
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

        self.assertEqual(response.data[0]["description"], "Crédito Prueba")
         
    def test_get_credit_detail_no_valid_client(self):
        url = self.url_template.format(10)
        
        response = self.client.get(url, format="json")
    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
    def test_create_credit(self):
        url = reverse("credit-list")
        
        credit_data = {
            "description": "Crédito Prueba",
            "no_installment": 12,
            "penalty_rate": Decimal("2.5"),
            "interest_rate": self.interest_rate.id,
            "client": self.client_user.id,
            "products": [
                {"id_product": self.product1.id, "quantity": 2},
                {"id_product": self.product2.id, "quantity": 1}
            ]
        }
        
        response = self.client.post(url, credit_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_credit_no_products(self):
        url = reverse("credit-list")
        
        credit_data = {
            "description": "Crédito Prueba",
            "no_installment": 12,
            "penalty_rate": Decimal("2.5"),
            "interest_rate": self.interest_rate.id,
            "client": self.client_user.id,
            "products": []
        }
     
        response = self.client.post(url, credit_data, format="json") 
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_credit_inactive_product(self):
        url = reverse("credit-list")
        
        self.product1.is_active = False
        self.product1.save()
        
        credit_data = {
            "description": "Crédito Prueba",
            "no_installment": 12,
            "penalty_rate": Decimal("2.5"),
            "interest_rate": self.interest_rate.id,
            "client": self.client_user.id,
            "products": [
                {"id_product": self.product1.id, "quantity": 2},
                {"id_product": self.product2.id, "quantity": 1}
            ]
        }
     
        response = self.client.post(url, credit_data, format="json")
         
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_credit_inactive_client(self):
        url = reverse("credit-list")
        
        self.client_user.is_active = False
        self.client_user.save()
        
        credit_data = {
            "description": "Crédito Prueba",
            "no_installment": 12,
            "penalty_rate": Decimal("2.5"),
            "interest_rate": self.interest_rate.id,
            "client": self.client_user.id,
            "products": [
                {"id_product": self.product1.id, "quantity": 2},
                {"id_product": self.product2.id, "quantity": 1}
            ]
        }
     
        response = self.client.post(url, credit_data, format="json") 
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_put_credit(self):
        url = reverse("credit-detail", kwargs={"pk": self.credit.id})
        
        credit_data = {
            "description": "Crédito Prueba 1",
            "no_installment": 12,
            "penalty_rate": Decimal("2.5"),
            "status": "approved",
            "interest_rate": self.interest_rate.id,
            "client": self.client_user.id,
            "products": [
                {"id_product": self.product1.id, "quantity": 2},
                {"id_product": self.product2.id, "quantity": 1}
            ]
        }
        
        response = self.client.put(url, credit_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "approved")
        
    def test_update_patch_credit_approved(self):
        url = reverse("credit-detail", kwargs={"pk": self.credit.id})
        
        data = {
            "status": "approved"
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "approved")
        
    def test_update_patch_credit_rejected(self):
        url = reverse("credit-detail", kwargs={"pk": self.credit.id})
        
        data = {
            "status": "rejected"
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "rejected")
    
    def test_update_patch_credit_no_longer_updated(self):
        self.credit.status = "approved"
        self.credit.save()
        
        url = reverse("credit-detail", kwargs={"pk": self.credit.id})
        
        data = {
            "status": "rejected"
        }
        
        with self.assertRaises(ValidationError):
            response = self.client.patch(url, data)
            
    #Test for Payment
    def test_get_payment_list(self):
        url = reverse("credit-detail", kwargs={"pk": self.credit.id})
        
        data = {
            "status": "approved"
        }
        
        self.client.patch(url, data)
        
        url = reverse("payment-list")
        
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 5)
        
    def test_get_payment_detail(self):
        url = reverse("credit-detail", kwargs={"pk": self.credit.id})
        
        data = {
            "status": "approved"
        }
        
        self.client.patch(url, data)
        
        url = reverse("payment-detail", kwargs={"pk": 1})
        
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "pending")
        
    def test_create_payment(self):
        url = reverse("payment-list")
        
        payment_data = {
            "payment_amount": 100,
            "payment_date": "2024-10-10",
            "due_date": "2024-10-17",
            "credit": self.credit.id
        }
        
        response = self.client.post(url, payment_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
          
    def test_update_put_payment(self):
        payment_test = Payment.objects.create(
            payment_amount = 1000,
            payment_date = "2024-11-11",
            due_date = "2024-11-18",
            status = "pending",
            credit = self.credit
        )
        
        url = reverse("payment-detail", kwargs={"pk": payment_test.id})
        
        data = {
            "payment_amount": 1000,
            "payment_date": "2024-11-11",
            "due_date": "2024-11-18",
            "status": "completed",
            "credit": self.credit.id
        }
        
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "completed")
        
    def test_update_patch_payment(self):
        payment_test = Payment.objects.create(
            payment_amount = 1000,
            payment_date = "2024-11-11",
            due_date = "2024-11-18",
            status = "pending",
            credit = self.credit
        )
        
        url = reverse("payment-detail", kwargs={"pk": payment_test.id})
        
        data = {
            "status": "completed"
        }
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "completed")
        
    #Test for Interest Rate
    def test_get_interest_rate_list(self):
        url = reverse("interest_rates")
        
        response = self.client.get(url, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_interest_rate(self):
        url = reverse("interest_rates")
        
        data = {
            "percentage": 5.5
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_credit_string_representation(self):
        self.assertEqual(str(self.credit), "Crédito Prueba - 123456789012 - John Doe")
    
    def test_payment_string_representation(self):
        payment_test = Payment.objects.create(
            payment_amount = 1000,
            payment_date = "2024-11-11",
            due_date = "2024-11-18",
            status = "pending",
            credit = self.credit
        )
        
        self.assertEqual(str(payment_test), "1 - Crédito Prueba")
        
    def test_clientcreditproduct_string_representation(self):
        clientcreditproduct_data = self.credit.clientcreditproduct_set.all()
        self.assertEqual(str(clientcreditproduct_data[0]), "Crédito Prueba - 123456789012 - John Doe - Product 1 - Quantity: 2")
    
    def test_interest_rate_string_representation(self):
        self.assertEqual(str(self.interest_rate), "5.5")