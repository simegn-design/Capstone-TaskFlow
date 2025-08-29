from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamCreateSerializer, TeamMemberSerializer, TeamMemberAddSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class IsTeamAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Team):
            return TeamMember.objects.filter(team=obj, user=request.user, role='admin').exists()
        return False

class TeamListView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeamCreateSerializer
        return TeamSerializer
    
    def get_queryset(self):
        return Team.objects.filter(members__user=self.request.user)
    
    def perform_create(self, serializer):
        team = serializer.save(created_by=self.request.user)
        TeamMember.objects.create(team=team, user=self.request.user, role='admin')

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamAdmin]
    queryset = Team.objects.all()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsTeamAdmin])
def add_team_member(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    serializer = TeamMemberAddSerializer(data=request.data)
    
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        role = serializer.validated_data['role']
        
        user = get_object_or_404(User, id=user_id)
        TeamMember.objects.create(team=team, user=user, role=role)
        
        return Response({'status': 'member added'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, IsTeamAdmin])
def remove_team_member(request, team_id, user_id):
    team = get_object_or_404(Team, id=team_id)
    user = get_object_or_404(User, id=user_id)
    
    membership = get_object_or_404(TeamMember, team=team, user=user)
    membership.delete()
    
    return Response({'status': 'member removed'}, status=status.HTTP_200_OK)
