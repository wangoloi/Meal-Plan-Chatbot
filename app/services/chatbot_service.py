"""
NLP Conversational Interface Service
Uses LLM for dietary conversations and nutrition advice
"""
import json
import re
from datetime import datetime
from app import db
from app.models import ChatHistory, User, FoodItem, Recommendation
from app.services.recommendation_engine import RecommendationEngine

class ChatbotService:
    """NLP-powered chatbot for dietary conversations"""
    
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'greetings'],
            'food_recommendation': ['recommend', 'suggest', 'what should i eat', 'food', 'meal'],
            'nutrition_info': ['nutrition', 'calories', 'protein', 'carbs', 'vitamin', 'nutrient'],
            'diabetes_advice': ['diabetes', 'blood sugar', 'glucose', 'insulin', 'glycemic'],
            'weight_management': ['weight', 'lose weight', 'gain weight', 'diet', 'calories'],
            'budget': ['budget', 'affordable', 'cheap', 'price', 'cost'],
            'recipe': ['recipe', 'how to cook', 'prepare', 'make'],
            'goodbye': ['bye', 'goodbye', 'see you', 'thanks', 'thank you']
        }
    
    def process_message(self, user, message):
        """
        Process user message and generate response
        
        Args:
            user: User model instance
            message: User's message string
        
        Returns:
            Dict with response, intent, and entities
        """
        message_lower = message.lower().strip()
        
        # Detect intent
        intent = self._detect_intent(message_lower)
        
        # Extract entities
        entities = self._extract_entities(message_lower, user)
        
        # Generate response based on intent
        response = self._generate_response(user, message, intent, entities)
        
        # Save to history
        chat_history = ChatHistory(
            user_id=user.id,
            message=message,
            response=response,
            intent=intent,
            entities=json.dumps(entities)
        )
        db.session.add(chat_history)
        db.session.commit()
        
        return {
            'response': response,
            'intent': intent,
            'entities': entities
        }
    
    def _detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()
        
        # Score each intent
        intent_scores = {}
        for intent, keywords in self.intents.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        
        return 'general'
    
    def _extract_entities(self, message, user):
        """Extract entities from message"""
        entities = {}
        message_lower = message.lower()
        
        # Extract food names
        food_items = FoodItem.query.all()
        for food in food_items:
            if food.name.lower() in message_lower or (food.local_name and food.local_name.lower() in message_lower):
                entities['food'] = food.name
                break
        
        # Extract numbers (could be calories, weight, etc.)
        numbers = re.findall(r'\d+\.?\d*', message)
        if numbers:
            entities['numbers'] = [float(n) for n in numbers]
        
        # Extract meal types
        meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        for meal in meal_types:
            if meal in message_lower:
                entities['meal_type'] = meal
                break
        
        return entities
    
    def _generate_response(self, user, message, intent, entities):
        """Generate response based on intent and context"""
        
        if intent == 'greeting':
            return f"Hello {user.first_name or 'there'}! I'm ZOE, your nutrition assistant. How can I help you today? I can help with food recommendations, nutrition advice, diabetes management, and more!"
        
        elif intent == 'food_recommendation':
            meal_type = entities.get('meal_type', 'all')
            recommendations = self.recommendation_engine.generate_recommendations(
                user=user,
                meal_type=meal_type,
                limit=3
            )
            
            if recommendations:
                food_names = [rec.food_item.name for rec in recommendations]
                response = f"Based on your profile, I recommend: {', '.join(food_names)}. "
                if recommendations[0].reasoning:
                    response += f"Reason: {recommendations[0].reasoning}"
                return response
            else:
                return "I'm having trouble finding recommendations right now. Please check your profile settings."
        
        elif intent == 'nutrition_info':
            food_name = entities.get('food')
            if food_name:
                food = FoodItem.query.filter_by(name=food_name).first()
                if food:
                    return self._format_nutrition_info(food)
                else:
                    return f"I don't have information about {food_name} in my database. Could you try a different food?"
            else:
                return "Which food would you like to know about? I can provide detailed nutritional information."
        
        elif intent == 'diabetes_advice':
            if not user.has_diabetes:
                return "I notice you don't have diabetes in your profile. Would you like to update your health information?"
            
            response = "For diabetes management, I recommend:\n"
            response += "1. Choose foods with low glycemic index (GI < 55)\n"
            response += "2. Monitor your blood sugar regularly\n"
            response += "3. Eat balanced meals with protein, fiber, and healthy carbs\n"
            response += "4. Avoid high-sugar foods and refined carbohydrates\n\n"
            
            if user.diabetes_type == 'type1':
                response += "For Type 1 diabetes, make sure to coordinate with your medical provider for insulin dosing."
            elif user.diabetes_type == 'type2':
                response += "For Type 2 diabetes, focus on lifestyle changes and medication adherence."
            
            return response
        
        elif intent == 'weight_management':
            if user.primary_goal == 'lose_weight':
                return "For weight loss, I recommend:\n- Low-calorie, high-fiber foods\n- Lean proteins\n- Plenty of vegetables\n- Portion control\n- Regular physical activity"
            elif user.primary_goal == 'gain_weight':
                return "For healthy weight gain, I recommend:\n- Calorie-dense foods\n- High-protein options\n- Healthy fats\n- Regular meals and snacks"
            else:
                return "I can help you with weight management. Would you like to set a weight goal in your profile?"
        
        elif intent == 'budget':
            if user.monthly_budget:
                daily_budget = user.monthly_budget / 30
                affordable_foods = FoodItem.query.filter(
                    FoodItem.current_price <= daily_budget * 0.15
                ).limit(5).all()
                
                if affordable_foods:
                    food_names = [f.name for f in affordable_foods]
                    return f"Based on your budget of {user.monthly_budget:,.0f} UGX/month, here are affordable options: {', '.join(food_names)}"
            
            return "I can help you find affordable foods. Please set your monthly budget in your profile settings."
        
        elif intent == 'recipe':
            food_name = entities.get('food')
            if food_name:
                return f"I can help you with recipes for {food_name}. Here's a simple preparation tip: focus on steaming, boiling, or grilling to preserve nutrients. Would you like more specific cooking instructions?"
            else:
                return "Which food would you like a recipe for? I can provide cooking tips and preparation methods."
        
        elif intent == 'goodbye':
            return "You're welcome! Feel free to ask me anything about nutrition anytime. Stay healthy!"
        
        else:
            # General fallback
            return "I'm here to help with nutrition and dietary advice. You can ask me about:\n- Food recommendations\n- Nutritional information\n- Diabetes management\n- Weight management\n- Budget-friendly options\nWhat would you like to know?"
    
    def _format_nutrition_info(self, food):
        """Format nutritional information for a food item"""
        info = f"Nutritional information for {food.name} (per 100g):\n\n"
        
        if food.calories:
            info += f"Calories: {food.calories} kcal\n"
        if food.protein:
            info += f"Protein: {food.protein}g\n"
        if food.carbohydrates:
            info += f"Carbohydrates: {food.carbohydrates}g\n"
        if food.fiber:
            info += f"Fiber: {food.fiber}g\n"
        if food.fat:
            info += f"Fat: {food.fat}g\n"
        if food.glycemic_index:
            info += f"Glycemic Index: {food.glycemic_index}\n"
        if food.vitamin_c:
            info += f"Vitamin C: {food.vitamin_c}mg\n"
        if food.iron:
            info += f"Iron: {food.iron}mg\n"
        
        if food.current_price:
            info += f"\nCurrent price: {food.current_price:,.0f} UGX per {food.price_unit}"
        
        return info
    
    def get_conversation_history(self, user, limit=10):
        """Get recent conversation history"""
        return ChatHistory.query.filter_by(
            user_id=user.id
        ).order_by(ChatHistory.created_at.desc()).limit(limit).all()

