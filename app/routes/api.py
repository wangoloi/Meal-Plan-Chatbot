"""
API Routes
RESTful API endpoints for external integrations
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, FoodItem, Recommendation, FoodLog
from app.services.price_api import PriceAPIService
from app.services.offline_manager import OfflineManager
from functools import wraps

api_bp = Blueprint('api', __name__)
price_service = PriceAPIService()
offline_manager = OfflineManager()

def api_key_required(f):
    """Decorator for API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        # In production, validate against database
        if not api_key:
            return jsonify({'success': False, 'error': 'API key required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/foods', methods=['GET'])
@login_required
def get_foods():
    """Get list of food items"""
    category = request.args.get('category')
    limit = request.args.get('limit', 50, type=int)
    
    query = FoodItem.query.filter_by(is_affordable=True)
    if category:
        query = query.filter_by(category=category)
    
    foods = query.limit(limit).all()
    
    return jsonify({
        'success': True,
        'foods': [food.to_dict() for food in foods]
    })

@api_bp.route('/foods/<int:food_id>', methods=['GET'])
@login_required
def get_food(food_id):
    """Get specific food item"""
    food = FoodItem.query.get_or_404(food_id)
    return jsonify({'success': True, 'food': food.to_dict()})

@api_bp.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """Get user recommendations"""
    meal_type = request.args.get('meal_type', 'all')
    limit = request.args.get('limit', 10, type=int)
    
    from app.services.recommendation_engine import RecommendationEngine
    engine = RecommendationEngine()
    recommendations = engine.generate_recommendations(
        user=current_user,
        meal_type=meal_type,
        limit=limit
    )
    
    return jsonify({
        'success': True,
        'recommendations': [rec.to_dict() for rec in recommendations]
    })

@api_bp.route('/prices/update', methods=['POST'])
@api_key_required
def update_prices():
    """Update food prices from external API"""
    force = request.json.get('force', False) if request.is_json else False
    updated_count = price_service.update_food_prices(force=force)
    
    return jsonify({
        'success': True,
        'updated_count': updated_count,
        'message': f'Updated {updated_count} food prices'
    })

@api_bp.route('/prices/<int:food_id>/trend', methods=['GET'])
@login_required
def get_price_trend(food_id):
    """Get price trend for a food item"""
    days = request.args.get('days', 30, type=int)
    trend = price_service.get_price_trend(food_id, days=days)
    
    return jsonify({
        'success': True,
        'trend': trend
    })

@api_bp.route('/offline/enable', methods=['POST'])
@login_required
def enable_offline():
    """Enable offline mode"""
    success = offline_manager.enable_offline_mode(current_user)
    
    return jsonify({
        'success': success,
        'offline_mode': current_user.offline_mode_enabled,
        'features': offline_manager.get_offline_features()
    })

@api_bp.route('/offline/disable', methods=['POST'])
@login_required
def disable_offline():
    """Disable offline mode and sync"""
    success = offline_manager.disable_offline_mode(current_user)
    
    return jsonify({
        'success': success,
        'offline_mode': current_user.offline_mode_enabled
    })

@api_bp.route('/offline/data', methods=['GET'])
@login_required
def get_offline_data():
    """Get cached offline data"""
    data = offline_manager.load_cached_data(current_user.id)
    
    if data:
        return jsonify({'success': True, 'data': data})
    else:
        return jsonify({'success': False, 'error': 'No cached data found'}), 404

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'online': offline_manager.is_online()
    })

