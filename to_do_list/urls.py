from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check),
    path('register/', views.register),
    path('teste/', views.register, name="cadastrar_usuario"),
]