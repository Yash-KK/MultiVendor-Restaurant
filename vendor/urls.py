from django.urls import path

#VIEWS
from accounts import views as account_views
from .import views

urlpatterns = [
    path("", account_views.my_account, name='vendor'),
    path("profile/", views.v_profile, name='v-profile')
]
