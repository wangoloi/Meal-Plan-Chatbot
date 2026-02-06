# NLP Conversational Interface Documentation

## Overview

The ZOE NutriTech chatbot uses Natural Language Processing (NLP) to provide conversational dietary advice and nutrition support. The system uses intent detection, entity extraction, and context-aware response generation.

## Architecture

### Components

1. **Chatbot Service** (`app/services/chatbot_service.py`)
   - Message processing
   - Intent detection
   - Entity extraction
   - Response generation

2. **Intent Classification**
   - Rule-based intent detection
   - Keyword matching
   - Pattern recognition

3. **Entity Extraction**
   - Food names
   - Numbers (calories, weight, etc.)
   - Meal types
   - Health conditions

4. **Response Generation**
   - Template-based responses
   - Context-aware replies
   - Integration with recommendation engine

## How It Works

### 1. Message Processing Pipeline

```
User Message
    ↓
Intent Detection
    ↓
Entity Extraction
    ↓
Context Retrieval (User Profile, History)
    ↓
Response Generation
    ↓
Response + Metadata
```

### 2. Intent Detection

The system recognizes the following intents:

#### Greeting
- Keywords: "hello", "hi", "hey", "greetings"
- Response: Personalized greeting with user's name

#### Food Recommendation
- Keywords: "recommend", "suggest", "what should i eat", "food", "meal"
- Action: Calls recommendation engine
- Response: Lists recommended foods with explanations

#### Nutrition Information
- Keywords: "nutrition", "calories", "protein", "carbs", "vitamin", "nutrient"
- Action: Retrieves nutritional data
- Response: Detailed nutritional information

#### Diabetes Advice
- Keywords: "diabetes", "blood sugar", "glucose", "insulin", "glycemic"
- Action: Provides diabetes-specific guidance
- Response: Educational content + recommendations

#### Weight Management
- Keywords: "weight", "lose weight", "gain weight", "diet", "calories"
- Action: Provides weight management advice
- Response: Goal-specific recommendations

#### Budget
- Keywords: "budget", "affordable", "cheap", "price", "cost"
- Action: Filters foods by budget
- Response: Budget-friendly food suggestions

#### Recipe
- Keywords: "recipe", "how to cook", "prepare", "make"
- Action: Provides cooking tips
- Response: Preparation methods

#### Goodbye
- Keywords: "bye", "goodbye", "see you", "thanks", "thank you"
- Response: Friendly farewell

### 3. Entity Extraction

The system extracts:

**Food Names**:
- Matches against food database
- Handles local names (e.g., "matooke", "binyebwa")
- Case-insensitive matching

**Numbers**:
- Extracts numeric values
- Context determines meaning (calories, weight, etc.)

**Meal Types**:
- "breakfast", "lunch", "dinner", "snack"
- Used for meal-specific recommendations

**Health Conditions**:
- Diabetes-related terms
- Symptoms
- Medications

### 4. Response Generation

#### Template-Based Responses

For structured information:
```python
response = f"Nutritional information for {food.name} (per 100g):\n\n"
response += f"Calories: {food.calories} kcal\n"
response += f"Protein: {food.protein}g\n"
# ... more details
```

#### Context-Aware Responses

Uses user profile:
- Diabetes status → diabetes-specific advice
- Goals → goal-oriented recommendations
- Budget → budget-aware suggestions

#### Dynamic Responses

Integrates with other services:
- Recommendation engine for food suggestions
- Search engine for food lookup
- Price API for cost information

## Example Conversations

### Example 1: Food Recommendation

**User**: "What should I eat for breakfast?"

**System**:
1. Intent: `food_recommendation`
2. Entity: `meal_type: breakfast`
3. Action: Generate breakfast recommendations
4. Response: "Based on your profile, I recommend: Matooke, Beans, Eggs. Reason: Diabetes-friendly food with low glycemic index. High protein (21.6g) for muscle health."

### Example 2: Nutrition Information

**User**: "Tell me about matooke"

**System**:
1. Intent: `nutrition_info`
2. Entity: `food: matooke`
3. Action: Retrieve nutritional data
4. Response: "Nutritional information for Matooke (per 100g):
   - Calories: 122 kcal
   - Protein: 1.3g
   - Carbohydrates: 31.9g
   - Fiber: 2.3g
   - Glycemic Index: 45
   - Current price: 3,000 UGX per kg"

### Example 3: Diabetes Advice

**User**: "I have high blood sugar, what should I do?"

**System**:
1. Intent: `diabetes_advice`
2. Action: Provide diabetes management guidance
3. Response: "For diabetes management, I recommend:
   1. Choose foods with low glycemic index (GI < 55)
   2. Monitor your blood sugar regularly
   3. Eat balanced meals with protein, fiber, and healthy carbs
   4. Avoid high-sugar foods and refined carbohydrates
   
   For Type 2 diabetes, focus on lifestyle changes and medication adherence."

## Conversation History

The system maintains conversation history:
- Stores user messages and responses
- Tracks intent and entities
- Enables context continuity
- Supports follow-up questions

## Integration with LLM (Future Enhancement)

### Current Implementation
- Rule-based intent detection
- Template-based responses
- Keyword matching

### Future: LLM Integration

**Option 1: OpenAI GPT**
```python
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are ZOE, a nutrition assistant..."},
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": context}
    ]
)
```

**Option 2: Local LLM**
- Use Hugging Face transformers
- Fine-tune on nutrition data
- Deploy locally for privacy

**Option 3: Hybrid Approach**
- LLM for complex queries
- Rule-based for structured information
- Best of both worlds

## Context Management

### User Context
- Profile information
- Health conditions
- Goals
- Budget
- Preferences

### Conversation Context
- Previous messages
- Extracted entities
- Detected intents
- Conversation flow

### External Context
- Food database
- Nutritional data
- Market prices
- Recommendations

## Error Handling

### Unknown Intent
- Fallback to general response
- Ask for clarification
- Suggest available features

### Missing Entities
- Prompt for required information
- Provide examples
- Guide user input

### No Results
- Apologize gracefully
- Suggest alternatives
- Offer to refine query

## Performance Optimization

1. **Caching**: Cache common responses
2. **Preprocessing**: Normalize user input
3. **Indexing**: Fast food name lookup
4. **Async Processing**: Non-blocking responses

## Limitations

1. **Language**: Currently English only
2. **Complexity**: Limited to structured queries
3. **Medical Advice**: Educational only, not medical
4. **Context Window**: Limited conversation history

## Future Enhancements

1. **Multi-language Support**: Luganda, Swahili
2. **Voice Interface**: Speech-to-text integration
3. **Sentiment Analysis**: Emotional understanding
4. **Proactive Suggestions**: Anticipate user needs
5. **Learning**: Improve from user feedback

## Usage Examples

### Python API
```python
from app.services.chatbot_service import ChatbotService

chatbot = ChatbotService()
response = chatbot.process_message(user, "What should I eat?")
print(response['response'])
```

### REST API
```bash
curl -X POST http://localhost:5000/chatbot/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Recommend foods for diabetes"}'
```

## Best Practices

1. **Clear Prompts**: Guide users on what to ask
2. **Error Messages**: Friendly and helpful
3. **Confirmation**: Confirm important actions
4. **Privacy**: Don't store sensitive medical data
5. **Transparency**: Explain limitations

