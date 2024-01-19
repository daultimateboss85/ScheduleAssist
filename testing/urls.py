from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.loginView, name="login"),

    path("home", views.Home, name="home"),

]
