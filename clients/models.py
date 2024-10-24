from django.db import models
from django.utils import timezone

class Client(models.Model):

    id = models.CharField(max_length=12, primary_key=True)
    first_name = models.CharField(max_length=30, default='', blank=False)
    last_name = models.CharField(max_length=30, default='', blank=False)
    email = models.EmailField(unique=True, default='', blank=False)
    phone = models.CharField(max_length=12, default='', blank=False)
    date_joined = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=50, default='', blank=False)
    is_active = models.BooleanField(("active"), default=True)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.first_name} {self.last_name}'