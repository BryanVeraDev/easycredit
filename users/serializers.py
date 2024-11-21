from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User

from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password

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
    
    #Validates that a user's password is secure
    def validate_password_similarity(self, value, user):
        try:
            validate_password(value, user)
        except DjangoValidationError as e:
            raise ValidationError(e.messages)
            
    def create(self, validated_data):
        
        password = validated_data.pop('password')
        groups_data = validated_data.pop('groups', None)
      
        user = User(**validated_data)  
        
        self.validate_password_similarity(password, user)
        user.set_password(password)
        
        user.save()
        
        user.groups.set(groups_data)
        
        return user
