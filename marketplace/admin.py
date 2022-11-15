from django.contrib import admin

#MODELS
from .models import (
    Cart,
    Tax
)

# Register your models here. 
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'fooditem', 'quantity']
class TaxAdmin(admin.ModelAdmin):
    list_display = ['tax_type', 'tax_percentage', 'is_active']
    list_display_links = ['tax_type']
    
admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
