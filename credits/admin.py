from django.contrib import admin
from .models import Credit, Payment, InterestRate, ClientCreditProduct

class ClientCreditProductInLine(admin.TabularInline):
    model = ClientCreditProduct
    extra = 1

class ClientCreditProductAdmin(admin.ModelAdmin):
    list_display = ('id_credit', 'id_product')
    list_display_links = ('id_credit', 'id_product')

class CreditAdmin(admin.ModelAdmin):
    inlines = [ClientCreditProductInLine]
    list_display = ('id', 'description', 'total_amount', 'no_installment', 'client')
    list_display_links = ('id', 'description')
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'credit', 'payment_amount', 'payment_date')
    list_display_links = ('id', 'credit')
    
admin.site.register(Credit, CreditAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(InterestRate)
admin.site.register(ClientCreditProduct, ClientCreditProductAdmin)



