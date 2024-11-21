from django.db import models
from authtools.models import AbstractEmailUser

class User(AbstractEmailUser):
    
    id = models.CharField(max_length=12, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=50)
    is_staff = models.BooleanField(("staff status"), default=True, help_text=("Designates whether the user can log into this admin site."),)
    
    REQUIRED_FIELDS = ['id', 'first_name', 'last_name', 'phone', 'address']
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Avoid conflict with'auth.User'
        blank=False
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Avoid conflict with 'auth.User'
        blank=True
    )
    
    def __str__(self) -> str:
        return f'{self.id} - {self.first_name} {self.last_name}'