from django.urls import path
from . import views

urlpatterns = [
    path("", views.root),
    path('register/', views.register, name="register_user"),
    path('login/', views.signin, name="login_user"),
    path('logout_user/', views.logout_user, name="logout"),

    path('account/', views.account, name="account"),
    path('account/update/', views.update_account, name="update_account"),
    path('account/update/password/', views.update_account_password, name="update_account_password"),
    path('account/delete/', views.delete_account, name="delete_account"),

    path('environments/', views.environments, name="environments"),
    path('environments/create/', views.create_environment, name="create_environment"),
    path('environments/<int:environment_id>/', views.environment_selected, name="environment"),
    path('environments/<int:environment_id>/update/', views.update_environment, name="update_environment"),
    path('environments/<int:environment_id>/delete/', views.delete_environment, name="delete_environment"),

    path('environments/<int:environment_id>/tasks/create/', views.create_task, name="create_task"),
    path('environments/<int:environment_id>/tasks/<int:task_id>/', views.task_detail, name="task_detail"),
    path('environments/<int:environment_id>/tasks/<int:task_id>/update/', views.update_task, name="update_task"),
    path('environments/<int:environment_id>/tasks/<int:task_id>/delete/', views.delete_task, name="delete_task"),

    path('environments/<int:environment_id>/tasks/<int:task_id>/add_attachment/', views.add_attachment, name="add_attachment"),
    path('environments/<int:environment_id>/tasks/<int:task_id>/remove_attachment/', views.remove_attachment, name="remove_attachment"),

    path('environments/<int:environment_id>/tasks/<int:task_id>/add_category/', views.add_category, name="add_category"),
    path('environments/<int:environment_id>/tasks/<int:task_id>/remove_category/', views.remove_category, name="remove_category"),

    path('environments/<int:environment_id>/categories/create/', views.create_category, name="create_category"),
    path('environments/<int:environment_id>/categories/<int:category_id>/', views.category_detail, name="category_detail"),
    path('environments/<int:environment_id>/categories/<int:category_id>/update/', views.update_category, name="update_category"),
    path('environments/<int:environment_id>/categories/<int:category_id>/delete/', views.delete_category, name="delete_category"),

    path('about_us/', views.about_us, name="about_us"),
]