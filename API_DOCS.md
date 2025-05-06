# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "phone": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully"
}
```

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "string",
  "first_name": "string",
  "last_name": "string"
}
```

### Get User Profile
```http
GET /auth/me
```

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": "number",
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string"
}
```

### Update Profile
```http
PUT /auth/profile
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "phone": "string"
}
```

## Image Processing

### Upload Image
```http
POST /images/upload
```

**Headers:**
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**Request Body:**
```
file: File
```

**Response:**
```json
{
  "imageUrl": "string",
  "prediction": "string"
}
```

## AI Consultation

### Get AI Explanation
```http
POST /deepseek/explain
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "result": "string",
  "lastName": "string",
  "messages": [
    {
      "role": "string",
      "content": "string"
    }
  ]
}
```

**Response:**
```json
{
  "explanation": "string"
}
```

### Medical Q&A
```http
POST /medical/qa
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "question": "string"
}
```

**Response:**
```json
{
  "answer": "string",
  "sources": ["string"]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Access denied"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
``` 