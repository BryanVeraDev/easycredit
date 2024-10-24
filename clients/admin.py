from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    exclude = ['date_joined']
    
admin.site.register(Client, ClientAdmin)