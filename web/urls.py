from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:id>', views.delete_from_cart, name='delete_from_cart'),
    path('pay/<int:id>', views.pay, name='pay'),
    path('comments/', views.cart, name='comments'),
]
