from rest_framework import serializers
from .models import Team, TeamMember
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamMemberSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = TeamMember
        fields = ['id', 'user', 'role', 'joined_at']

class TeamSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    members = TeamMemberSerializer(many=True, read_only=True)
    members_count = serializers.IntegerField(source='members.count', read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at', 'members', 'members_count']

class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description']

class TeamMemberAddSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    
    class Meta:
        model = TeamMember
        fields = ['user_id', 'role']
