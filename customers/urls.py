from django.urls import path
from accounts.views import my_account
from .import views
urlpatterns = [
    path('', my_account, name='customer'),
    path('cprofile/', views.cprofile, name='cprofile'),
    path('my-orders/', views.my_orders, name='my-orders'),
    path('order-detail/<int:id>/', views.order_detail, name='order-detail')
    
]
