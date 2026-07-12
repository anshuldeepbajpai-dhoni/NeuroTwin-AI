# 🧠 NeuroTwin AI

NeuroTwin AI is an intelligent Digital Twin platform designed to create a personalized AI representation of each user.

The system combines secure user authentication, profile management, Digital Twin configuration, long-term memory storage, intelligent search, filtering, pagination, and future AI-powered conversation capabilities.

The backend is developed using FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic, and JWT authentication. The project follows a modular and scalable architecture with separate layers for API routes, database models, schemas, CRUD operations, authentication dependencies, exception handling, database migrations, and automated testing.

---

## 🚀 Project Status

| Phase | Module | Status |
|---|---|---|
| Phase 2.1 | Authentication and User Management | ✅ Completed |
| Phase 2.2 | Profile and Digital Twin Management | ✅ Completed |
| Phase 2.3 | Memory Management | ✅ Completed |
| Phase 2.4 | Conversation and Message Management | ✅ Completed |
| Phase 2.5 | AI Integration | ✅ Completed |
| Phase 2.6 | AI Intelligence and Memory System | ✅ Completed |

Current backend progress:

```text
Phase 2.1  ████████████████████  100%
Phase 2.2  ████████████████████  100%
Phase 2.3  ████████████████████  100%
Phase 2.4  ████████████████████  100%
Phase 2.5  ████████████████████  100%
Phase 2.6  ████████████████████  100%
```

---

# ✨ Core Features

## Authentication and User Management

- User registration
- Secure user login
- JWT access-token generation
- Password hashing
- Protected API endpoints
- Current-user authentication
- Role-based user structure
- Duplicate-user validation
- User activation status
- Authentication tests

## User Profile Management

- Retrieve the authenticated user's profile
- Update phone number
- Update biography
- Update date of birth
- Update timezone
- Update preferred language
- Upload a profile avatar
- Replace an existing avatar
- Delete a profile avatar
- Static avatar file serving
- Profile API tests

## Digital Twin Management

- Create one Digital Twin per authenticated user
- Retrieve the current user's Digital Twin
- Update Digital Twin configuration
- Delete a Digital Twin
- Prevent duplicate Digital Twins
- Validate empty update requests
- User-level ownership protection
- Custom exception handling
- Digital Twin lifecycle tests

## Memory Management

- Create memories linked to a user and Digital Twin
- Retrieve a specific memory
- Retrieve all user memories
- Update memories
- Delete memories
- Search by title and content
- Filter by category
- Filter by importance
- Filter favorite memories
- Sort memory records
- Paginate memory records
- Return pagination metadata
- Enforce memory ownership
- Handle missing memories
- Reject empty update requests
- Complete Memory lifecycle testing

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Object Relational Mapper |
| Alembic | Database schema migrations |
| Pydantic v2 | Request and response validation |
| JWT | Token-based authentication |
| Uvicorn | ASGI development server |
| Passlib/Bcrypt | Secure password hashing |
| Pytest | Automated backend testing |
| HTTPX/TestClient | API endpoint testing |
| Swagger UI | Interactive API documentation |
| Git | Version control |
| GitHub | Source-code hosting |

---

# 📁 Project Structure

```text
NeuroTwin-AI/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── profile.py
│   │   │   ├── digital_twin.py
│   │   │   └── memory.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logger.py
│   │   │   └── security.py
│   │   │
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── profile.py
│   │   │   ├── digital_twin.py
│   │   │   └── memory.py
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── database.py
│   │   │   └── session.py
│   │   │
│   │   ├── dependencies/
│   │   │   ├── __init__.py
│   │   │   └── auth.py
│   │   │
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── custom_exceptions.py
│   │   │   └── digital_twin.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── digital_twin.py
│   │   │   └── memory.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── profile.py
│   │   │   ├── digital_twin.py
│   │   │   └── memory.py
│   │   │
│   │   ├── main.py
│   │   └── __init__.py
│   │
│   ├── migrations/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── static/
│   │   └── avatars/
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_digital_twin.py
│   │   ├── test_memory.py
│   │   ├── test_profile.py
│   │   └── test_root.py
│   │
│   ├── alembic.ini
│   ├── pytest.ini
│   └── requirements.txt
│
├── .gitignore
├── README.md
└── LICENSE
```

> The exact structure may change as new modules are added.

---

# Phase 2.1 – Authentication and User Management

## Overview

Phase 2.1 established the authentication foundation of NeuroTwin AI.

The module enables users to register, authenticate securely, receive JWT access tokens, and access protected endpoints.

## Features Completed

- User database model
- UUID-based user identification
- User registration
- Unique username validation
- Unique email validation
- Secure password hashing
- User login
- JWT access-token generation
- Token validation
- Current-user authentication dependency
- Protected API routes
- User role support
- User active-status support
- Authentication exception handling
- Swagger authentication support
- Authentication API tests

## User Model

The User model contains fields such as:

| Field | Description |
|---|---|
| `id` | Unique UUID-based user identifier |
| `username` | Unique username |
| `email` | Unique user email |
| `password_hash` | Securely hashed password |
| `phone` | Optional phone number |
| `bio` | Optional user biography |
| `date_of_birth` | Optional date of birth |
| `avatar_url` | Profile-avatar location |
| `timezone` | User timezone |
| `language` | Preferred language |
| `role` | User authorization role |
| `is_active` | Account activation status |
| `created_at` | Account creation timestamp |
| `updated_at` | Last update timestamp |

## Authentication Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Authenticate a user and generate a JWT token |

## Authentication Flow

```text
User Registration
        ↓
Request Validation
        ↓
Duplicate User Check
        ↓
Password Hashing
        ↓
User Saved in PostgreSQL
        ↓
Registration Response
```

```text
User Login
      ↓
Email and Password Validation
      ↓
Password Verification
      ↓
JWT Access Token Generation
      ↓
Authenticated API Access
```

## Security Features

- Plain-text passwords are never stored.
- Passwords are stored only as secure hashes.
- Protected routes require a valid Bearer token.
- JWT token payloads identify the authenticated user.
- Invalid credentials are rejected.
- Inactive or unavailable users cannot access protected resources.

---

# Phase 2.2 – Profile and Digital Twin Management

## 2.2.1 – User Profile Management

The Profile module allows authenticated users to retrieve and maintain personal profile information.

### Profile Features

- Get the authenticated user's profile
- Update phone number
- Update biography
- Update date of birth
- Update timezone
- Update preferred language
- Return validated profile responses

### Profile Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/users/profile` | Retrieve the authenticated user's profile |
| `PUT` | `/users/profile` | Update profile information |
| `PATCH` | `/users/profile/avatar` | Upload or replace a profile avatar |
| `DELETE` | `/users/profile/avatar` | Delete the current profile avatar |

### Profile Update Example

```json
{
  "phone": "+919876543210",
  "bio": "AI and Machine Learning developer.",
  "timezone": "Asia/Kolkata",
  "language": "English"
}
```

## Avatar Management

The avatar module supports:

- Image upload using multipart form data
- Avatar replacement
- Avatar deletion
- Avatar URL storage
- Static avatar serving
- Authenticated avatar management

Avatar files are stored in:

```text
backend/static/avatars/
```

---

## 2.2.2 – Digital Twin Management

The Digital Twin module enables each authenticated user to create and configure a personalized AI identity.

### Digital Twin Features

- Create a Digital Twin
- Retrieve the authenticated user's Digital Twin
- Update Digital Twin information
- Delete a Digital Twin
- Allow only one Digital Twin per user
- Reject duplicate creation
- Reject empty updates
- Protect user ownership
- Use custom domain exceptions

### Digital Twin Fields

| Field | Description |
|---|---|
| `id` | Unique Digital Twin identifier |
| `user_id` | Owner of the Digital Twin |
| `twin_name` | Name of the AI Digital Twin |
| `personality` | Personality configuration |
| `communication_style` | Preferred communication style |
| `goals` | Goals assigned to the Digital Twin |
| `interests` | User interests used for personalization |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

### Digital Twin Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/digital-twin/` | Create a Digital Twin |
| `GET` | `/digital-twin/` | Retrieve the current user's Digital Twin |
| `PUT` | `/digital-twin/` | Update the Digital Twin |
| `DELETE` | `/digital-twin/` | Delete the Digital Twin |

### Create Digital Twin Example

```json
{
  "twin_name": "Anshul AI",
  "personality": "Friendly, analytical and curious.",
  "communication_style": "Professional",
  "goals": "Help users solve AI and software engineering problems.",
  "interests": "Artificial Intelligence, Machine Learning, Python and Data Science"
}
```

### Digital Twin Business Rules

- Each user can create only one Digital Twin.
- Duplicate Digital Twin creation returns `409 Conflict`.
- A missing Digital Twin returns `404 Not Found`.
- An empty update request returns `400 Bad Request`.
- Users can retrieve and modify only their own Digital Twin.

### Digital Twin Exception Mapping

| Exception | HTTP status |
|---|---:|
| `DigitalTwinAlreadyExistsException` | `409 Conflict` |
| `DigitalTwinNotFoundException` | `404 Not Found` |
| `EmptyUpdateException` | `400 Bad Request` |

---

# Phase 2.3 – Memory Management

## Overview

The Memory Management module enables a Digital Twin to store and retrieve long-term information associated with its authenticated user.

Every memory belongs to:

```text
Authenticated User
        ↓
Digital Twin
        ↓
Memory
```

The module supports complete CRUD operations, search, filtering, pagination, sorting, pagination metadata, ownership protection, exception handling, and automated lifecycle testing.

---

## Memory Features

- Create a memory
- Retrieve all memories
- Retrieve a memory by ID
- Update a memory
- Delete a memory
- Search memory titles
- Search memory content
- Filter by category
- Filter by importance
- Filter favorite memories
- Combine multiple filters
- Sort by supported fields
- Use ascending or descending order
- Paginate large result sets
- Return pagination metadata
- Protect user ownership
- Reject empty update requests
- Return standards-based HTTP errors

---

## Memory Model

| Field | Description |
|---|---|
| `id` | Unique Memory identifier |
| `user_id` | Owner of the Memory |
| `digital_twin_id` | Associated Digital Twin |
| `title` | Memory title |
| `content` | Detailed Memory content |
| `category` | Memory classification |
| `importance` | Importance level from 1 to 5 |
| `is_favorite` | Favorite-memory status |
| `created_at` | Memory creation timestamp |
| `updated_at` | Last update timestamp |

---

## Memory API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/memories/` | Create a new Memory |
| `GET` | `/memories/` | Retrieve, search, filter, sort, and paginate Memories |
| `GET` | `/memories/{memory_id}` | Retrieve a Memory by ID |
| `PUT` | `/memories/{memory_id}` | Update an existing Memory |
| `DELETE` | `/memories/{memory_id}` | Delete a Memory |

---

## Create Memory Example

```json
{
  "title": "Python Development",
  "content": "The user enjoys building backend APIs using Python and FastAPI.",
  "category": "Programming",
  "importance": 5,
  "is_favorite": true
}
```

Expected response:

```text
201 Created
```

---

## Search and Filtering

The Memory listing endpoint supports these optional query parameters:

| Parameter | Description |
|---|---|
| `search` | Search by Memory title or content |
| `category` | Filter by Memory category |
| `importance` | Filter by importance from 1 to 5 |
| `is_favorite` | Filter favorite or non-favorite Memories |
| `page` | Select the requested page |
| `page_size` | Set the number of records per page |
| `sort_by` | Select the sorting field |
| `sort_order` | Select ascending or descending order |

### Search Example

```text
GET /memories/?search=python
```

### Category Filter Example

```text
GET /memories/?category=Programming
```

### Importance Filter Example

```text
GET /memories/?importance=5
```

### Favorite Filter Example

```text
GET /memories/?is_favorite=true
```

### Combined Query Example

```text
GET /memories/?search=python&category=Programming&importance=5&is_favorite=true&page=1&page_size=10&sort_by=created_at&sort_order=desc
```

---

## Memory Pagination

Pagination uses:

```text
page

page_size
```

Example:

```text
GET /memories/?page=1&page_size=10
```

The pagination offset is calculated as:

```text
offset = (page - 1) × page_size
```

The maximum supported page size is:

```text
100 records
```

---

## Pagination Response

The Memory listing endpoint returns:

```json
{
  "items": [
    {
      "id": "memory-id",
      "user_id": "user-id",
      "digital_twin_id": "digital-twin-id",
      "title": "Python Development",
      "content": "The user enjoys building APIs using Python and FastAPI.",
      "category": "Programming",
      "importance": 5,
      "is_favorite": true,
      "created_at": "2026-07-10T10:00:00+00:00",
      "updated_at": "2026-07-10T10:00:00+00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

Pagination metadata includes:

| Field | Description |
|---|---|
| `items` | Memory records on the current page |
| `total` | Total matching Memory records |
| `page` | Current page number |
| `page_size` | Maximum records per page |
| `total_pages` | Total number of available pages |

---

## Memory Sorting

Supported sorting fields:

```text
created_at

updated_at

title

category

importance
```

Supported sort orders:

```text
asc

desc
```

Example:

```text
GET /memories/?sort_by=importance&sort_order=desc
```

---

## Memory Business Rules

- A Memory can be created only when the authenticated user has a Digital Twin.
- Every Memory belongs to an authenticated user.
- Every Memory is associated with a Digital Twin.
- Users can access only their own Memories.
- Memory importance must be between `1` and `5`.
- Empty Memory updates are rejected.
- Missing Memories return `404 Not Found`.
- Empty search results return `200 OK`.
- Empty search results contain an empty `items` list.
- Invalid query parameters return `422 Unprocessable Entity`.
- Page numbering starts at `1`.
- Page size is restricted to a maximum of `100`.

---

## Memory Exception Handling

| Exception | HTTP status |
|---|---:|
| `DigitalTwinNotFoundException` | `404 Not Found` |
| `MemoryNotFoundException` | `404 Not Found` |
| `EmptyMemoryUpdateException` | `400 Bad Request` |

---

# 🗄️ Database Relationships

```text
User
 │
 │ One-to-One
 ▼
Digital Twin
 │
 │ One-to-Many
 ▼
Memories
```

The database relationships support cascade deletion.

If a user or Digital Twin is deleted, related records can be removed according to the configured relationship and foreign-key behavior.

---

# 🧱 Backend Architecture

The backend follows a layered architecture:

```text
Client Request
      ↓
FastAPI Router
      ↓
Authentication Dependency
      ↓
Pydantic Validation
      ↓
CRUD/Service Logic
      ↓
SQLAlchemy ORM
      ↓
PostgreSQL Database
      ↓
Pydantic Response
      ↓
JSON API Response
```

Responsibilities are separated as follows:

| Layer | Responsibility |
|---|---|
| `api/` | HTTP routes and response mapping |
| `crud/` | Database operations and business logic |
| `models/` | SQLAlchemy database models |
| `schemas/` | Pydantic request and response validation |
| `database/` | Database engine, sessions, and Base |
| `dependencies/` | Reusable FastAPI dependencies |
| `exceptions/` | Domain-specific exceptions |
| `core/` | Configuration, logging, and security |
| `migrations/` | Alembic database migrations |
| `tests/` | Automated API and lifecycle tests |

---

# ⚙️ Local Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project:

```bash
cd NeuroTwin-AI
```

---

## 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r backend/requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
backend/.env
```

Add the required configuration using your local values:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/neurotwin
SECRET_KEY=replace_with_a_secure_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit `.env` to GitHub.

---

## 5. Apply Database Migrations

Move into the backend directory:

```powershell
cd backend
```

Run:

```powershell
alembic upgrade head
```

Verify the current migration:

```powershell
alembic current
```

---

## 6. Start the Backend Server

```powershell
uvicorn app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Swagger allows developers to:

- Inspect API endpoints
- View request schemas
- View response schemas
- Authorize using JWT
- Execute API requests
- Verify HTTP status codes

---

# 🧪 Automated Testing

Move into:

```powershell
cd backend
```

Run all tests:

```powershell
pytest -v
```

Run tests with concise output:

```powershell
pytest -q
```

Run Authentication tests:

```powershell
pytest tests/test_auth.py -v
```

Run Profile tests:

```powershell
pytest tests/test_profile.py -v
```

Run Digital Twin tests:

```powershell
pytest tests/test_digital_twin.py -v
```

Run Memory tests:

```powershell
pytest tests/test_memory.py -v
```

Run the complete Memory lifecycle test:

```powershell
pytest tests/test_memory.py::test_complete_memory_lifecycle -v
```

---

# ✅ Test Coverage

The current test suite verifies:

- User registration
- User login
- JWT authentication
- Protected endpoints
- Profile retrieval
- Profile updates
- Avatar upload
- Avatar deletion
- Digital Twin creation
- Duplicate Digital Twin prevention
- Digital Twin retrieval
- Digital Twin updates
- Empty Digital Twin update handling
- Digital Twin deletion
- Memory creation
- Memory retrieval
- Memory search
- Memory filtering
- Memory pagination
- Pagination metadata
- Memory sorting
- Memory updates
- Empty Memory update handling
- Memory deletion
- Missing Memory handling
- Complete Memory lifecycle

---

# 🔐 HTTP Status Codes

| Status | Meaning |
|---:|---|
| `200 OK` | Request completed successfully |
| `201 Created` | Resource created successfully |
| `400 Bad Request` | Invalid operation or empty update |
| `401 Unauthorized` | Authentication is missing or invalid |
| `404 Not Found` | Requested resource does not exist |
| `409 Conflict` | Resource already exists |
| `422 Unprocessable Entity` | Request validation failed |
| `500 Internal Server Error` | Unexpected server error |

---

# 🛣️ Development Roadmap

## Completed

- [x] Phase 2.1 – Authentication and User Management
- [x] Phase 2.2 – Profile and Digital Twin Management
- [x] Phase 2.3 – Memory Management

## Upcoming

- [ ] Phase 2.4 – Conversation Management
- [ ] Message Management
- [ ] Conversation History
- [ ] AI Response Generation
- [ ] Digital Twin Context Integration
- [ ] Memory Retrieval for AI Responses
- [ ] Vector Embeddings
- [ ] Semantic Memory Search
- [ ] Frontend Application
- [ ] Analytics Dashboard
- [ ] Production Deployment

---

# 🔮 Future Enhancements

Planned enhancements include:

- AI-powered Digital Twin conversations
- Conversation sessions
- User and assistant message history
- Context-aware response generation
- Long-term Memory retrieval
- Semantic Memory search
- Vector embeddings
- Personalized AI responses
- Memory summarization
- Memory relevance scoring
- Conversation analytics
- User dashboard
- Frontend integration
- Cloud deployment

---

# 👨‍💻 Author

**Anshul Deep Bajpai**

B.Tech Computer Science and Engineering  
Specialization: Artificial Intelligence and Machine Learning

Interests:

- Artificial Intelligence
- Machine Learning
- Data Science
- Python
- FastAPI
- Backend Development
- Generative AI

---

# 📄 License

This project is intended for educational, learning, research, and portfolio purposes.

---

# ⭐ Project Summary

NeuroTwin AI currently provides a secure and modular backend foundation with:

- JWT authentication
- User management
- Profile management
- Avatar management
- Personalized Digital Twins
- Long-term Memory management
- Search and filtering
- Pagination and sorting
- Custom exception handling
- PostgreSQL persistence
- Alembic migrations
- Swagger documentation
- Automated backend testing

The next major development stage is:

## Phase 2.4 – Conversation and Messaging System

Phase 2.4 introduces the core conversation infrastructure for NeuroTwin AI. Authenticated users can create and manage conversations associated with their Digital Twin and store structured user messages inside those conversations.

### Features Implemented

#### Conversation Management

- Create new conversations
- Retrieve a conversation by ID
- Retrieve all user-owned conversations
- Update conversation titles
- Archive and unarchive conversations
- Delete conversations
- Search conversations by title
- Filter conversations by archive status
- Sort conversations by:
  - Creation date
  - Update date
  - Title
- Paginated conversation results
- User ownership validation
- JWT-protected endpoints

#### Message Management

- Create user messages inside conversations
- Retrieve conversation message history
- Retrieve individual messages
- Delete messages
- Filter messages by role
- Sort messages chronologically
- Paginated message history
- Conversation ownership validation
- Message ownership validation
- JWT-protected endpoints

#### Message Role Security

Public API users can create only:

- `user` messages

The following roles are protected for future internal AI services:

- `assistant`
- `system`

This prevents clients from impersonating the NeuroTwin AI assistant or injecting system messages.

### Database Tables

Phase 2.4 adds:

- `conversations`
- `messages`

Database relationships:

```text
User
 └── Digital Twin
      └── Conversations
           └── Messages 

## Phase 2.5 – AI Chat Engine

Phase 2.5 introduces the core AI conversation engine for NeuroTwin AI. It connects the authenticated user's Digital Twin, saved memories, and recent conversation history to generate personalized AI responses.

### Completed Features

- AI provider configuration using environment variables
- Secure OpenAI API key configuration
- OpenAI client integration
- Configurable AI model
- Configurable temperature and token limits
- AI request timeout handling
- Digital Twin personality prompt generation
- Relevant user memory retrieval
- Memory-aware AI context generation
- Recent conversation history integration
- Configurable conversation history limits
- AI context builder
- User-message database storage
- Assistant-message database storage
- Personalized AI response generation
- Authenticated AI chat endpoint
- Conversation ownership validation
- Digital Twin ownership validation
- AI provider exception handling
- OpenAI authentication error handling
- OpenAI rate-limit and quota handling
- AI service availability handling
- Database rollback and failed-message cleanup
- AI chat request and response schemas
- Swagger API integration
- Automated AI chat tests

### AI Chat Processing Flow

```text
Authenticated User
        |
        v
Conversation Validation
        |
        v
Digital Twin Configuration
        |
        v
Digital Twin Personality Prompt
        |
        v
Relevant Saved Memories
        |
        v
Recent Conversation History
        |
        v
Complete AI Context
        |
        v
OpenAI API
        |
        v
Personalized AI Response
        |
        v
Store User and Assistant Messages
        |
        v
Return Chat Response

## Phase 2.6 – AI Intelligence and Memory System

Phase 2.6 extends NeuroTwin AI with intelligent provider fallback,
automatic long-term memory extraction, duplicate prevention, memory
updates, and conversation summarization.

### Completed Features

- OpenAI integration
- Ollama local AI fallback
- Automatic OpenAI-to-Ollama provider fallback
- Structured memory extraction from user messages
- AI memory validation using Pydantic
- Automatic long-term memory storage
- Duplicate memory prevention
- Intelligent memory updates
- Memory importance scoring from 1 to 5
- Conversation summarization
- Conversation summary database storage
- Previous summary integration into future AI context
- Graceful AI and memory-processing failure handling
- Automated memory and summarization tests

### AI Processing Flow

```text
User Message
      |
      v
OpenAI Provider
      |
      | Provider unavailable or quota exceeded
      v
Ollama Local Fallback
      |
      v
Personalized AI Response
      |
      v
Automatic Memory Extraction
      |
      +--> Duplicate Memory --> Skip
      |
      +--> Related Memory --> Update
      |
      +--> New Memory --> Save
      |
      v
Conversation Summarization
      |
      v
Summary Stored for Future AI Context