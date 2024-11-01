from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check),
    path('register/', views.register, name="register_user"),
    path('login/', views.signin, name="login_user"),
    path('home/', views.home, name="home"),
]