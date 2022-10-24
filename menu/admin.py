from django.contrib import admin

#MODELS
from .models import (
    Category,
    FoodItem
)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'vendor', 'created_at']
    prepopulated_fields = {'slug': ('category_name',), }

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['food_title', 'category', 'vendor', 'price', 'is_available']
    list_filter = ['food_title', 'category__category_name', 'is_available']
    prepopulated_fields = {'slug': ('food_title',), }
    
    

admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
