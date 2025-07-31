from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Handles creation, updating, and representation of tasks.
    """
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_done', 'created_at', 'updated_at', 'completed_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def create(self, validated_data):
        """
        Create a new task and associate it with the current user.
        """
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)
    