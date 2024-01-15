from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:curso_id>/',views.add_cart, name='add_cart'),
    path('remove_cart_item/<int:curso_id>/',views.remove_cart_item, name='remove_cart_item'),
    #path('cart/<str:incart>/', views.cart, name='cart_with_incart'),
    path('checkout/',views.checkout, name='checkout'),
]
