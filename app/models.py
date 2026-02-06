from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    activity_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # User preferences and conditions
    has_diabetes = db.Column(db.Boolean, default=False)
    diabetes_type = db.Column(db.String(20))  # 'type1' or 'type2' or None
    primary_goal = db.Column(db.String(50))  # 'healthy_eating', 'lose_weight', 'gain_weight', 'diabetes_management'
    budget_range = db.Column(db.String(50))  # 'low', 'medium', 'high'
    monthly_budget = db.Column(db.Float)  # in UGX
    
    # Medical connections
    medical_provider_id = db.Column(db.String(100))
    diet_therapist_id = db.Column(db.String(100))
    
    # Offline mode
    offline_mode_enabled = db.Column(db.Boolean, default=False)
    last_sync = db.Column(db.DateTime)
    
    # Relationships
    diabetes_records = db.relationship('DiabetesRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    food_logs = db.relationship('FoodLog', backref='user', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 2)
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'bmi': self.calculate_bmi(),
            'has_diabetes': self.has_diabetes,
            'diabetes_type': self.diabetes_type,
            'primary_goal': self.primary_goal,
            'budget_range': self.budget_range,
            'monthly_budget': self.monthly_budget
        }


class FoodItem(db.Model):
    """Ugandan food items database"""
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    local_name = db.Column(db.String(200))  # Local Ugandan name
    category = db.Column(db.String(100))  # 'grains', 'vegetables', 'fruits', 'proteins', etc.
    description = db.Column(db.Text)
    
    # Nutritional information per 100g
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)  # grams
    carbohydrates = db.Column(db.Float)  # grams
    fiber = db.Column(db.Float)  # grams
    fat = db.Column(db.Float)  # grams
    sugar = db.Column(db.Float)  # grams
    glycemic_index = db.Column(db.Float)  # Important for diabetes
    sodium = db.Column(db.Float)  # mg
    
    # Vitamins and minerals
    vitamin_c = db.Column(db.Float)  # mg
    iron = db.Column(db.Float)  # mg
    calcium = db.Column(db.Float)  # mg
    
    # Affordability and availability
    is_affordable = db.Column(db.Boolean, default=True)
    is_seasonal = db.Column(db.Boolean, default=False)
    season_months = db.Column(db.String(50))  # JSON array of months
    
    # Price tracking
    current_price = db.Column(db.Float)  # in UGX per unit
    price_unit = db.Column(db.String(20))  # 'kg', 'piece', 'bunch', etc.
    price_last_updated = db.Column(db.DateTime)
    
    # Recommendation metadata
    diabetes_friendly = db.Column(db.Boolean, default=False)
    weight_loss_friendly = db.Column(db.Boolean, default=False)
    weight_gain_friendly = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    food_logs = db.relationship('FoodLog', backref='food_item', lazy=True)
    recommendations = db.relationship('Recommendation', backref='food_item', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'local_name': self.local_name,
            'category': self.category,
            'description': self.description,
            'calories': self.calories,
            'protein': self.protein,
            'carbohydrates': self.carbohydrates,
            'fiber': self.fiber,
            'fat': self.fat,
            'sugar': self.sugar,
            'glycemic_index': self.glycemic_index,
            'current_price': self.current_price,
            'price_unit': self.price_unit,
            'diabetes_friendly': self.diabetes_friendly
        }


class DiabetesRecord(db.Model):
    """Diabetes tracking records for Type 1 and Type 2"""
    __tablename__ = 'diabetes_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    record_type = db.Column(db.String(50))  # 'blood_glucose', 'insulin', 'hba1c', 'medication'
    
    # Blood glucose
    blood_glucose_level = db.Column(db.Float)  # mg/dL
    measurement_time = db.Column(db.DateTime)
    measurement_type = db.Column(db.String(20))  # 'fasting', 'postprandial', 'random'
    
    # Insulin (Type 1)
    insulin_type = db.Column(db.String(50))  # 'rapid', 'long_acting', etc.
    insulin_units = db.Column(db.Float)
    insulin_time = db.Column(db.DateTime)
    external_system_id = db.Column(db.String(100))  # For foreign system integration
    
    # HbA1c
    hba1c_value = db.Column(db.Float)  # percentage
    hba1c_date = db.Column(db.DateTime)
    
    # Medication (Type 2)
    medication_name = db.Column(db.String(100))
    medication_dose = db.Column(db.String(50))
    
    # Additional notes
    notes = db.Column(db.Text)
    symptoms = db.Column(db.Text)  # JSON array
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'record_type': self.record_type,
            'blood_glucose_level': self.blood_glucose_level,
            'measurement_time': self.measurement_time.isoformat() if self.measurement_time else None,
            'insulin_units': self.insulin_units,
            'hba1c_value': self.hba1c_value,
            'created_at': self.created_at.isoformat()
        }


class Goal(db.Model):
    """User goals for weight management and health"""
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_type = db.Column(db.String(50))  # 'lose_weight', 'gain_weight', 'maintain_weight', 'blood_glucose_control'
    target_value = db.Column(db.Float)
    current_value = db.Column(db.Float)
    unit = db.Column(db.String(20))  # 'kg', 'mg/dL', etc.
    target_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'paused'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Progress tracking
    progress_updates = db.relationship('GoalProgress', backref='goal', lazy=True, cascade='all, delete-orphan')
    
    def calculate_progress(self):
        if self.target_value and self.current_value:
            if self.goal_type == 'lose_weight':
                initial = self.current_value + (self.target_value - self.current_value)
                progress = ((initial - self.current_value) / (initial - self.target_value)) * 100
            elif self.goal_type == 'gain_weight':
                initial = self.current_value - (self.target_value - self.current_value)
                progress = ((self.current_value - initial) / (self.target_value - initial)) * 100
            else:
                progress = (self.current_value / self.target_value) * 100
            return min(100, max(0, progress))
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'goal_type': self.goal_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'status': self.status,
            'progress': self.calculate_progress()
        }


class GoalProgress(db.Model):
    """Progress updates for goals"""
    __tablename__ = 'goal_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)
    value = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FoodLog(db.Model):
    """User food consumption logs"""
    __tablename__ = 'food_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    quantity = db.Column(db.Float)  # in grams or units
    meal_type = db.Column(db.String(20))  # 'breakfast', 'lunch', 'dinner', 'snack'
    consumed_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'food_item': self.food_item.to_dict() if self.food_item else None,
            'quantity': self.quantity,
            'meal_type': self.meal_type,
            'consumed_at': self.consumed_at.isoformat()
        }


class Recommendation(db.Model):
    """Food recommendations for users"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    recommendation_type = db.Column(db.String(50))  # 'ml_based', 'rule_based', 'hybrid'
    confidence_score = db.Column(db.Float)  # 0-1
    reasoning = db.Column(db.Text)  # Explainability
    meal_suggestion = db.Column(db.String(20))  # 'breakfast', 'lunch', 'dinner', 'snack'
    serving_size = db.Column(db.Float)
    estimated_cost = db.Column(db.Float)  # in UGX
    
    # ML model metadata
    model_version = db.Column(db.String(50))
    features_used = db.Column(db.Text)  # JSON
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_viewed = db.Column(db.Boolean, default=False)
    is_accepted = db.Column(db.Boolean)
    
    def to_dict(self):
        return {
            'id': self.id,
            'food_item': self.food_item.to_dict() if self.food_item else None,
            'recommendation_type': self.recommendation_type,
            'confidence_score': self.confidence_score,
            'reasoning': self.reasoning,
            'meal_suggestion': self.meal_suggestion,
            'serving_size': self.serving_size,
            'estimated_cost': self.estimated_cost
        }


class ChatHistory(db.Model):
    """NLP chatbot conversation history"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(100))  # Detected intent
    entities = db.Column(db.Text)  # JSON array of extracted entities
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'response': self.response,
            'intent': self.intent,
            'created_at': self.created_at.isoformat()
        }


class FoodPrice(db.Model):
    """Food price tracking from market API"""
    __tablename__ = 'food_prices'
    
    id = db.Column(db.Integer, primary_key=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)  # in UGX
    location = db.Column(db.String(100))  # Market location
    source = db.Column(db.String(50))  # 'api', 'user_report', 'market_survey'
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'food_item_id': self.food_item_id,
            'price': self.price,
            'location': self.location,
            'source': self.source,
            'recorded_at': self.recorded_at.isoformat()
        }

