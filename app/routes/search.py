"""
Search Routes
Food search and discovery
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.search_engine import SearchEngine

search_bp = Blueprint('search', __name__)
search_engine = SearchEngine()

@search_bp.route('/')
@login_required
def search():
    """Food search page"""
    query = request.args.get('q', '')
    filters = {
        'category': request.args.get('category'),
        'max_price': request.args.get('max_price', type=float),
        'diabetes_friendly': request.args.get('diabetes_friendly', type=bool),
        'min_calories': request.args.get('min_calories', type=float),
        'max_calories': request.args.get('max_calories', type=float)
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    results = []
    if query or filters:
        results = search_engine.search(query, filters=filters if filters else None)
    
    return render_template('search/results.html',
                         query=query,
                         results=results,
                         filters=filters)

@search_bp.route('/api/autocomplete')
@login_required
def autocomplete():
    """Autocomplete suggestions"""
    prefix = request.args.get('q', '')
    
    if len(prefix) < 2:
        return jsonify({'success': True, 'suggestions': []})
    
    suggestions = search_engine.autocomplete(prefix)
    
    return jsonify({
        'success': True,
        'suggestions': suggestions
    })

@search_bp.route('/api/search', methods=['POST'])
@login_required
def api_search():
    """API endpoint for search"""
    data = request.get_json()
    query = data.get('query', '')
    filters = data.get('filters', {})
    limit = data.get('limit', 20)
    
    results = search_engine.search(query, filters=filters, limit=limit)
    
    return jsonify({
        'success': True,
        'results': [food.to_dict() for food in results]
    })

@search_bp.route('/nutrition')
@login_required
def search_by_nutrition():
    """Search foods by nutritional criteria"""
    nutrition_filters = {
        'min_protein': request.args.get('min_protein', type=float),
        'max_carbs': request.args.get('max_carbs', type=float),
        'min_fiber': request.args.get('min_fiber', type=float),
        'max_gi': request.args.get('max_gi', type=float),
        'max_calories': request.args.get('max_calories', type=float)
    }
    
    # Remove None values
    nutrition_filters = {k: v for k, v in nutrition_filters.items() if v is not None}
    
    results = []
    if nutrition_filters:
        results = search_engine.search_by_nutrition(nutrition_filters)
    
    return render_template('search/nutrition.html',
                         results=results,
                         filters=nutrition_filters)

