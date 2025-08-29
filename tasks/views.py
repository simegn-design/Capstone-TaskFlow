from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer
from teams.models import TeamMember

class IsTeamMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'team' in request.data:
            team_id = request.data['team']
            return TeamMember.objects.filter(team_id=team_id, user=request.user).exists()
        return True
    
    def has_object_permission(self, request, view, obj):
        return TeamMember.objects.filter(team=obj.team, user=request.user).exists()

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(team__members__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]
    queryset = Task.objects.all()
