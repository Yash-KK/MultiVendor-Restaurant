from django.urls import path, include

from .import views
urlpatterns = [
    path('', views.my_account, name='accounts'),
    path("register-user/", views.register_user, name='register-user'),
    path('register-vendor/', views.register_vendor, name='register-vendor'),
    
    path('login-user', views.login_user, name='login-user'),
    path("logout-user", views.logout_user, name='logout-user'),
    
    path("my-account/", views.my_account, name='my-account'),
    path('customer-dashboard', views.customer_dashboard, name='customer-dashboard'),
    path('vendor-dashboard', views.vendor_dashboard, name='vendor-dashboard'),
    
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path("reset-password/", views.reset_password, name='reset-password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset-password-validate'),
    
    path("vendor/", include('vendor.urls'))
]
