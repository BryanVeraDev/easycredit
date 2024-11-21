from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = "__all__"
        
class ClientInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        exclude = [
            'date_joined',
            'is_active'
        ]