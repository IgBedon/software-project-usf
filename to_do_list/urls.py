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
    # path('home/', views.home, name="home"),

    path('environments/', views.environments, name="environments"),
    path('environments/create/', views.create_environment, name="create_environment"),
    path('environments/<int:environment_id>/', views.environment_selected, name="environment"),

    path('environments/<int:environment_id>/tasks/create/', views.create_task, name="create_task"),
    path('environments/<int:environment_id>/tasks/<int:task_id>/', views.task_detail, name="task_detail"),

    path('environments/<int:environment_id>/categories/create/', views.create_category, name="create_category"),
    path('environments/<int:environment_id>/categories/<int:category_id>/', views.category_detail, name="category_detail"),


    # path('home/', views.home, name="task_list"),

    path('trash/', views.trash, name="trash"),
]