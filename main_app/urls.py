from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for items index
    path('items/', views.items_index, name='index'),
    path('items/<int:item_id>', views.items_detail, name='detail'),
    path('cart/', views.cart, name='cart'),
]
