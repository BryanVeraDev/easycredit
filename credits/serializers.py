from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Credit, Payment, InterestRate, ClientCreditProduct

from products.models import Product
from products.serializers import ProductInfoSerializer

from clients.models import Client
from clients.serializers import ClientInfoSerializer

from dateutil.relativedelta import relativedelta

from django.utils import timezone

class PaymentSerializer(serializers.ModelSerializer):
    credit = serializers.PrimaryKeyRelatedField(queryset=Credit.objects.all(), write_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 
            'payment_amount', 
            'payment_date', 
            'due_date', 
            'status', 
            'credit'
            ]
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        
        credit = instance.credit
        
        if credit.payment_set.filter(status="completed").count() == credit.payment_set.count():
            credit.status = "paid"
            credit.save()
        
        return instance
             
class InterestRateSerializer(serializers.ModelSerializer):   
    
    class Meta:
        model = InterestRate
        fields = '__all__'
        
class InterestRateInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InterestRate
        exclude = ['id']
        
class ClientCreditProductSerializer(serializers.ModelSerializer):
    id_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    product_info = ProductInfoSerializer(source='id_product', read_only=True)
    
    class Meta:
        model = ClientCreditProduct
        fields = [
            'id_product', 
            'product_info', 
            'quantity'
            ]
        
class CreditSerializer(serializers.ModelSerializer):
    
    products = ClientCreditProductSerializer(source='clientcreditproduct_set', many=True)
    
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True)
    client_info = ClientInfoSerializer(source='client', read_only=True)
    
    interest_rate = serializers.PrimaryKeyRelatedField(queryset=InterestRate.objects.all(), write_only=True)
    interest_rate_info = InterestRateInfoSerializer(source='interest_rate', read_only=True)
    
    payments = PaymentSerializer(source="payment_set", many=True, read_only=True)
    
    class Meta:
        model = Credit
        fields = [
            'id', 
            'description', 
            'total_amount', 
            'no_installment', 
            'application_date', 
            'start_date', 
            'end_date', 
            'penalty_rate', 
            'status', 
            'interest_rate', 
            'interest_rate_info',
            'client', 
            'client_info', 
            'products',
            'payments'
            ]
    
    #Validates that a product exists
    def validate_products(self, value):
        if not value:
            raise ValidationError("There must be at least one product.")
        return value
    
    """
    #Updates the product in the credit
    def _update_credit_products(self, instance, validated_data):
        product_data = validated_data.pop('clientcreditproduct_set', [])
       
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
                
        new_product_ids = [product['id_product'].id for product in product_data]
        
        if new_product_ids:
            #Update products in a credit
            instance.clientcreditproduct_set.exclude(id_product__in=new_product_ids).delete()
                    
            for product in product_data:
                ClientCreditProduct.objects.update_or_create(id_credit=instance, id_product=product['id_product'].id, defaults=product)
                    
            instance.total_amount = instance.calculate_total_amount()
    
    """
    
    def create(self, validated_data):
        products_data = validated_data.pop('clientcreditproduct_set')
        credit = Credit.objects.create(**validated_data)
        
        for product_data in products_data:
            ClientCreditProduct.objects.create(id_credit=credit, **product_data)
            
        credit.total_amount = credit.calculate_total_amount()
        
        credit.save()
            
        return credit
    
    def update(self, instance, validated_data):
        status = validated_data.pop('status', [])
        instance_status = instance.status
        
        if instance_status == "pending":
            if status == "approved":
                
                if instance.payment_set.count() == 0:
                    start_date = timezone.now().date() + relativedelta(months=1)
                    no_installment = instance.no_installment
                    monthly_amount = instance.total_amount / no_installment
                    
                    for i in range(no_installment):
                        payment_date = start_date + relativedelta(months=i)
                        
                        Payment.objects.create(credit=instance, payment_date=payment_date, due_date=payment_date + relativedelta(weeks=1), payment_amount=monthly_amount)
                    
                    instance.start_date = start_date
                    instance.end_date = instance.start_date + relativedelta(months=instance.no_installment-1)
                    
                    """
                    Update the product in the credit
                    self._update_credit_products(instance, validated_data)
                    """
                    
                    instance.status = "approved"
                
            elif status == "rejected": 
                instance.status = "rejected"
            
            elif status == "pending":
                self._update_credit_products(instance, validated_data)
                
        else:
            raise ValidationError("The credit can no longer be updated.")
                               
        instance.save()
                 
        return instance
        

    