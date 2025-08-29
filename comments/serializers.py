from rest_framework import serializers
from .models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    task = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'task', 'author', 'created_at', 'updated_at']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'task']
