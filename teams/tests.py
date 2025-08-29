from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Team, TeamMember

User = get_user_model()

class TeamTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@test.com', username='user1', password='testpass123')
        self.user2 = User.objects.create_user(email='user2@test.com', username='user2', password='testpass123')
        self.client = APIClient()
    
    def test_create_team(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/teams/', {
            'name': 'Test Team',
            'description': 'Test Description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(TeamMember.objects.count(), 1)
    
    def test_list_teams(self):
        team = Team.objects.create(name='Test Team', description='Test', created_by=self.user1)
        TeamMember.objects.create(team=team, user=self.user1, role='admin')
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_add_team_member(self):
        team = Team.objects.create(name='Test Team', description='Test', created_by=self.user1)
        TeamMember.objects.create(team=team, user=self.user1, role='admin')
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f'/api/teams/{team.id}/members/', {
            'user_id': self.user2.id,
            'role': 'member'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamMember.objects.count(), 2)
