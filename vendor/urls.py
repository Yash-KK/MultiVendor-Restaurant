from django.urls import path

#VIEWS
from accounts import views as account_views
from .import views

urlpatterns = [
    path("", account_views.my_account, name='vendor'),
    path("profile/", views.v_profile, name='v-profile'),
    
    path("menu-builder/", views.menu_builder, name='menu-builder'),
    path("menu-builder/add-category/", views.add_category, name='add-category'),
    
    #CATEGORY CRUD
    path('menu-builder/edit-category/<slug:slug>/', views.edit_category, name='edit-category'),
    path('menu-builder/delete-category/<slug:slug>/', views.delete_category, name='delete-category'),
    path('menu-builder/items-by-category/<slug:category_slug>/', views.items_by_category, name='items-by-category'),
    
    #FOOD ITEM CRUD
    path('menu-builder/add-food-item/', views.add_food_item, name='add-food-item'),
    path('menu-builder/delete-food-item/<slug:slug>/', views.delete_food_item, name='delete-food-item'),
    path("menu-builder/edit-food-item/<slug:slug>/", views.edit_food_item, name='edit-food-item'),
    
    
    #OPENING HOURS
    path('opening-hours/',views.opening_hours, name='opening-hours'),
    path('add-hours/', views.add_hours, name='add-hours'),
    
    path("remove-opening-hours/<int:pk>/", views.remove_add_hours, name='remove-add-hours'),
    
    path('vendor-order-detail/<int:order_number>/', views.vendor_order_detail, name='vendor-order-detail')
    
]
