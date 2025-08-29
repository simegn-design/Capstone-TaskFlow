from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField()
    created_by = serializers.StringRelatedField()
    team = serializers.StringRelatedField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'due_date', 
                 'assigned_to', 'team', 'created_by', 'created_at', 'updated_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'assigned_to', 'team']
