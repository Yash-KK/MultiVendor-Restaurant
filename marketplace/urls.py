from django.urls import path

from .import views
urlpatterns = [
    path("", views.market_place, name='market-place'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor-detail')
]


