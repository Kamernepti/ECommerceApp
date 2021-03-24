from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logging', views.logging),
    path('register', views.register),
    path('cart', views.cart),
    path('purchase', views.purchase),
]
