from django.urls import path
from . import views


app_name = "task"

urlpatterns = [
    path('', views.admin_login_view, name='admin_login'),
    path('dashboard/', views.admin_dashboard_view, name='dashboard'),
    path('users/', views.user_management_view, name='user_management'),
    path('admins/', views.admin_management_view, name='admin_management'),
    path('tasks/', views.task_management_view, name='task_management'),
    path('reports/', views.task_reports_view, name='task_reports'),
    path('users/create/', views.create_user_view, name='create_user'),
    path('admins/create/', views.create_admin_view, name='create_admin'),
    path('tasks/create/', views.create_task_view, name='create_task'),
    path('users/<int:user_id>/delete/', views.delete_user_view, name='delete_user'),
    path('admins/<int:admin_id>/delete/', views.delete_admin_view, name='delete_admin'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
]