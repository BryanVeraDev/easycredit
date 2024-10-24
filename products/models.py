from django.db import models

class Product(models.Model):
    
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    is_active = models.BooleanField(("active"), default=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.RESTRICT)
    
    def __str__(self) -> str:
        return self.name

class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    
    def __str__(self):
        return self.description