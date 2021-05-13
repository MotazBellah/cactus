from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.Login_view, name="login"),
    path("home", views.index, name="index"),
    path("register", views.register, name='register'),
    path("logout", views.logout_view, name='logout'),
    path("kids", views.kids, name='kids'),
    path("kid/<int:kid_id>", views.kid_view, name='kid'),
    path("charts/<int:kid_id>", views.chart_weight, name='charts'),
    path("delete", views.delete_child, name='delete'),

]
