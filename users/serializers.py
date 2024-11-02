from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'email', 
            'phone',
            'password', 
            'address', 
            'date_joined', 
            'last_login',
            'is_active', 
            'is_staff', 
            'is_superuser', 
            'groups'
            ]
        extra_kwargs = {'password': {'write_only': True}}
     
    def create(self, validated_data):
        
        print(validated_data)
        password = validated_data.pop('password')
        groups_data = validated_data.pop('groups', None)
      
        user = User(**validated_data)  
        
        user.set_password(password)
        user.save()
        user.groups.set(groups_data)
        
        return user
