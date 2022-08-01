from django.urls import path
from . import views


urlpatterns = [
    path('', views.adminpanel, name='adminpanel' ),
    path('user_table/', views.user_table, name='user_table'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('view_category/', views.view_category, name='view_category'),
    path('view_products/', views.view_products, name='view_products'),
    path('view_variations/', views.view_variations, name='view_variations'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('ban_user/<int:id>/', views.ban_user, name='ban_user'),
    path('banned_user/', views.banned_user, name='banned_user'),
    path('unban_user/<int:id>/', views.unban_user, name='unban_user'),
    path('unlisted_products/', views.unlisted_products, name='unlisted_products'),
    path('list_products/<int:id>/', views.list_products, name='list_products'),
    path('unlisted_category/', views.unlisted_category, name='unlisted_category'),
    path('unlist_category/<int:id>/', views.unlist_category, name='unlist_category'),
    path('list_category/<int:id>/', views.list_category, name='list_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('search_user/', views.search_user, name='search_user'),
    path('accept_orders/<int:id>/', views.accept_orders, name='accept_orders'),
    path('accepted_orders/', views.accepted_orders_list, name='accepted_orders'),
    path('completed_order/<int:id>/', views.completed_order, name='completed_order'),
    path('completed_orders_list/', views.completed_orders_list, name='completed_orders_list'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),
]