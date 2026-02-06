"""
Food Price API Integration Service
Fetches and updates real-time food prices from market APIs
"""
import requests
from datetime import datetime, timedelta
from app import db
from app.models import FoodItem, FoodPrice
import os

class PriceAPIService:
    """Service for fetching and managing food prices"""
    
    def __init__(self):
        # In production, this would be a real API endpoint
        # For now, we'll simulate with market data
        self.api_url = os.getenv('FOOD_PRICE_API_URL', 'https://api.example.com/prices')
        self.api_key = os.getenv('FOOD_PRICE_API_KEY', '')
        self.update_interval_hours = 24
    
    def update_food_prices(self, force=False):
        """
        Update food prices from API
        
        Args:
            force: Force update even if recently updated
        
        Returns:
            Number of prices updated
        """
        updated_count = 0
        
        # Get all food items
        foods = FoodItem.query.all()
        
        for food in foods:
            # Check if update is needed
            if not force and food.price_last_updated:
                time_since_update = datetime.utcnow() - food.price_last_updated
                if time_since_update < timedelta(hours=self.update_interval_hours):
                    continue
            
            # Fetch price from API (or use simulated data)
            price_data = self._fetch_price(food)
            
            if price_data:
                # Update food item price
                old_price = food.current_price
                food.current_price = price_data['price']
                food.price_last_updated = datetime.utcnow()
                
                # Record price history
                price_record = FoodPrice(
                    food_item_id=food.id,
                    price=price_data['price'],
                    location=price_data.get('location', 'Kampala'),
                    source=price_data.get('source', 'api')
                )
                db.session.add(price_record)
                updated_count += 1
        
        db.session.commit()
        return updated_count
    
    def _fetch_price(self, food_item):
        """
        Fetch price from external API
        In production, this would make actual API calls
        """
        try:
            # Simulate API call - in production, use actual API
            # For now, add some variation to simulate market prices
            import random
            
            base_price = food_item.current_price or 1000
            # Simulate price variation (±20%)
            variation = random.uniform(0.8, 1.2)
            new_price = base_price * variation
            
            return {
                'price': round(new_price, 2),
                'location': 'Kampala',
                'source': 'api',
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Error fetching price for {food_item.name}: {str(e)}")
            return None
    
    def get_price_trend(self, food_item_id, days=30):
        """Get price trend for a food item"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        prices = FoodPrice.query.filter(
            FoodPrice.food_item_id == food_item_id,
            FoodPrice.recorded_at >= cutoff_date
        ).order_by(FoodPrice.recorded_at.asc()).all()
        
        return [{
            'date': price.recorded_at.isoformat(),
            'price': price.price,
            'location': price.location
        } for price in prices]
    
    def get_affordable_foods(self, max_price, limit=20):
        """Get foods within a price range"""
        foods = FoodItem.query.filter(
            FoodItem.current_price <= max_price,
            FoodItem.is_affordable == True
        ).order_by(FoodItem.current_price.asc()).limit(limit).all()
        
        return foods
    
    def estimate_meal_cost(self, food_items_with_quantities):
        """
        Estimate total cost for a meal
        
        Args:
            food_items_with_quantities: List of tuples (food_item_id, quantity_in_grams)
        
        Returns:
            Total estimated cost in UGX
        """
        total_cost = 0
        
        for food_id, quantity in food_items_with_quantities:
            food = FoodItem.query.get(food_id)
            if food and food.current_price:
                if food.price_unit == 'kg':
                    cost_per_gram = food.current_price / 1000
                    total_cost += cost_per_gram * quantity
                elif food.price_unit == 'piece':
                    total_cost += food.current_price
                else:
                    # Assume per 100g
                    cost_per_gram = food.current_price / 100
                    total_cost += cost_per_gram * quantity
        
        return round(total_cost, 2)

