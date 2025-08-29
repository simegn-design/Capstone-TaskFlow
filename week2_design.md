# TaskFlow API - Design Phase

## Database Schema (ERD)
![TaskFlow ERD](https://via.placeholder.com/800x600/0088cc/ffffff?text=TaskFlow+ERD+Diagram)

### Models Description:
**User**
- id (PrimaryKey)
- username (CharField)
- email (EmailField)
- password (CharField)
- profile_pic (ImageField)
- bio (TextField)
- date_joined (DateTimeField)

**Team** 
- id (PrimaryKey)
- name (CharField)
- description (TextField)
- created_by (ForeignKey: User)
- created_at (DateTimeField)

**TeamMember** (Through model)
- id (PrimaryKey)
- user (ForeignKey: User)
- team (ForeignKey: Team)
- role (CharField: 'admin', 'member')

**Task**
- id (PrimaryKey)
- title (CharField)
- description (TextField)
- status (CharField: 'todo', 'in_progress', 'done')
- priority (CharField: 'low', 'medium', 'high')
- due_date (DateTimeField)
- assigned_to (ForeignKey: User)
- team (ForeignKey: Team)
- created_by (ForeignKey: User)
- created_at (DateTimeField)

**Comment**
- id (PrimaryKey)
- content (TextField)
- task (ForeignKey: Task)
- author (ForeignKey: User)
- created_at (DateTimeField)

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/user/` - Get current user

### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user profile
- `GET /api/users/me/` - Get current user profile

### Teams
- `GET /api/teams/` - List user's teams
- `POST /api/teams/` - Create new team
- `GET /api/teams/{id}/` - Get team details
- `PUT /api/teams/{id}/` - Update team
- `DELETE /api/teams/{id}/` - Delete team
- `POST /api/teams/{id}/members/` - Add member to team
- `DELETE /api/teams/{id}/members/{user_id}/` - Remove member

### Tasks
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `GET /api/teams/{id}/tasks/` - Get team tasks

### Comments
- `GET /api/tasks/{id}/comments/` - List task comments
- `POST /api/tasks/{id}/comments/` - Add comment
- `PUT /api/comments/{id}/` - Update comment
- `DELETE /api/comments/{id}/` - Delete comment

## Relationships
- User 1───┐ Many TeamMember
- Team 1───┘ Many TeamMember
- Team 1───┐ Many Task
- User 1───┘ Many Task (assigned_to)
- Task 1───┐ Many Comment
- User 1───┘ Many Comment
