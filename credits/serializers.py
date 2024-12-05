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
        
        try:
            instance.update(validated_data)
            
            credit = instance.credit
            
            if credit.payment_set.filter(status="completed").count() == credit.payment_set.count():
                credit.status = "paid"
                credit.save()
        
        except Exception as e:
            raise ValidationError(f"Error updating payment: {str(e)}")
        
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
        
        inactive_products = [product['id_product'] for product in value if not product['id_product'].is_active]
        
        if inactive_products:
            product_names = "\n".join([product.name for product in inactive_products])
            raise ValidationError(
                f"The following products are inactive and cannot be added to credit: {product_names}"
            )
            
        return value
  
    def create(self, validated_data):
        products_data = validated_data.pop('clientcreditproduct_set')
        
        client = validated_data.get('client')
        
        if not client.is_active:
            raise ValidationError("The client is inactive and cannot create a credit")
        
        credit = Credit.objects.create(**validated_data)
        
        for product_data in products_data:
            ClientCreditProduct.objects.create(id_credit=credit, **product_data)
            
        credit.total_amount = credit.calculate_total_amount()
        
        credit.save()
            
        return credit
    
    def update(self, instance, validated_data):
        
        try:
            instance.update(validated_data)
        except Exception as e:
            raise ValidationError(f"Error updating credit: {str(e)}")
                
        return instance
        

    