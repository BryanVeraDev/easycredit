from django.test import TestCase
from products.models import ProductType

# Create your tests here.

class ProductTypeTestCase(TestCase):
    def setUp(self):
        ProductType.objects.create(description="Implementos de cocina")
    
    def test_productType(self):
        product = ProductType.objects.get(description="Implementos de cocina")
        self.assertEqual(product.description, "TEST")
