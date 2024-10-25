from rest_framework import serializers
from .models import ProductType, Product


class ProductTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductType
        fields = ['id', 'description']
        
class ProductSerializer(serializers.ModelSerializer):
    
    """
    To modify the Product Type foreign key and display it
    ---
    product_type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())
    product_type_info = ProductTypeSerializer(source='product_type', read_only=True)
    ---
    
    Only display product_type data
    ---
    product_type = ProductTypeSerializer(read_only=True)
    ---
    """
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'is_active', 'product_type']
        
