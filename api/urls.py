from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('menu-items', views.list_menu_items, name='list_menu_items'),
    path('menu-items/<int:id>', views.get_menu_item, name='get_menu_item'),
    path('groups/manager/users', views.list_managers, name='list_managers'),
    path('groups/manager/users/<int:pk>',
         views.get_manager, name='get_manager'),
    path('cart/menu-items', views.cart_items, name='cart_items'),
    path('cart/menu-items/<int:pk>', views.cart, name='cart'),
    path('orders', views.list_orders, name='list_orders'),
    path('orders/<int:orderId>/<int:userId>',
         views.list_orders, name='list_orders'),
    path('jwt/token', views.create_tokens, name='create_tokens'),
]
