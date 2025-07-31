from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    """
    GET: List all tasks for the authenticated user
    POST: Create a new task for the authenticated user
    """
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        is_done = self.request.query_params.get('is_done')
        if is_done is not None:
            queryset = queryset.filter(is_done=is_done.lower() == 'true')
        return queryset
    


@api_view(['PATCH'])
def complete_task(request, task_id):
    """
    Mark a task as completed.
    Only the task owner can complete their task.
    """
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found or you do not have permission to access it'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    task.is_done = True
    task.completed_at = timezone.now() 
    task.save()
    
    serializer = TaskSerializer(task)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def ping(request):
    """
    Public health check endpoint.
    Returns 200 OK with status message.
    """
    return Response({'status': 'OK'})