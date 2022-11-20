from django.contrib import admin

from .models import (
    Order,
    OrderedFood,
    Payment
)
# Register your models here.

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ['order', 'vendor','fooditem', 'quantity', 'price']
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_number', 'payment', 'phone', 'order_placed_to', 'is_ordered']
    inlines = [
        OrderedFoodInline
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
admin.site.register(Payment)

