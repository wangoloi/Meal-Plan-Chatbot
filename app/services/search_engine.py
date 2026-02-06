"""
Optimized Search Engine for Food Items
Uses full-text search, semantic search, and filtering
"""
from sqlalchemy import or_, and_
from app.models import FoodItem
import re

class SearchEngine:
    """Advanced search engine for food items"""
    
    def __init__(self):
        self.stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    def search(self, query, filters=None, limit=20):
        """
        Search for food items
        
        Args:
            query: Search query string
            filters: Dict with filters (category, max_price, diabetes_friendly, etc.)
            limit: Maximum results
        
        Returns:
            List of FoodItem objects sorted by relevance
        """
        # Start with base query
        base_query = FoodItem.query.filter_by(is_affordable=True)
        
        # Apply filters
        if filters:
            if filters.get('category'):
                base_query = base_query.filter(FoodItem.category == filters['category'])
            
            if filters.get('max_price'):
                base_query = base_query.filter(FoodItem.current_price <= filters['max_price'])
            
            if filters.get('diabetes_friendly') is not None:
                base_query = base_query.filter(FoodItem.diabetes_friendly == filters['diabetes_friendly'])
            
            if filters.get('min_calories'):
                base_query = base_query.filter(FoodItem.calories >= filters['min_calories'])
            
            if filters.get('max_calories'):
                base_query = base_query.filter(FoodItem.calories <= filters['max_calories'])
        
        # Get all matching items
        all_items = base_query.all()
        
        if not query or query.strip() == '':
            return all_items[:limit]
        
        # Score items by relevance
        query_lower = query.lower().strip()
        query_words = self._tokenize(query_lower)
        
        scored_items = []
        for item in all_items:
            score = self._calculate_relevance_score(item, query_lower, query_words)
            if score > 0:
                scored_items.append((item, score))
        
        # Sort by score
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        return [item for item, score in scored_items[:limit]]
    
    def _tokenize(self, text):
        """Tokenize text into words"""
        words = re.findall(r'\b\w+\b', text.lower())
        return [w for w in words if w not in self.stop_words and len(w) > 2]
    
    def _calculate_relevance_score(self, item, query, query_words):
        """Calculate relevance score for an item"""
        score = 0.0
        
        # Exact name match (highest priority)
        if query in item.name.lower():
            score += 100
        elif any(word in item.name.lower() for word in query_words):
            score += 50
        
        # Local name match
        if item.local_name:
            if query in item.local_name.lower():
                score += 80
            elif any(word in item.local_name.lower() for word in query_words):
                score += 40
        
        # Description match
        if item.description:
            desc_lower = item.description.lower()
            if query in desc_lower:
                score += 30
            else:
                for word in query_words:
                    if word in desc_lower:
                        score += 5
        
        # Category match
        if item.category:
            if query in item.category.lower():
                score += 20
        
        # Partial word matches
        for word in query_words:
            if item.name.lower().startswith(word):
                score += 15
            if item.local_name and item.local_name.lower().startswith(word):
                score += 15
        
        return score
    
    def autocomplete(self, prefix, limit=10):
        """Get autocomplete suggestions"""
        if not prefix or len(prefix) < 2:
            return []
        
        prefix_lower = prefix.lower()
        
        # Search in names and local names
        items = FoodItem.query.filter(
            or_(
                FoodItem.name.ilike(f'{prefix}%'),
                FoodItem.local_name.ilike(f'{prefix}%')
            )
        ).limit(limit).all()
        
        suggestions = []
        for item in items:
            suggestions.append({
                'name': item.name,
                'local_name': item.local_name,
                'category': item.category,
                'id': item.id
            })
        
        return suggestions
    
    def search_by_nutrition(self, nutrition_filters, limit=20):
        """
        Search foods by nutritional criteria
        
        Args:
            nutrition_filters: Dict with min/max values for nutrients
            limit: Maximum results
        """
        query = FoodItem.query.filter_by(is_affordable=True)
        
        if nutrition_filters.get('min_protein'):
            query = query.filter(FoodItem.protein >= nutrition_filters['min_protein'])
        
        if nutrition_filters.get('max_carbs'):
            query = query.filter(FoodItem.carbohydrates <= nutrition_filters['max_carbs'])
        
        if nutrition_filters.get('min_fiber'):
            query = query.filter(FoodItem.fiber >= nutrition_filters['min_fiber'])
        
        if nutrition_filters.get('max_gi'):
            query = query.filter(FoodItem.glycemic_index <= nutrition_filters['max_gi'])
        
        if nutrition_filters.get('max_calories'):
            query = query.filter(FoodItem.calories <= nutrition_filters['max_calories'])
        
        return query.limit(limit).all()

