from django.urls import path

from .import views
urlpatterns = [
    path("register-user/", views.register_user, name='register-user'),
    path('register-vendor/', views.register_vendor, name='register-vendor'),
    
    path('login-user', views.login_user, name='login-user'),
    path("logout-user", views.logout_user, name='logout-user'),
    
    path("my-account/", views.my_account, name='my-account'),
    path('customer-dashboard', views.customer_dashboard, name='customer-dashboard'),
    path('vendor-dashboard', views.vendor_dashboard, name='vendor-dashboard')
]
