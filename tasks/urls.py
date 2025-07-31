from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/all/', views.get_all_tasks, name='get-all-tasks'),
    path('tasks/delete/<int:pk>/', views.delete_task, name='delete-task'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/create/', views.task_create, name='task-create'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]