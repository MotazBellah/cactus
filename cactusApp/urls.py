from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.index, name="index"),
    path("register", views.register, name='register'),
    path("logout", views.logout, name='logout'),
]
