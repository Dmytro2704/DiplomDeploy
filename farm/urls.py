from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns=[
    path("",views.index, name='index'),
    path("about",views.about, name="about"),
    path("blog",views.blog, name="blog"),
    path("contact",views.contact, name="contact"),
    path("products",views.products, name="products"),
    path("registration",views.registration, name="registration"),
    path("buy_page",views.buy_page, name="buy_page"),
    path('login', views.CustomLoginView.as_view(), name='blog_login'),
    path('logout', views.user_logout, name='blog_logout'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),


]