from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name="home"),
    path('search/', views.search, name="search"),
    path('success/', views.success, name="success"),
    path('detail/', views.detail, name="detail"),
    path('category/', views.category, name="category"),
    path('register/', views.register, name="register"),
    path('login/', views.loginForm, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path("review/<int:product_id>/", review, name="review"),
    path('review/<int:product_id>/add/', add_or_update_review, name="add_review"),
    path('review/<int:product_id>/delete/', delete_review, name='delete_review'),
    path('update_order/', views.updateOrder, name="update_order"),
    path('delete-order-detail/<int:detail_id>/', delete_order_detail, name='delete_order_detail'),
]