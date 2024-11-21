from django.urls import reverse
from rest_framework.test import APITestCase
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
            credit.save()  
