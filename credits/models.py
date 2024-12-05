from django.db import models
from clients.models import Client
from products.models import Product

from django.core.exceptions import ValidationError 

from dateutil.relativedelta import relativedelta
from django.utils import timezone

def validate_positive(value):
    if value < 0:
        raise ValidationError("Ensure this value is greater than or equal to 0.")
    
class Credit(models.Model):
    
    CREDIT_STATUS = {
        "pending":"Pending",
        "approved":"Approved",
        "rejected":"Rejected",
        "paid":"Paid"
    }
    
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    no_installment = models.PositiveSmallIntegerField()
    application_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    penalty_rate = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_positive])
    status = models.CharField(max_length=15, default="pending", choices=CREDIT_STATUS)
    interest_rate = models.ForeignKey('InterestRate', on_delete=models.RESTRICT)    
    client = models.ForeignKey(Client, on_delete=models.RESTRICT) 
    products = models.ManyToManyField(Product, through='ClientCreditProduct', through_fields=('id_credit', 'id_product'), blank=False)
    
    def __str__(self) -> str:
        return f'{self.description} - {self.client}'
    
    def calculate_total_amount(self):
        total = 0
        
        for credit_product in self.clientcreditproduct_set.all():
            total += credit_product.id_product.price * credit_product.quantity
            
        return total

    def update(self, validated_data):
        status = validated_data.pop('status', [])
        instance_status = self.status
        
        if instance_status == "pending":
            if status == "approved":
                
                if self.payment_set.count() == 0:
                    start_date = timezone.now().date() + relativedelta(months=1)
                    no_installment = self.no_installment
                    monthly_amount = self.total_amount / no_installment
                    
                    for i in range(no_installment):
                        payment_date = start_date + relativedelta(months=i)
                        
                        Payment.objects.create(credit=self, payment_date=payment_date, due_date=payment_date + relativedelta(weeks=1), payment_amount=monthly_amount)
                    
                    self.start_date = start_date
                    self.end_date = self.start_date + relativedelta(months=self.no_installment-1)
                    
                    self.status = "approved"
                
            elif status == "rejected": 
                self.status = "rejected"
            
            else:
                raise ValidationError("The credit can no longer be updated.")
             
        else:
            raise ValidationError("The credit can no longer be updated.")
                               
        self.save()
        
class Payment(models.Model):
    
    PAYMENT_STATUS = {
        "pending":"Pending",
        "completed":"Completed"
    }
    
    id = models.AutoField(primary_key=True)
    payment_amount = models.DecimalField(max_digits=11, decimal_places=2)
    payment_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, default="pending", choices=PAYMENT_STATUS)
    credit = models.ForeignKey(Credit, on_delete=models.RESTRICT)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.credit.description}'
    
    def update(self, validated_data):
        status = validated_data.pop('status', [])
        instance_status = self.status
        
        if instance_status == "pending":
            if status == "completed":
                self.status = "completed"
            
            else:
                raise ValidationError("The payment can no longer be updated.")
                
        else:
            raise ValidationError("The payment can no longer be updated.")
            
        self.save()

class ClientCreditProduct(models.Model):
    id_credit = models.ForeignKey(Credit, on_delete=models.RESTRICT)
    id_product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveSmallIntegerField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_credit', 'id_product'], name='unique_client_credit_product')
        ]
  
    def __str__(self) -> str:
        return f'{self.id_credit} - {self.id_product} - Quantity: {self.quantity}'
     
class InterestRate(models.Model):
    id = models.SmallAutoField(primary_key=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=2, validators=[validate_positive])
    
    def __str__(self) -> str:
        return f'{self.percentage}'
    
    
    