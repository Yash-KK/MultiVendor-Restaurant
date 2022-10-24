from django.urls import path

#VIEWS
from accounts import views as account_views
from .import views

urlpatterns = [
    path("", account_views.my_account, name='vendor'),
    path("profile/", views.v_profile, name='v-profile'),
    
    path("menu-builder/", views.menu_builder, name='menu-builder'),
    path("add-category/", views.add_category, name='add-category'),
    path('edit-category/<slug:slug>/', views.edit_category, name='edit-category'),
    path('delete-category/<slug:slug>/', views.delete_category, name='delete-category'),
    path('items-by-category/<slug:category_slug>/', views.items_by_category, name='items-by-category'),
    
]
