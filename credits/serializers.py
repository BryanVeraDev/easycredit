from rest_framework import serializers
from .models import Credit, Payment, InterestRate
from products.serializers import ProductSerializer

class CreditSerializer(serializers.ModelSerializer):
    
    products = ProductSerializer(many=True)
    
    class Meta:
        model = Credit
        fields = ['id', 'description', 'total_amount', 'no_installment', 
                  'application_date', 'start_date', 'end_date', 'penalty_rate', 
                  'status', 'interest_rate', 'client', 'products']
        
class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = ['id', 'payment_amount', 'payment_date', 
                  'due_date', 'status', 'credit']
        
class InterestRateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = InterestRate
        fields = '__all__'