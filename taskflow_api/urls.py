from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('teams.urls')),
    path('api/', include('tasks.urls')),
    path('api/', include('comments.urls')),
]
