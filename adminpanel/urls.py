from django.urls import path
from .import views


urlpatterns = [
    path('', views.adminpanel, name='adminpanel' ),
    path('user_table/', views.user_table, name='user_table'),
    path('banned_user/', views.banned_user, name='banned_user'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('view_category/', views.view_category, name='view_category'),
    path('view_products/', views.view_products, name='view_products'),
    path('view_variations/', views.view_variations, name='view_variations'),
    path('add_product/', views.add_product, name='add_user'),
]