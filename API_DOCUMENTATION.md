# TaskFlow API Documentation

## Base URL
`https://domain.com/api/`

## Authentication
All endpoints require JWT authentication except registration and login.

### Register User
**POST** `/auth/register/`
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "password2": "testpass123"
}
