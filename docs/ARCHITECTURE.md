# System Architecture Documentation

## Overview

ZOE NutriTech follows a **layered architecture** with clear separation of concerns, making it scalable, maintainable, and extensible.

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Technology**: HTML, CSS, JavaScript, Bootstrap 5

**Components**:
- Templates (Jinja2)
- Static assets
- Client-side JavaScript
- Responsive UI components

**Responsibilities**:
- User interface rendering
- User interaction handling
- API calls to backend
- Client-side validation

### 2. Application Layer (Backend)

**Technology**: Flask (Python)

**Components**:
- Route handlers (`app/routes/`)
- Request/response processing
- Session management
- Authentication/authorization

**Responsibilities**:
- HTTP request handling
- Business logic orchestration
- Data validation
- Error handling

### 3. Business Logic Layer (Services)

**Technology**: Python

**Components**:
- Recommendation Engine
- Search Engine
- Chatbot Service
- Price API Service
- Offline Manager

**Responsibilities**:
- Core business logic
- Algorithm implementation
- External API integration
- Data processing

### 4. Data Access Layer (Models)

**Technology**: SQLAlchemy ORM

**Components**:
- Database models (`app/models.py`)
- Query builders
- Data relationships

**Responsibilities**:
- Database abstraction
- Data persistence
- Query optimization
- Data validation

### 5. Data Storage Layer

**Technology**: SQLite (dev) / PostgreSQL (prod)

**Components**:
- Database tables
- Indexes
- Constraints

**Responsibilities**:
- Data storage
- Data integrity
- Performance optimization

## System Components

### Core Modules

```
app/
├── __init__.py              # Application factory
├── models.py                # Database models
├── routes/                   # URL routing
│   ├── auth.py              # Authentication
│   ├── main.py              # Main routes
│   ├── recommendations.py  # Recommendations
│   ├── diabetes.py          # Diabetes management
│   ├── chatbot.py           # Chat interface
│   ├── search.py            # Search functionality
│   ├── goals.py             # Goal tracking
│   └── api.py               # REST API
├── services/                # Business logic
│   ├── recommendation_engine.py
│   ├── search_engine.py
│   ├── chatbot_service.py
│   ├── price_api.py
│   └── offline_manager.py
└── utils/                   # Utilities
    └── data_initializer.py
```

## Data Flow

### 1. User Request Flow

```
User Browser
    ↓
Flask Routes (app/routes/)
    ↓
Authentication Check
    ↓
Service Layer (app/services/)
    ↓
Data Models (app/models.py)
    ↓
Database (SQLite/PostgreSQL)
    ↓
Response Generation
    ↓
Template Rendering
    ↓
User Browser
```

### 2. Recommendation Generation Flow

```
User Request
    ↓
Recommendation Route
    ↓
Recommendation Engine Service
    ↓
    ├── User Profile Analysis
    ├── Food Database Query
    ├── Scoring Algorithm
    │   ├── Rule-Based Scoring
    │   └── ML-Based Scoring
    ├── Result Ranking
    └── Explanation Generation
    ↓
Database Storage
    ↓
Response to User
```

### 3. Search Flow

```
User Query
    ↓
Search Route
    ↓
Search Engine Service
    ↓
    ├── Query Tokenization
    ├── Stop Word Removal
    ├── Database Query
    ├── Relevance Scoring
    └── Result Ranking
    ↓
Response to User
```

## Database Schema

### Core Tables

**users**
- User accounts and profiles
- Health information
- Preferences

**food_items**
- Food database
- Nutritional information
- Prices

**recommendations**
- Generated recommendations
- User interactions
- Explanations

**diabetes_records**
- Blood glucose readings
- Insulin records
- HbA1c values

**goals**
- User goals
- Progress tracking

**food_logs**
- User food consumption
- Meal tracking

**chat_history**
- Chatbot conversations
- Intent/entity tracking

**food_prices**
- Price history
- Market data

## External Integrations

### 1. Food Price API
- **Purpose**: Real-time market prices
- **Integration**: REST API
- **Frequency**: Daily updates
- **Fallback**: Cached prices

### 2. Medical System (Type 1 Diabetes)
- **Purpose**: Insulin recommendations
- **Integration**: REST API
- **Protocol**: HL7 FHIR (future)
- **Security**: Encrypted communication

### 3. Diet Therapist System
- **Purpose**: Professional consultation
- **Integration**: REST API
- **Features**: Appointment scheduling, reports

## Scalability Architecture

### Horizontal Scaling

1. **Load Balancer**: Distribute requests
2. **Multiple App Servers**: Gunicorn workers
3. **Database Replication**: Read replicas
4. **Caching Layer**: Redis for sessions/cache

### Vertical Scaling

1. **Database Optimization**: Indexes, query optimization
2. **Caching**: Redis, Memcached
3. **CDN**: Static asset delivery
4. **Database Connection Pooling**

## Security Architecture

### Authentication
- Flask-Login for session management
- Password hashing (bcrypt)
- CSRF protection

### Authorization
- Role-based access control
- Route protection
- API key authentication

### Data Security
- Encrypted connections (HTTPS)
- SQL injection prevention (ORM)
- XSS protection (template escaping)
- Input validation

## Deployment Architecture

### Development
```
Local Machine
    ├── Flask Development Server
    ├── SQLite Database
    └── Local File Storage
```

### Production
```
Load Balancer (Nginx)
    ↓
Application Servers (Gunicorn)
    ├── App Instance 1
    ├── App Instance 2
    └── App Instance N
    ↓
Database (PostgreSQL)
    ├── Primary
    └── Replica
    ↓
Cache (Redis)
    ↓
File Storage (S3/Local)
```

## Monitoring & Logging

### Application Monitoring
- Error tracking
- Performance metrics
- User activity
- API usage

### Database Monitoring
- Query performance
- Connection pool status
- Storage usage

### System Monitoring
- Server resources
- Network traffic
- Uptime monitoring

## Backup & Recovery

### Database Backups
- Daily automated backups
- Point-in-time recovery
- Backup verification

### Data Recovery
- Restore procedures
- Disaster recovery plan
- Data integrity checks

## Performance Optimization

### Caching Strategy
- **Redis**: Session data, frequently accessed data
- **Browser Cache**: Static assets
- **Application Cache**: Computed results

### Database Optimization
- Indexes on frequently queried columns
- Query optimization
- Connection pooling
- Read replicas for read-heavy operations

### Code Optimization
- Lazy loading
- Pagination
- Async operations (where applicable)

## Future Architecture Enhancements

1. **Microservices**: Split into independent services
2. **Message Queue**: Celery for async tasks
3. **API Gateway**: Centralized API management
4. **Containerization**: Docker deployment
5. **Kubernetes**: Orchestration for scaling
6. **CDN**: Global content delivery

## Technology Stack

### Backend
- **Framework**: Flask 3.0
- **ORM**: SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: Flask-Login
- **Migrations**: Flask-Migrate

### Frontend
- **Templates**: Jinja2
- **CSS Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS + jQuery
- **Icons**: Font Awesome

### Services
- **ML**: scikit-learn, pandas, numpy
- **NLP**: transformers (future), nltk
- **API**: requests
- **Task Queue**: Celery (future)

### Deployment
- **WSGI Server**: Gunicorn
- **Reverse Proxy**: Nginx
- **Process Manager**: systemd/supervisor

## Development Workflow

1. **Local Development**: Flask dev server
2. **Testing**: pytest (to be implemented)
3. **Staging**: Production-like environment
4. **Production**: Gunicorn + Nginx

## API Architecture

### RESTful Design
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- JSON responses
- Status codes

### API Versioning
- URL versioning: `/api/v1/`
- Future: `/api/v2/`

### Rate Limiting
- Per-user limits
- API key limits
- IP-based limits

