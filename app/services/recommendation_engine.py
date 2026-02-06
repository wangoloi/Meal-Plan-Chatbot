"""
Recommendation Engine Service
Combines ML-based and rule-based logic for personalized food recommendations
"""
import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime
from app import db
from app.models import FoodItem, Recommendation, FoodLog, User

# Optional ML imports - app works without them using rule-based logic only
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    # Define dummy classes for when sklearn is not available
    class TfidfVectorizer:
        def __init__(self, *args, **kwargs):
            pass
    class StandardScaler:
        def __init__(self, *args, **kwargs):
            pass

class RecommendationEngine:
    """Hybrid recommendation system using ML and rule-based logic"""
    
    def __init__(self):
        self.model_dir = 'models'
        os.makedirs(self.model_dir, exist_ok=True)
        if SKLEARN_AVAILABLE:
            self.scaler = StandardScaler()
            self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        else:
            self.scaler = None
            self.vectorizer = None
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = os.path.join(self.model_dir, 'recommendation_model.pkl')
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                return
            except:
                pass
        
        # Train a simple model (in production, use more sophisticated ML)
        self.model = None  # Will use rule-based + similarity for now
    
    def generate_recommendations(self, user, meal_type='all', limit=10):
        """
        Generate personalized food recommendations
        
        Args:
            user: User model instance
            meal_type: 'breakfast', 'lunch', 'dinner', 'snack', or 'all'
            limit: Maximum number of recommendations
        
        Returns:
            List of Recommendation objects
        """
        # Get all food items
        query = FoodItem.query.filter_by(is_affordable=True)
        
        if meal_type != 'all':
            # Filter by typical meal categories
            if meal_type == 'breakfast':
                query = query.filter(FoodItem.category.in_(['grains', 'fruits', 'proteins']))
            elif meal_type == 'lunch' or meal_type == 'dinner':
                query = query.filter(FoodItem.category.in_(['grains', 'vegetables', 'proteins']))
            elif meal_type == 'snack':
                query = query.filter(FoodItem.category.in_(['fruits', 'vegetables']))
        
        all_foods = query.all()
        
        if not all_foods:
            return []
        
        # Score each food item
        scored_foods = []
        for food in all_foods:
            score, reasoning = self._calculate_food_score(user, food, meal_type)
            if score > 0:
                scored_foods.append((food, score, reasoning))
        
        # Sort by score
        scored_foods.sort(key=lambda x: x[1], reverse=True)
        
        # Create recommendations
        recommendations = []
        for food, score, reasoning in scored_foods[:limit]:
            # Check if recommendation already exists
            existing = Recommendation.query.filter_by(
                user_id=user.id,
                food_item_id=food.id,
                meal_suggestion=meal_type if meal_type != 'all' else None
            ).first()
            
            if not existing:
                recommendation = Recommendation(
                    user_id=user.id,
                    food_item_id=food.id,
                    recommendation_type='hybrid',
                    confidence_score=min(1.0, score / 100.0),
                    reasoning=reasoning,
                    meal_suggestion=meal_type if meal_type != 'all' else None,
                    serving_size=self._calculate_serving_size(user, food),
                    estimated_cost=self._estimate_cost(food, user),
                    model_version='v1.0',
                    features_used=str(self._extract_features(user, food))
                )
                db.session.add(recommendation)
                recommendations.append(recommendation)
            else:
                recommendations.append(existing)
        
        db.session.commit()
        return recommendations
    
    def _calculate_food_score(self, user, food, meal_type):
        """
        Calculate recommendation score for a food item
        Uses both rule-based and ML-based scoring
        """
        score = 50.0  # Base score
        reasoning_parts = []
        
        # Rule-based scoring
        # 1. Diabetes considerations
        if user.has_diabetes:
            if food.diabetes_friendly:
                score += 30
                reasoning_parts.append("Diabetes-friendly food with low glycemic index")
            else:
                score -= 40
                reasoning_parts.append("Not recommended for diabetes management")
            
            if food.glycemic_index and food.glycemic_index < 55:
                score += 20
                reasoning_parts.append(f"Low GI ({food.glycemic_index}) helps maintain stable blood sugar")
            elif food.glycemic_index and food.glycemic_index > 70:
                score -= 30
                reasoning_parts.append(f"High GI ({food.glycemic_index}) may cause blood sugar spikes")
        
        # 2. Goal-based scoring
        if user.primary_goal == 'lose_weight':
            if food.weight_loss_friendly:
                score += 25
                reasoning_parts.append("Supports weight loss goals")
            if food.calories and food.calories < 100:
                score += 15
                reasoning_parts.append("Low calorie content")
            if food.fiber and food.fiber > 3:
                score += 10
                reasoning_parts.append("High fiber promotes satiety")
        
        elif user.primary_goal == 'gain_weight':
            if food.weight_gain_friendly:
                score += 25
                reasoning_parts.append("Supports healthy weight gain")
            if food.calories and food.calories > 200:
                score += 15
                reasoning_parts.append("Calorie-dense for weight gain")
            if food.protein and food.protein > 15:
                score += 10
                reasoning_parts.append("High protein for muscle building")
        
        elif user.primary_goal == 'healthy_eating':
            # Balanced nutrition
            if food.protein and food.protein > 10:
                score += 10
            if food.fiber and food.fiber > 2:
                score += 10
            if food.vitamin_c and food.vitamin_c > 10:
                score += 5
            reasoning_parts.append("Nutritious and balanced")
        
        # 3. Budget considerations
        if user.monthly_budget:
            daily_budget = user.monthly_budget / 30
            if food.current_price and food.current_price <= daily_budget * 0.1:
                score += 15
                reasoning_parts.append("Affordable within your budget")
            elif food.current_price and food.current_price > daily_budget * 0.3:
                score -= 20
                reasoning_parts.append("May exceed budget constraints")
        
        # 4. Nutritional completeness
        nutrition_score = 0
        if food.protein and food.protein > 0:
            nutrition_score += 1
        if food.fiber and food.fiber > 0:
            nutrition_score += 1
        if food.vitamin_c and food.vitamin_c > 0:
            nutrition_score += 1
        if food.iron and food.iron > 0:
            nutrition_score += 1
        
        score += nutrition_score * 5
        if nutrition_score >= 3:
            reasoning_parts.append("Rich in essential nutrients")
        
        # 5. User history (collaborative filtering aspect)
        recent_logs = FoodLog.query.filter_by(
            user_id=user.id
        ).order_by(FoodLog.consumed_at.desc()).limit(10).all()
        
        if recent_logs:
            recent_food_ids = [log.food_item_id for log in recent_logs]
            if food.id in recent_food_ids:
                # Slight boost for foods user has eaten before
                score += 5
                reasoning_parts.append("Based on your eating history")
        
        # 6. ML-based similarity (if we have user preferences)
        # This would use collaborative filtering or content-based filtering
        
        reasoning = ". ".join(reasoning_parts) if reasoning_parts else "Recommended based on your profile"
        
        return max(0, score), reasoning
    
    def _calculate_serving_size(self, user, food):
        """Calculate appropriate serving size based on user profile"""
        base_serving = 100  # grams
        
        if user.primary_goal == 'lose_weight':
            return base_serving * 0.8
        elif user.primary_goal == 'gain_weight':
            return base_serving * 1.2
        else:
            return base_serving
    
    def _estimate_cost(self, food, user):
        """Estimate cost for a serving"""
        if not food.current_price:
            return 0
        
        serving_size = self._calculate_serving_size(user, food)
        
        # Convert to cost per serving
        if food.price_unit == 'kg':
            cost_per_gram = food.current_price / 1000
            return cost_per_gram * serving_size
        elif food.price_unit == 'piece':
            return food.current_price
        else:
            return food.current_price * (serving_size / 100)
    
    def _extract_features(self, user, food):
        """Extract features for ML model"""
        return {
            'user_age': user.age or 30,
            'user_bmi': user.calculate_bmi() or 22,
            'has_diabetes': 1 if user.has_diabetes else 0,
            'food_calories': food.calories or 0,
            'food_protein': food.protein or 0,
            'food_carbs': food.carbohydrates or 0,
            'food_fiber': food.fiber or 0,
            'food_gi': food.glycemic_index or 50,
            'food_price': food.current_price or 0
        }
    
    def explain_recommendation(self, recommendation):
        """Generate detailed explanation for a recommendation"""
        food = recommendation.food_item
        user = recommendation.user
        
        explanation = {
            'food_name': food.name,
            'confidence': f"{recommendation.confidence_score * 100:.1f}%",
            'reasoning': recommendation.reasoning,
            'nutritional_benefits': [],
            'suitability': {}
        }
        
        # Nutritional benefits
        if food.protein and food.protein > 10:
            explanation['nutritional_benefits'].append(f"High protein ({food.protein}g) for muscle health")
        if food.fiber and food.fiber > 3:
            explanation['nutritional_benefits'].append(f"Rich in fiber ({food.fiber}g) for digestive health")
        if food.vitamin_c and food.vitamin_c > 20:
            explanation['nutritional_benefits'].append(f"Excellent source of Vitamin C ({food.vitamin_c}mg)")
        if food.iron and food.iron > 2:
            explanation['nutritional_benefits'].append(f"Good iron source ({food.iron}mg) for blood health")
        
        # Suitability
        if user.has_diabetes:
            if food.glycemic_index:
                if food.glycemic_index < 55:
                    explanation['suitability']['diabetes'] = "Excellent - Low GI helps maintain stable blood sugar"
                elif food.glycemic_index < 70:
                    explanation['suitability']['diabetes'] = "Good - Moderate GI, consume in moderation"
                else:
                    explanation['suitability']['diabetes'] = "Caution - High GI, monitor blood sugar"
        
        if user.primary_goal:
            goal_map = {
                'lose_weight': 'weight_loss',
                'gain_weight': 'weight_gain',
                'healthy_eating': 'general_health'
            }
            goal_key = goal_map.get(user.primary_goal, 'general_health')
            explanation['suitability'][goal_key] = "Well-suited for your goals"
        
        return explanation

