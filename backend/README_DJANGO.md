# Django Backend - Healthcare Portal

A modern Django REST API backend for the healthcare portal with MongoDB support.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MongoDB running on your system
- pip (Python package manager)

### Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Update .env with your MongoDB URI
# MONGO_URI=mongodb://localhost:27017/

# 6. Run development server
python manage.py runserver 0.0.0.0:8000
```

Server will be available at `http://localhost:8000`

## 📁 Project Structure

```
backend/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── healthcare/              # Django project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── api/                     # Main API application
│   ├── models.py            # MongoEngine models (User, PatientProfile, ProviderProfile)
│   ├── serializers.py       # DRF serializers
│   ├── authentication.py    # JWT authentication
│   ├── exceptions.py        # Custom exceptions
│   ├── views/               # API views
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── patients.py      # Patient endpoints
│   │   └── providers.py     # Provider endpoints
│   └── urls/                # URL patterns
│       ├── auth.py          # Auth URLs
│       ├── patients.py      # Patient URLs
│       └── providers.py     # Provider URLs
└── Dockerfile              # Docker configuration
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT token
- `POST /api/auth/logout/` - Logout (requires authentication)
- `GET /api/auth/profile/` - Get current user profile

### Patients
- `GET /api/patients/` - List all patients (provider/admin only)
- `GET /api/patients/{patient_id}/` - Get patient details
- `PUT /api/patients/{patient_id}/update/` - Update patient profile

### Providers
- `GET /api/providers/` - List all providers
- `GET /api/providers/{provider_id}/` - Get provider details
- `POST /api/providers/create/` - Create provider profile
- `PUT /api/providers/{provider_id}/update/` - Update provider profile

### Health Check
- `GET /health/` - Server health status

## 🔐 Authentication

All endpoints except `/register/` and `/login/` require JWT authentication.

Include token in request header:
```
Authorization: Bearer <your-jwt-token>
```

## 🗄️ Database

Uses **MongoDB** with **MongoEngine** ORM.

### Collections
- **users** - User accounts
- **patient_profiles** - Patient data
- **provider_profiles** - Provider/doctor data

### Models

**User**
```python
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password_hash": "hashed_password",
  "role": "patient|provider|admin",
  "consent_given": boolean,
  "is_active": boolean,
  "created_at": datetime,
  "updated_at": datetime
}
```

**PatientProfile**
```python
{
  "_id": ObjectId,
  "user_id": "user_mongodb_id",
  "wellness_goals": {},
  "appointments": [],
  "health_data": {},
  "medical_history": [],
  "allergies": [],
  "medications": [],
  "created_at": datetime,
  "updated_at": datetime
}
```

**ProviderProfile**
```python
{
  "_id": ObjectId,
  "user_id": "user_mongodb_id",
  "specialty": "Cardiology",
  "license_number": "LIC123456",
  "qualifications": ["MD", "Board Certified"],
  "experience_years": "10",
  "clinic_address": "123 Medical St",
  "phone": "+1-555-0000",
  "available_hours": {},
  "patients": ["patient_id_1", "patient_id_2"],
  "created_at": datetime,
  "updated_at": datetime
}
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t healthcare-backend:latest .
```

### Run Container
```bash
docker run -e MONGO_URI=mongodb://host.docker.internal:27017/ \
           -e JWT_SECRET=your-secret \
           -p 8000:8000 \
           healthcare-backend:latest
```

## 📊 Dependencies

Key packages:
- **Django** - Web framework
- **djangorestframework** - REST API toolkit
- **MongoEngine** - MongoDB ORM
- **PyJWT** - JWT authentication
- **bcrypt** - Password hashing
- **django-cors-headers** - CORS support
- **pymongo** - MongoDB driver

## 🔧 Configuration

Edit `healthcare/settings.py` for:
- Debug mode
- Allowed hosts
- CORS settings
- JWT expiration time
- Database connection

## 📝 Logging

Configured in `healthcare/settings.py`:
- Console output for errors and info
- Separate loggers for Django and API

View logs:
```bash
tail -f <logfile>
```

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [MongoEngine](http://mongoengine.org/)
- [JWT](https://jwt.io/)

## 🤝 Contributing

1. Create a new branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

MIT License
