# ZOE NutriTech - Smart Nutrition & Diabetes Support System

## Overview

ZOE NutriTech is a comprehensive smart nutrition and diabetes support system designed specifically for Uganda. The system provides personalized food recommendations based on local, affordable Ugandan foods, with specialized support for both Type 1 and Type 2 diabetes management.

## Key Features

### 🎯 Dual-Purpose System
- **Diabetes Support**: Comprehensive management for Type 1 and Type 2 diabetes
- **Health & Nutrition**: Support for healthy eating, weight loss, and weight gain goals

### 🤖 AI-Powered Recommendations
- Hybrid recommendation engine combining ML and rule-based logic
- Personalized food suggestions based on:
  - Health conditions (diabetes type, goals)
  - Budget constraints
  - Nutritional requirements
  - Local food availability

### 💬 NLP Conversational Interface
- Natural language chatbot for dietary conversations
- Intent detection and entity extraction
- Context-aware responses about nutrition, recipes, and health

### 🔍 Advanced Search Engine
- Full-text search with autocomplete
- Nutritional filtering (protein, carbs, fiber, GI)
- Budget-based filtering
- Category-based search

### 📊 Diabetes Management
- **Type 1**: Insulin recommendation support with external system integration
- **Type 2**: Health monitoring and improvement tracking
- Blood glucose tracking
- HbA1c monitoring
- Progress analytics

### 💰 Budget Integration
- Real-time food price tracking
- Budget-aware recommendations
- Market price API integration
- Cost estimation for meals

### 📱 Offline Support
- Offline mode for low-connectivity areas
- Cached data for essential features
- Synchronization when online

### 📈 Goal Tracking
- Weight management goals
- Blood glucose control goals
- Progress visualization
- Metrics dashboard

## System Architecture

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login

### Frontend
- **Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS with jQuery
- **Icons**: Font Awesome
- **Responsive Design**: Mobile-first approach

### Services Layer
- **Recommendation Engine**: ML + Rule-based hybrid system
- **Search Engine**: Full-text and semantic search
- **Chatbot Service**: NLP-based conversational interface
- **Price API Service**: Market price integration
- **Offline Manager**: Offline mode and sync

### Data Pipeline
- Food data initialization
- Price updates (daily)
- User data synchronization
- Recommendation generation

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd Testing2
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///zoenutritech.db
FLASK_ENV=development
FOOD_PRICE_API_URL=https://api.example.com/prices
FOOD_PRICE_API_KEY=your-api-key
```

5. **Initialize database**
```bash
python run.py
```
The database will be created automatically on first run.

6. **Run the application**
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
Testing2/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                 # Database models
│   ├── routes/                   # Route handlers
│   │   ├── auth.py              # Authentication routes
│   │   ├── main.py              # Main routes (dashboard, profile)
│   │   ├── recommendations.py   # Recommendation routes
│   │   ├── diabetes.py          # Diabetes management routes
│   │   ├── chatbot.py           # Chatbot routes
│   │   ├── search.py            # Search routes
│   │   ├── goals.py             # Goal tracking routes
│   │   └── api.py               # API endpoints
│   ├── services/                # Business logic services
│   │   ├── recommendation_engine.py
│   │   ├── search_engine.py
│   │   ├── chatbot_service.py
│   │   ├── price_api.py
│   │   └── offline_manager.py
│   └── utils/
│       └── data_initializer.py  # Initial data setup
├── templates/                    # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── auth/
│   ├── recommendations/
│   ├── diabetes/
│   ├── chatbot/
│   ├── search/
│   └── goals/
├── models/                       # ML models (generated)
├── offline_cache/                # Offline data cache
├── requirements.txt
├── run.py                        # Application entry point
└── README.md
```

## Usage Guide

### For Users

1. **Registration & Onboarding**
   - Create an account
   - Complete profile with health information
   - Set primary goals and budget

2. **Getting Recommendations**
   - Visit Recommendations page
   - Filter by meal type
   - Accept/reject recommendations
   - View detailed explanations

3. **Diabetes Management** (if applicable)
   - Record blood glucose readings
   - Track insulin (Type 1)
   - Monitor progress
   - View analytics

4. **Using Chat Assistant**
   - Ask questions about nutrition
   - Get food recommendations
   - Learn about diabetes management
   - Get budget-friendly suggestions

5. **Goal Tracking**
   - Create health goals
   - Update progress regularly
   - View progress charts
   - Celebrate achievements

### For Developers

See detailed documentation in:
- `docs/RECOMMENDATION_SYSTEM.md` - Recommendation engine details
- `docs/NLP_CHATBOT.md` - NLP chatbot implementation
- `docs/SEARCH_ENGINE.md` - Search engine architecture
- `docs/ML_TECHNIQUES.md` - Machine learning approaches
- `docs/ARCHITECTURE.md` - System architecture
- `docs/STORAGE.md` - Storage architecture

## API Endpoints

### Public Endpoints
- `GET /` - Landing page
- `GET /auth/register` - Registration
- `GET /auth/login` - Login
- `GET /api/health` - Health check

### Protected Endpoints (Require Authentication)
- `GET /dashboard` - User dashboard
- `GET /recommendations` - Food recommendations
- `POST /recommendations/api/generate` - Generate recommendations
- `GET /search` - Search foods
- `GET /chatbot` - Chat interface
- `POST /chatbot/message` - Send chat message
- `GET /diabetes/dashboard` - Diabetes dashboard
- `POST /diabetes/record` - Record diabetes data
- `GET /goals` - List goals
- `POST /goals/create` - Create goal

### API Endpoints (REST)
- `GET /api/foods` - List foods
- `GET /api/foods/<id>` - Get food details
- `GET /api/recommendations` - Get recommendations
- `POST /api/prices/update` - Update prices (API key required)
- `POST /api/offline/enable` - Enable offline mode
- `POST /api/offline/disable` - Disable offline mode

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Environment (development/production)
- `FOOD_PRICE_API_URL`: Food price API endpoint
- `FOOD_PRICE_API_KEY`: API key for price service

### Database Configuration
Default: SQLite (development)
Production: PostgreSQL recommended

## Testing

```bash
# Run tests (when implemented)
python -m pytest tests/
```

## Deployment

### Production Checklist
- [ ] Set strong SECRET_KEY
- [ ] Use PostgreSQL database
- [ ] Configure proper CORS settings
- [ ] Set up SSL/HTTPS
- [ ] Configure production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure backup strategy

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Specify your license here]

## Support

For support, email support@zoenutritech.ug or open an issue in the repository.

## Acknowledgments

- Ugandan food database contributors
- Medical advisors for diabetes management features
- Open source community

---

**Note**: This system is designed for educational and support purposes. Medical advice should always be obtained from qualified healthcare professionals.

