from django.urls import path

from .import views
urlpatterns = [
    path("", views.market_place, name='market-place'),
    path("add-to-cart/<int:food_id>/", views.add_to_cart, name='add-to-cart'),
    path('decrease-cart/<int:food_id>/', views.decrease_cart, name='decrease-cart'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor-detail'),
    path('delete-cart-item/<int:cart_item_id>/', views.delete_cart_item, name='delete-cart-item')
]


