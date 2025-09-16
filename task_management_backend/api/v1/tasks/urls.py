from django.urls import path
from . import views


app_name = "api_v1_tasks"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='admin_login'),
    path('tasks/', views.UserTaskListView.as_view(), name="task-list"),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
]