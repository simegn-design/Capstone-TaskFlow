from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from teams.models import TeamMember

class IsTaskTeamMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            task_id = request.data.get('task')
            if task_id:
                from tasks.models import Task
                task = Task.objects.get(id=task_id)
                return TeamMember.objects.filter(team=task.team, user=request.user).exists()
        return True
    
    def has_object_permission(self, request, view, obj):
        return TeamMember.objects.filter(team=obj.task.team, user=request.user).exists()

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskTeamMember]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(task__team__members__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTaskTeamMember]
    queryset = Comment.objects.all()
