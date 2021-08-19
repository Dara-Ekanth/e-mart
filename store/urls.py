from django.urls import path
from . import views

urlpatterns = [
    path('', views.ordered_item, name="ordered_item"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/description/<str:id>', views.product_info, name="product_description_page"),
    path('update_item/', views.updateItem, name="update_item"),
    path('previous/order', views.prev_orders, name="prev_orders"),
    path('previous/items/<str:id>', views.prev_items, name="prev_items"),
]
