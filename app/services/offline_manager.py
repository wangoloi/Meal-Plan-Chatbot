"""
Offline Mode Manager
Handles offline functionality and data synchronization
"""
import json
import os
from datetime import datetime
from app import db
from app.models import User, FoodItem, Recommendation, FoodLog, Goal

class OfflineManager:
    """Manages offline mode and data synchronization"""
    
    def __init__(self):
        self.cache_dir = 'offline_cache'
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def enable_offline_mode(self, user):
        """Enable offline mode for user and cache essential data"""
        user.offline_mode_enabled = True
        user.last_sync = datetime.utcnow()
        db.session.commit()
        
        # Cache essential data
        self._cache_user_data(user)
        return True
    
    def disable_offline_mode(self, user):
        """Disable offline mode and sync data"""
        user.offline_mode_enabled = False
        
        # Sync any pending changes
        self.sync_offline_data(user)
        
        db.session.commit()
        return True
    
    def _cache_user_data(self, user):
        """Cache user's essential data for offline access"""
        cache_data = {
            'user': user.to_dict(),
            'food_items': [],
            'recommendations': [],
            'goals': [],
            'cached_at': datetime.utcnow().isoformat()
        }
        
        # Cache all food items (essential for recommendations)
        foods = FoodItem.query.filter_by(is_affordable=True).all()
        cache_data['food_items'] = [food.to_dict() for food in foods]
        
        # Cache user's recent recommendations
        recommendations = Recommendation.query.filter_by(
            user_id=user.id
        ).order_by(Recommendation.created_at.desc()).limit(50).all()
        cache_data['recommendations'] = [rec.to_dict() for rec in recommendations]
        
        # Cache user's goals
        goals = Goal.query.filter_by(user_id=user.id, status='active').all()
        cache_data['goals'] = [goal.to_dict() for goal in goals]
        
        # Save to file
        cache_file = os.path.join(self.cache_dir, f'user_{user.id}.json')
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
    
    def load_cached_data(self, user_id):
        """Load cached data for offline access"""
        cache_file = os.path.join(self.cache_dir, f'user_{user_id}.json')
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def sync_offline_data(self, user):
        """Sync offline changes back to server"""
        # This would sync any changes made while offline
        # For now, we'll just update the sync timestamp
        user.last_sync = datetime.utcnow()
        db.session.commit()
        
        # In a full implementation, this would:
        # 1. Read offline changes from local storage
        # 2. Apply them to the database
        # 3. Handle conflicts
        # 4. Update cache
    
    def is_online(self):
        """Check if system has internet connectivity"""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def get_offline_features(self):
        """Get list of features available offline"""
        return {
            'food_search': True,
            'view_recommendations': True,
            'log_food': True,
            'view_profile': True,
            'chatbot': False,  # Requires LLM API
            'price_updates': False,  # Requires API
            'sync_data': False  # Requires connection
        }

