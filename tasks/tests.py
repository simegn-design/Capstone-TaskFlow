from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from teams.models import Team, TeamMember
from .models import Task

User = get_user_model()

class TaskTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@test.com', username='user1', password='testpass123')
        self.user2 = User.objects.create_user(email='user2@test.com', username='user2', password='testpass123')
        self.team = Team.objects.create(name='Test Team', description='Test', created_by=self.user1)
        TeamMember.objects.create(team=self.team, user=self.user1, role='admin')
        TeamMember.objects.create(team=self.team, user=self.user2, role='member')
        self.client = APIClient()
    
    def test_create_task(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post('/api/tasks/', {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'todo',
            'priority': 'medium',
            'team': self.team.id,
            'assigned_to': self.user2.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_list_tasks(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test',
            team=self.team,
            created_by=self.user1,
            assigned_to=self.user2
        )
        
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
