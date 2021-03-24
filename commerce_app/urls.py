from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('cart', views.cart),
    path('purchase', views.purchase),
    path('add', views.add, name="add_to_cart")
]
