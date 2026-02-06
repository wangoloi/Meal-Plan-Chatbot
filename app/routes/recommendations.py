from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Recommendation, FoodItem
from app.services.recommendation_engine import RecommendationEngine

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/')
@login_required
def get_recommendations():
    """Get personalized food recommendations"""
    meal_type = request.args.get('meal_type', 'all')
    
    engine = RecommendationEngine()
    recommendations = engine.generate_recommendations(
        user=current_user,
        meal_type=meal_type,
        limit=10
    )
    
    return render_template('recommendations/list.html', 
                         recommendations=recommendations,
                         meal_type=meal_type)

@recommendations_bp.route('/api/generate', methods=['POST'])
@login_required
def generate_recommendations_api():
    """API endpoint for generating recommendations"""
    data = request.get_json()
    meal_type = data.get('meal_type', 'all')
    limit = data.get('limit', 10)
    
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

@recommendations_bp.route('/<int:recommendation_id>/accept', methods=['POST'])
@login_required
def accept_recommendation(recommendation_id):
    """Accept a recommendation"""
    recommendation = Recommendation.query.get_or_404(recommendation_id)
    
    if recommendation.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    recommendation.is_accepted = True
    db.session.commit()
    
    return jsonify({'success': True})

@recommendations_bp.route('/<int:recommendation_id>/reject', methods=['POST'])
@login_required
def reject_recommendation(recommendation_id):
    """Reject a recommendation"""
    recommendation = Recommendation.query.get_or_404(recommendation_id)
    
    if recommendation.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    recommendation.is_accepted = False
    db.session.commit()
    
    return jsonify({'success': True})

