from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check),
    path('register/', views.register, name="register_user"),
    path('login/', views.signin, name="login_user"),

    path('home/', views.home, name="home"),

    path('environments/', views.environments, name="environments"),
    path('environments/create/', views.create_environment, name="create_environment"),

    path('environments/<int:environment_id>/tasks/', views.tasks, name="tasks"),
    path('environments/<int:environment_id>/tasks/create/', views.create_task, name="create_task"),
    path('environments/<int:environment_id>/tasks/<int:task_id>/', views.task_detail, name="task_detail"),

    # path('home/', views.home, name="task_list"),

    path('trash/', views.trash, name="trash"),
]