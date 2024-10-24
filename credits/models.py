from django.db import models
from clients.models import Client
from products.models import Product

class Credit(models.Model):
    
    CREDIT_STATUS = {
        "pending":"Pending",
        "approved":"Approved",
        "rejected":"Rejected",
        "paid":"Paid",
        "default": "Default"
    }
    
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=11, decimal_places=2)
    no_installment = models.SmallIntegerField()
    application_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    penalty_rate = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.CharField(max_length=15, choices=CREDIT_STATUS)
    interest_rate = models.ForeignKey('InterestRate', on_delete=models.RESTRICT)    
    client = models.ForeignKey(Client, on_delete=models.RESTRICT) 
    products = models.ManyToManyField(Product, through='ClientCreditProduct', through_fields=('id_credit', 'id_product'))
    
    def __str__(self) -> str:
        return f'{self.description} - {self.client}'

class Payment(models.Model):
    
    PAYMENT_STATUS = {
        "pending":"Pending",
        "completed":"Completed"
    }
    
    id = models.AutoField(primary_key=True)
    payment_amount = models.DecimalField(max_digits=11, decimal_places=2)
    payment_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=PAYMENT_STATUS)
    credit = models.ForeignKey(Credit, on_delete=models.RESTRICT)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.credit.description}'

class ClientCreditProduct(models.Model):
    id = models.AutoField(primary_key=True)
    id_credit = models.ForeignKey(Credit, on_delete=models.RESTRICT)
    id_product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.SmallIntegerField()
  
    def __str__(self) -> str:
        return f'{self.id_credit} - {self.id_product} - Quantity: {self.quantity}'
    
class InterestRate(models.Model):
    id = models.SmallAutoField(primary_key=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    
    def __str__(self) -> str:
        return f'{self.percentage}'
    
    
    