from django.urls import path
from .views import TaskListCreateView, complete_task, ping

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:task_id>/complete/', complete_task, name='task-complete'),
    path('ping/', ping, name='ping'),
]
