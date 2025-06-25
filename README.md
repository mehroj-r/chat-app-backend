# Chat App Backend

## Overview

This project is a robust, scalable backend for a real-time chat application, built with Django, Django REST Framework, and Django Channels. It supports user authentication, private and group chats, real-time messaging via WebSockets, and is fully containerized with Docker for easy deployment. PostgreSQL is used as the primary database and Redis powers the WebSocket layer for real-time communication.

---

## Features

- **User Management**: Registration, JWT authentication, profile management.
- **Chat System**: Private and group chats, chat membership management.
- **Real-Time Messaging**: WebSocket-based messaging with typing indicators.
- **RESTful API**: Endpoints for users, chats, and messages.
- **Scalable Architecture**: Uses Django Channels and Redis for real-time features.
- **Dockerized**: Easy local development and production deployment with Docker and docker-compose.

---

## Tech Stack

- **Backend**: Python, Django, Django REST Framework, Django Channels
- **Database**: PostgreSQL
- **Real-Time Layer**: Redis, Django Channels
- **Authentication**: JWT (via `rest_framework_simplejwt`)
- **Containerization**: Docker, docker-compose

---

## Architecture

```
[Client]
   |         REST (HTTP)        |         WebSocket (WS)   |
   |----------------------------|--------------------------|
   |                            |                          |
[ Django REST API ]        [ Django Channels ]
         |                        |
   [ PostgreSQL ]             [ Redis ]
```
- **REST API**: Handles user, chat, and message management.
- **WebSocket**: Handles real-time chat and typing notifications.
- **PostgreSQL**: Stores users, chats, and messages.
- **Redis**: Manages WebSocket channels and message brokering.

---

## Getting Started

### Prerequisites
- Docker & docker-compose
- Python 3.12+
- UV package manager

### Quick Start (Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mehroj-r/chat-app-backend.git
   cd chat-app-backend
   ```
2. **Create a `.env` file** in the project root with the following variables:
   ```env
   SECRET_KEY=your-django-secret-key
   POSTGRES_DB=chat_db
   POSTGRES_USER=chat_user
   POSTGRES_PASSWORD=yourpassword
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   REDIS_IP=redis
   REDIS_PORT=6379
   APP_PORT=8080
   PIPELINE=production
   # Add any other required variables
   ```
   You can use the provided `.env.example` as a template.
3. **Build and run the containers:**
   ```bash
   docker-compose up --build
   ```
4. **Access the API:**
   - API root: `http://localhost:8080/api/v1/`
   - Django admin: `http://localhost:8080/admin/`

### Manual Setup (Without Docker)

1. Install Python dependencies:
   ```bash
   uv sync
   uv run src/manage.py runserver 8000
   ```
2. Set up PostgreSQL and Redis locally.
3. Create a `.env` file as above.
4. Run migrations and start the server:
   ```bash
   python src/manage.py migrate
   python src/manage.py runserver
   ```

---

## Environment Variables

The following environment variables are required (see `.env`):
- `SECRET_KEY`: Django secret key
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`: PostgreSQL settings
- `REDIS_IP`, `REDIS_PORT`: Redis settings
- `APP_PORT`: Port for the backend server
- `PIPELINE`: Deployment environment (e.g., production)

---

## API Overview

### Authentication
- `POST /api/v1/auth/login/` — Obtain JWT token
- `POST /api/v1/auth/refresh/` — Refresh JWT token
- `POST /api/v1/auth/verify/` — Verify JWT token

### User Endpoints
- `POST /api/v1/users/signup/` — Register a new user
- `GET /api/v1/users/me/` — Get current user profile
- `GET /api/v1/users/search/?query=<name>` — Search users
- `PATCH /api/v1/users/update-profile/` — Update profile

### Chat Endpoints
- `GET /api/v1/chats/` — List user chats
- `POST /api/v1/chats/private/` — Create private chat
- `POST /api/v1/chats/group/` — Create group chat
- `GET /api/v1/chats/<chat_id>/messages/` — List messages in a chat
- `POST /api/v1/chats/<chat_id>/messages/` — Send a message
- `GET /api/v1/chats/<chat_id>/members/` — List chat members

### WebSocket Endpoints
- `ws://<host>/ws/chats/` — Chat list updates
- `ws://<host>/ws/chats/<chat_id>/` — Real-time messaging in a chat
  - Authenticate via JWT in the `Authorization` header: `Bearer <token>`

---

## Usage Example

**Register a user:**
```http
POST /api/v1/users/signup/
Content-Type: application/json
{
  "phone": "+1234567890",
  "first_name": "John",
  "password": "yourpassword"
}
```

**Connect to WebSocket:**
```js
const ws = new WebSocket('ws://localhost:8080/ws/chats/1/');
ws.onopen = () => {
  ws.send(JSON.stringify({ text: "Hello!" }));
};
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

