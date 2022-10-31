from django.contrib import admin

#MODELS
from .models import (
    Cart
)

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'fooditem', 'quantity']
    
admin.site.register(Cart, CartAdmin)
 