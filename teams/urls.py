from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.TeamListView.as_view(), name='team-list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
    path('teams/<int:team_id>/members/', views.add_team_member, name='add-team-member'),
    path('teams/<int:team_id>/members/<int:user_id>/', views.remove_team_member, name='remove-team-member'),
]
