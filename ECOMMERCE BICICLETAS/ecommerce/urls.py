from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path("", views.login_view, name="login"),
    path("productos/", views.productos, name="productos"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
]
