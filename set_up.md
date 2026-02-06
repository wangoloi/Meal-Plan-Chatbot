# ZOE NutriTech - Complete Development Setup Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [VS Code Setup](#vs-code-setup)
4. [Project Initialization](#project-initialization)
5. [Step-by-Step Development Process](#step-by-step-development-process)
6. [ML Model Integration](#ml-model-integration)
7. [Testing and Verification](#testing-and-verification)
8. [Deployment](#deployment)

---

## Overview

This guide provides complete step-by-step instructions for developing the ZOE NutriTech system from scratch, including integration with machine learning models. The system is a Flask-based web application for smart nutrition and diabetes support.

---

## Prerequisites

### Required Software
1. **Python 3.8+** (Python 3.14 used in this project)
2. **VS Code** (Visual Studio Code)
3. **Git** (optional, for version control)
4. **Web Browser** (Chrome, Firefox, or Edge)

### Required Python Packages
- Flask 3.0+
- Flask-SQLAlchemy
- Flask-Login
- Flask-Migrate
- Flask-WTF
- pandas, numpy
- scikit-learn (for ML models)
- waitress (for production server)

---

## VS Code Setup

### Step 1: Install VS Code Extensions

Open VS Code and install these essential extensions:

1. **Python** (by Microsoft)
   - Provides Python language support
   - Install from Extensions marketplace (Ctrl+Shift+X)

2. **Python Debugger** (by Microsoft)
   - For debugging Flask applications

3. **Pylance** (by Microsoft)
   - Enhanced Python IntelliSense

4. **Flask Snippets** (optional)
   - Code snippets for Flask development

### Step 2: Configure VS Code Settings

Create `.vscode/settings.json` in your project root:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.typeCheckingMode": "basic",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

### Step 3: Create VS Code Launch Configuration

Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "run.py",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true,
            "justMyCode": true
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

---

## Project Initialization

### Step 1: Create Project Directory

```bash
# Create project folder
mkdir zoenutritech
cd zoenutritech
```

### Step 2: Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Create Project Structure

Create the following directory structure:

```
zoenutritech/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── recommendations.py
│   │   ├── diabetes.py
│   │   ├── chatbot.py
│   │   ├── search.py
│   │   ├── goals.py
│   │   └── api.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── recommendation_engine.py
│   │   ├── search_engine.py
│   │   ├── chatbot_service.py
│   │   ├── price_api.py
│   │   └── offline_manager.py
│   └── utils/
│       └── data_initializer.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── onboarding.html
│   ├── profile.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── recommendations/
│   │   └── list.html
│   ├── search/
│   │   └── results.html
│   ├── chatbot/
│   │   └── chat.html
│   ├── diabetes/
│   │   ├── dashboard.html
│   │   ├── record.html
│   │   └── progress.html
│   └── goals/
│       ├── list.html
│       ├── create.html
│       └── view.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── models/
├── instance/
├── offline_cache/
├── uploads/
├── docs/
├── .env
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

### Step 4: Install Dependencies

Create `requirements.txt`:

```txt
# Core Flask dependencies
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
Flask-Migrate>=4.0.5
Flask-Login>=0.6.3
Flask-WTF>=1.2.1
WTForms>=3.1.1
Werkzeug>=3.0.1

# Essential utilities
requests>=2.31.0
python-dotenv>=1.0.0
python-dateutil>=2.8.2

# Data processing
pandas>=2.0.0
numpy>=1.24.0

# ML/AI packages
scikit-learn>=1.3.0
joblib>=1.3.0
nltk>=3.8.0

# Production server
waitress>=2.1.0

# Other utilities
beautifulsoup4>=4.12.0
Pillow>=10.0.0
bcrypt>=4.0.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Step-by-Step Development Process

### Phase 1: Core Application Setup

#### Step 1.1: Initialize Flask Application

Create `app/__init__.py`:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='development'):
    import os
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app = Flask(__name__, 
                template_folder=os.path.join(basedir, 'templates'),
                static_folder=os.path.join(basedir, 'static'))
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'sqlite:///zoenutritech.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    # ... register other blueprints
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    
    # Initialize database
    with app.app_context():
        db.create_all()
        from app.utils.data_initializer import initialize_default_data
        initialize_default_data()
    
    return app
```

#### Step 1.2: Create Database Models

Create `app/models.py` with all models:
- User
- FoodItem
- Recommendation
- DiabetesRecord
- Goal
- FoodLog
- ChatHistory
- FoodPrice

(Refer to existing `app/models.py` for complete implementation)

#### Step 1.3: Create Routes

Create route files in `app/routes/`:
- `auth.py` - Authentication routes
- `main.py` - Main routes (dashboard, profile)
- `recommendations.py` - Recommendation routes
- `diabetes.py` - Diabetes management routes
- `chatbot.py` - Chatbot routes
- `search.py` - Search routes
- `goals.py` - Goal tracking routes
- `api.py` - API endpoints

(Refer to existing route files for complete implementation)

### Phase 2: Service Layer Development

#### Step 2.1: Recommendation Engine

Create `app/services/recommendation_engine.py`:

**Key Components:**
1. **Rule-Based Scoring System**
   - Diabetes considerations (GI-based scoring)
   - Goal-based scoring (weight loss/gain)
   - Budget considerations
   - Nutritional completeness

2. **ML-Based Scoring** (when sklearn available)
   - Feature extraction
   - Similarity calculations
   - User preference learning

**Implementation Steps:**

```python
# 1. Import required libraries
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime
from app import db
from app.models import FoodItem, Recommendation, FoodLog, User

# 2. Create RecommendationEngine class
class RecommendationEngine:
    def __init__(self):
        self.model_dir = 'models'
        os.makedirs(self.model_dir, exist_ok=True)
        self.scaler = StandardScaler()
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self._load_or_train_model()
    
    # 3. Implement scoring algorithm
    def _calculate_food_score(self, user, food, meal_type):
        score = 50.0  # Base score
        reasoning_parts = []
        
        # Rule-based scoring
        if user.has_diabetes:
            if food.glycemic_index and food.glycemic_index < 55:
                score += 30
                reasoning_parts.append("Low GI helps maintain stable blood sugar")
        
        # Goal-based scoring
        if user.primary_goal == 'lose_weight':
            if food.calories and food.calories < 100:
                score += 15
        
        # Budget considerations
        if user.monthly_budget:
            daily_budget = user.monthly_budget / 30
            if food.current_price <= daily_budget * 0.1:
                score += 15
        
        reasoning = ". ".join(reasoning_parts)
        return max(0, score), reasoning
    
    # 4. Generate recommendations
    def generate_recommendations(self, user, meal_type='all', limit=10):
        # Filter foods
        query = FoodItem.query.filter_by(is_affordable=True)
        all_foods = query.all()
        
        # Score each food
        scored_foods = []
        for food in all_foods:
            score, reasoning = self._calculate_food_score(user, food, meal_type)
            if score > 0:
                scored_foods.append((food, score, reasoning))
        
        # Sort and return top recommendations
        scored_foods.sort(key=lambda x: x[1], reverse=True)
        # ... create Recommendation objects
        return recommendations
```

#### Step 2.2: Search Engine

Create `app/services/search_engine.py`:

**Implementation:**
- Full-text search with relevance scoring
- Autocomplete functionality
- Nutritional filtering
- Category-based search

#### Step 2.3: Chatbot Service

Create `app/services/chatbot_service.py`:

**Implementation:**
- Intent detection (keyword-based)
- Entity extraction
- Response generation
- Conversation history

### Phase 3: Frontend Development

#### Step 3.1: Base Template

Create `templates/base.html`:
- Bootstrap 5 framework
- Navigation bar
- Footer
- Flash message handling
- Responsive design

#### Step 3.2: Page Templates

Create templates for:
- Landing page (`index.html`)
- Dashboard (`dashboard.html`)
- Authentication pages (`auth/login.html`, `auth/register.html`)
- Feature pages (recommendations, search, chatbot, etc.)

### Phase 4: Data Initialization

#### Step 4.1: Food Database

Create `app/utils/data_initializer.py`:

```python
from app import db
from app.models import FoodItem
from datetime import datetime

def initialize_default_data():
    if FoodItem.query.first():
        return
    
    ugandan_foods = [
        {
            'name': 'Matooke (Plantain)',
            'local_name': 'Matooke',
            'category': 'grains',
            'calories': 122,
            'protein': 1.3,
            'carbohydrates': 31.9,
            'fiber': 2.3,
            'glycemic_index': 45,
            'diabetes_friendly': True,
            'current_price': 3000,
            'price_unit': 'kg'
        },
        # ... more foods
    ]
    
    for food_data in ugandan_foods:
        food = FoodItem(**food_data)
        food.price_last_updated = datetime.utcnow()
        db.session.add(food)
    
    db.session.commit()
```

---

## ML Model Integration

### Overview

The system uses a hybrid approach combining rule-based logic with machine learning models for recommendations.

### Step 1: Prepare Training Data

#### 1.1: Collect User Interaction Data

```python
# Structure for training data
training_data = {
    'user_features': [
        'age', 'gender', 'bmi', 'has_diabetes', 
        'diabetes_type', 'primary_goal', 'activity_level', 
        'budget_range', 'monthly_budget'
    ],
    'food_features': [
        'calories', 'protein', 'carbohydrates', 'fiber', 
        'fat', 'sugar', 'glycemic_index', 'current_price'
    ],
    'interactions': [
        # User accepted/rejected recommendations
        {'user_id': 1, 'food_id': 5, 'accepted': True, 'timestamp': '...'},
        # ...
    ]
}
```

#### 1.2: Feature Engineering

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def prepare_features(users, foods, interactions):
    # User features
    user_features = []
    for user in users:
        features = [
            user.age or 30,
            encode_gender(user.gender),
            user.calculate_bmi() or 22,
            1 if user.has_diabetes else 0,
            encode_diabetes_type(user.diabetes_type),
            encode_goal(user.primary_goal),
            encode_activity(user.activity_level),
            encode_budget(user.budget_range),
            user.monthly_budget or 0
        ]
        user_features.append(features)
    
    # Food features
    food_features = []
    for food in foods:
        features = [
            food.calories or 0,
            food.protein or 0,
            food.carbohydrates or 0,
            food.fiber or 0,
            food.fat or 0,
            food.sugar or 0,
            food.glycemic_index or 50,
            food.current_price or 0
        ]
        food_features.append(features)
    
    return np.array(user_features), np.array(food_features)
```

### Step 2: Train ML Models

#### 2.1: Collaborative Filtering Model

```python
from sklearn.decomposition import NMF
from sklearn.metrics import mean_squared_error
import numpy as np

def train_collaborative_filtering(user_item_matrix, n_components=50):
    """
    Train Non-negative Matrix Factorization model
    for collaborative filtering
    """
    from sklearn.decomposition import NMF
    
    # Create user-item matrix
    # Rows = users, Columns = foods
    # Values = ratings (1 = accepted, 0 = rejected, NaN = no interaction)
    
    # Initialize and train NMF
    model = NMF(n_components=n_components, random_state=42)
    W = model.fit_transform(user_item_matrix)
    H = model.components_
    
    # Save model
    import joblib
    joblib.dump(model, 'models/collaborative_filtering.pkl')
    
    return model, W, H

def predict_rating(user_id, food_id, model, W, H):
    """Predict user rating for a food item"""
    user_vector = W[user_id]
    item_vector = H[:, food_id]
    predicted_rating = np.dot(user_vector, item_vector)
    return predicted_rating
```

#### 2.2: Content-Based Filtering Model

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

def train_content_based(foods):
    """
    Train content-based filtering model
    """
    # Extract features
    food_features = []
    food_descriptions = []
    
    for food in foods:
        # Numerical features
        features = [
            food.calories or 0,
            food.protein or 0,
            food.carbohydrates or 0,
            food.fiber or 0,
            food.glycemic_index or 50,
            food.current_price or 0
        ]
        food_features.append(features)
        
        # Text description
        desc = f"{food.name} {food.local_name or ''} {food.description or ''}"
        food_descriptions.append(desc)
    
    # Scale numerical features
    scaler = StandardScaler()
    food_features_scaled = scaler.fit_transform(food_features)
    
    # Vectorize descriptions
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    desc_vectors = vectorizer.fit_transform(food_descriptions)
    
    # Combine features
    from scipy.sparse import hstack
    combined_features = hstack([food_features_scaled, desc_vectors])
    
    # Save models
    import joblib
    joblib.dump(scaler, 'models/food_scaler.pkl')
    joblib.dump(vectorizer, 'models/food_vectorizer.pkl')
    
    return combined_features, scaler, vectorizer

def find_similar_foods(food_id, combined_features, top_n=10):
    """Find similar foods using cosine similarity"""
    from sklearn.metrics.pairwise import cosine_similarity
    
    food_vector = combined_features[food_id:food_id+1]
    similarities = cosine_similarity(food_vector, combined_features)[0]
    
    # Get top N similar foods
    similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
    return similar_indices, similarities[similar_indices]
```

#### 2.3: Hybrid Recommendation Model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_hybrid_model(user_features, food_features, interactions):
    """
    Train hybrid model combining collaborative and content-based
    """
    # Prepare training data
    X = []
    y = []
    
    for interaction in interactions:
        user_id = interaction['user_id']
        food_id = interaction['food_id']
        accepted = interaction['accepted']
        
        # Combine user and food features
        combined = np.concatenate([
            user_features[user_id],
            food_features[food_id]
        ])
        X.append(combined)
        y.append(1 if accepted else 0)
    
    X = np.array(X)
    y = np.array(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training accuracy: {train_score:.2f}")
    print(f"Test accuracy: {test_score:.2f}")
    
    # Save model
    import joblib
    joblib.dump(model, 'models/hybrid_recommendation.pkl')
    
    return model
```

### Step 3: Integrate Models into Recommendation Engine

Update `app/services/recommendation_engine.py`:

```python
class RecommendationEngine:
    def __init__(self):
        self.model_dir = 'models'
        os.makedirs(self.model_dir, exist_ok=True)
        self._load_models()
    
    def _load_models(self):
        """Load trained ML models"""
        try:
            # Load collaborative filtering model
            cf_model_path = os.path.join(self.model_dir, 'collaborative_filtering.pkl')
            if os.path.exists(cf_model_path):
                self.cf_model = joblib.load(cf_model_path)
            else:
                self.cf_model = None
            
            # Load content-based model
            self.food_scaler = joblib.load(os.path.join(self.model_dir, 'food_scaler.pkl'))
            self.food_vectorizer = joblib.load(os.path.join(self.model_dir, 'food_vectorizer.pkl'))
            
            # Load hybrid model
            hybrid_model_path = os.path.join(self.model_dir, 'hybrid_recommendation.pkl')
            if os.path.exists(hybrid_model_path):
                self.hybrid_model = joblib.load(hybrid_model_path)
            else:
                self.hybrid_model = None
        except Exception as e:
            print(f"Warning: Could not load ML models: {e}")
            self.cf_model = None
            self.hybrid_model = None
    
    def _calculate_ml_score(self, user, food):
        """Calculate ML-based recommendation score"""
        if not self.hybrid_model:
            return 0, "ML model not available"
        
        # Extract features
        user_features = self._extract_user_features(user)
        food_features = self._extract_food_features(food)
        
        # Combine features
        combined = np.concatenate([user_features, food_features]).reshape(1, -1)
        
        # Predict
        probability = self.hybrid_model.predict_proba(combined)[0][1]
        score = probability * 100
        
        # Get feature importance for explainability
        feature_importance = self.hybrid_model.feature_importances_
        
        return score, f"ML prediction: {probability:.2%} confidence"
    
    def _calculate_food_score(self, user, food, meal_type):
        """Hybrid scoring: Rule-based + ML"""
        # Rule-based score
        rule_score, rule_reasoning = self._rule_based_score(user, food, meal_type)
        
        # ML-based score
        ml_score, ml_reasoning = self._calculate_ml_score(user, food)
        
        # Combine scores (weighted average)
        final_score = (rule_score * 0.6) + (ml_score * 0.4)
        
        # Combine reasoning
        reasoning = f"{rule_reasoning}. {ml_reasoning}"
        
        return final_score, reasoning
```

### Step 4: Model Training Script

Create `train_models.py`:

```python
"""
Script to train ML models for recommendations
"""
from app import create_app, db
from app.models import User, FoodItem, Recommendation
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def prepare_training_data():
    """Prepare training data from user interactions"""
    app = create_app()
    
    with app.app_context():
        # Get all users and foods
        users = User.query.all()
        foods = FoodItem.query.all()
        
        # Get user interactions (accepted/rejected recommendations)
        recommendations = Recommendation.query.filter(
            Recommendation.is_accepted.isnot(None)
        ).all()
        
        # Prepare features
        user_features = []
        food_features = []
        labels = []
        
        for rec in recommendations:
            user = next((u for u in users if u.id == rec.user_id), None)
            food = next((f for f in foods if f.id == rec.food_item_id), None)
            
            if not user or not food:
                continue
            
            # Extract user features
            uf = [
                user.age or 30,
                1 if user.gender == 'male' else 0,
                user.calculate_bmi() or 22,
                1 if user.has_diabetes else 0,
                user.monthly_budget or 0
            ]
            
            # Extract food features
            ff = [
                food.calories or 0,
                food.protein or 0,
                food.carbohydrates or 0,
                food.fiber or 0,
                food.glycemic_index or 50,
                food.current_price or 0
            ]
            
            user_features.append(uf)
            food_features.append(ff)
            labels.append(1 if rec.is_accepted else 0)
        
        return np.array(user_features), np.array(food_features), np.array(labels)

def train_model():
    """Train the hybrid recommendation model"""
    print("Preparing training data...")
    user_features, food_features, labels = prepare_training_data()
    
    if len(user_features) < 10:
        print("Not enough training data. Need at least 10 interactions.")
        return
    
    # Combine features
    X = np.hstack([user_features, food_features])
    y = labels
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    print("Training model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training accuracy: {train_score:.2%}")
    print(f"Test accuracy: {test_score:.2%}")
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model_path = os.path.join('models', 'hybrid_recommendation.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    return model

if __name__ == '__main__':
    train_model()
```

### Step 5: Model Retraining Schedule

Create `retrain_models.py` for periodic retraining:

```python
"""
Schedule periodic model retraining
"""
import schedule
import time
from train_models import train_model

def retrain_job():
    """Job to retrain models"""
    print("Starting model retraining...")
    try:
        train_model()
        print("Model retraining completed successfully")
    except Exception as e:
        print(f"Error during retraining: {e}")

# Schedule daily retraining at 2 AM
schedule.every().day.at("02:00").do(retrain_job)

if __name__ == '__main__':
    print("Model retraining scheduler started")
    while True:
        schedule.run_pending()
        time.sleep(3600)  # Check every hour
```

---

## Testing and Verification

### Step 1: Unit Tests

Create `tests/` directory and test files:

```python
# tests/test_models.py
import unittest
from app import create_app, db
from app.models import User, FoodItem

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_creation(self):
        user = User(username='test', email='test@test.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('password'))
```

### Step 2: Integration Tests

Test routes and services:

```python
# tests/test_routes.py
import unittest
from app import create_app
from flask.testing import FlaskClient

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_register_page(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
```

### Step 3: Run Tests

```bash
python -m pytest tests/
```

---

## Deployment

### Step 1: Production Configuration

Create `.env.production`:

```env
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@localhost/zoenutritech
FLASK_ENV=production
```

### Step 2: Production Server

Use `run_production.py` with Waitress:

```bash
python run_production.py
```

### Step 3: Database Migration

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## Development Workflow

### Daily Development Process

1. **Start Development Server**
   ```bash
   python start_final.py
   ```

2. **Make Changes**
   - Edit code in VS Code
   - Save files
   - Server auto-reloads (if enabled)

3. **Test Changes**
   - Open browser: http://127.0.0.1:5000
   - Test functionality
   - Check for errors in terminal

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

### Adding New Features

1. **Create Route**
   - Add route in `app/routes/`
   - Create template in `templates/`
   - Update navigation if needed

2. **Add Service Logic**
   - Create service in `app/services/`
   - Implement business logic
   - Add tests

3. **Update Models**
   - Modify `app/models.py`
   - Create migration: `flask db migrate`
   - Apply migration: `flask db upgrade`

---

## Troubleshooting

### Common Issues

1. **Template Not Found**
   - Check `app/__init__.py` template_folder path
   - Verify templates exist in correct location

2. **Database Errors**
   - Run: `flask db upgrade`
   - Check database file permissions

3. **Import Errors**
   - Verify virtual environment is activated
   - Run: `pip install -r requirements.txt`

4. **ML Model Errors**
   - Check if models exist in `models/` directory
   - Run: `python train_models.py` to create models

---

## Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Documentation: https://www.sqlalchemy.org/
- scikit-learn Documentation: https://scikit-learn.org/
- Bootstrap 5 Documentation: https://getbootstrap.com/

---

## Conclusion

This guide provides a complete roadmap for developing the ZOE NutriTech system. Follow each phase systematically, test thoroughly, and integrate ML models as your user base grows and provides more interaction data.

For questions or issues, refer to the main `README.md` and documentation in the `docs/` folder.

