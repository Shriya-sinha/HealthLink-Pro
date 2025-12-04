# Healthcare Portal - Full Stack Application

A modern healthcare portal built with Django REST Framework, React, and MongoDB. Deploy quickly with Docker Compose.

---

## 🏗️ Project Structure

```
hcl_tech/
├── backend/                    # Django REST API
│   ├── manage.py              # Django management
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Backend container
│   ├── api/                   # API endpoints
│   │   ├── authentication.py  # Auth logic
│   │   ├── models.py          # Data models
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views/             # API views
│   │   └── urls/              # URL routing
│   ├── middleware/            # Custom middleware
│   ├── healthcare/            # Django settings
│   └── db.sqlite3             # SQLite database
│
├── frontend/                  # React + Vite application
│   ├── src/
│   │   ├── App.jsx           # Main component
│   │   ├── main.jsx          # Entry point
│   │   ├── components/       # UI components
│   │   │   ├── LoginForm.jsx
│   │   │   ├── HealthDashboard.jsx
│   │   │   └── InfoCard.jsx
│   │   ├── context/          # Context API
│   │   │   └── AuthContext.jsx
│   │   └── assets/           # Images, fonts
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite config
│   ├── Dockerfile            # Frontend container
│   └── index.html            # HTML entry
│
└── docker-compose.yaml        # Docker Compose config
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Setup

```bash
# 1. Navigate to project
cd /path/to/hcl_tech

# 2. Start all services (creates .env files from examples on first run)
docker-compose up -d

# 3. Verify services are running
docker-compose ps
```

### Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Database**: localhost:27017 (MongoDB)

### View Logs & Stop

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down
docker-compose down -v  # Remove all data
```

---

## 📡 API Details

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Patients

- `GET /api/patients` - List all patients
- `GET /api/patients/<id>` - Get patient details
- `POST /api/patients` - Create patient
- `PUT /api/patients/<id>` - Update patient
- `DELETE /api/patients/<id>` - Delete patient

### Providers

- `GET /api/providers` - List all providers
- `POST /api/providers` - Create provider
- `PUT /api/providers/<id>` - Update provider

### Authentication Flow

1. **Login**: POST `/api/auth/login` with email & password
2. **Token**: Receive JWT token in response
3. **Storage**: Token saved in browser localStorage
4. **Usage**: Token sent in `Authorization: Bearer <token>` header

---

## 🏛️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│ Frontend (React + Vite) - Port 5173                     │
│ ├─ Login/Register                                       │
│ ├─ Health Dashboard                                     │
│ └─ Patient Management                                   │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST
                       │ (JWT Auth)
                       ↓
┌─────────────────────────────────────────────────────────┐
│ Backend (Django REST) - Port 8000                       │
│ ├─ Authentication API                                   │
│ ├─ Patient CRUD                                         │
│ ├─ Provider Management                                  │
│ └─ JWT Middleware                                       │
└──────────────────────┬──────────────────────────────────┘
                       │ MongoDB Queries
                       ↓
┌─────────────────────────────────────────────────────────┐
│ MongoDB - Port 27017                                    │
│ ├─ users collection                                     │
│ ├─ patients collection                                  │
│ └─ providers collection                                 │
└─────────────────────────────────────────────────────────┘
```

### Services

| Service | Port | Technology |
|---------|------|------------|
| Backend | 8000 | Django REST |
| Frontend | 5173 | React + Vite |
| Database | 27017 | MongoDB |

### Environment Variables

**Backend (.env)**
```env
DEBUG=True
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://mongodb:27017/healthcare
```

**Frontend (via Vite)**
```env
VITE_API_URL=http://localhost:8000
```
