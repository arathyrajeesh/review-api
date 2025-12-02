from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services_list'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('service/<int:service_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('service/<int:service_id>/add-review/', views.add_review, name='add_review'),
    path('cart/', views.cart, name='cart'),
    path('cart/<int:cart_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('reviews/', views.my_reviews, name='my_reviews'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]