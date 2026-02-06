# Recommendation System Documentation

## Overview

The ZOE NutriTech recommendation system uses a **hybrid approach** combining Machine Learning (ML) and rule-based logic to provide personalized food recommendations. The system is designed to be explainable, transparent, and nutritionally sound.

## Architecture

### Components

1. **Recommendation Engine** (`app/services/recommendation_engine.py`)
   - Main orchestrator for recommendation generation
   - Combines ML and rule-based scoring
   - Handles explainability

2. **Scoring System**
   - Rule-based scoring (nutritional rules, health conditions)
   - ML-based scoring (user preferences, collaborative filtering)
   - Hybrid scoring (weighted combination)

3. **Explainability Module**
   - Generates human-readable explanations
   - Provides nutritional reasoning
   - Shows confidence scores

## How It Works

### 1. User Profile Analysis

The system analyzes:
- **Health Conditions**: Diabetes type, BMI, age, gender
- **Goals**: Weight loss, weight gain, healthy eating, diabetes management
- **Preferences**: Budget, activity level
- **History**: Past food logs, accepted recommendations

### 2. Food Scoring Algorithm

Each food item receives a score based on multiple factors:

#### Rule-Based Scoring

**Diabetes Considerations** (if user has diabetes):
- Low GI foods (< 55): +30 points
- Medium GI (55-70): +10 points
- High GI (> 70): -30 points
- Diabetes-friendly flag: +30 points

**Goal-Based Scoring**:
- Weight Loss:
  - Low calories (< 100): +15 points
  - High fiber (> 3g): +10 points
  - Weight loss friendly flag: +25 points

- Weight Gain:
  - High calories (> 200): +15 points
  - High protein (> 15g): +10 points
  - Weight gain friendly flag: +25 points

**Budget Considerations**:
- Within 10% of daily budget: +15 points
- Exceeds 30% of daily budget: -20 points

**Nutritional Completeness**:
- Each essential nutrient (protein, fiber, vitamins, minerals): +5 points
- Rich in 3+ nutrients: +15 points

#### ML-Based Scoring

**Collaborative Filtering**:
- Users with similar profiles who accepted similar foods
- User-item matrix factorization
- Similarity-based recommendations

**Content-Based Filtering**:
- Feature extraction (calories, protein, carbs, GI, price)
- User preference learning
- Nutritional profile matching

### 3. Recommendation Generation

```python
def generate_recommendations(user, meal_type='all', limit=10):
    1. Filter foods by meal type and availability
    2. Score each food using hybrid approach
    3. Sort by score (descending)
    4. Generate explanations for top recommendations
    5. Store recommendations in database
    6. Return top N recommendations
```

### 4. Explainability

Each recommendation includes:
- **Confidence Score**: 0-1 (percentage)
- **Reasoning**: Human-readable explanation
- **Nutritional Benefits**: Key nutrients
- **Suitability**: For diabetes/goals
- **Cost**: Estimated cost per serving

## Example Recommendation

```json
{
  "food": "Beans",
  "confidence": 0.85,
  "reasoning": "Diabetes-friendly food with low glycemic index. Low GI (29) helps maintain stable blood sugar. Supports weight loss goals. High protein (21.6g) for muscle health. Rich in essential nutrients. Affordable within your budget.",
  "nutritional_benefits": [
    "High protein (21.6g) for muscle health",
    "Rich in fiber (15.2g) for digestive health",
    "Good iron source (8.2mg) for blood health"
  ],
  "suitability": {
    "diabetes": "Excellent - Low GI helps maintain stable blood sugar",
    "weight_loss": "Well-suited for your goals"
  },
  "estimated_cost": 1200.0,
  "serving_size": 100.0
}
```

## Nutritional Proof

All recommendations are based on:
- **USDA Food Database**: Nutritional values
- **Glycemic Index Database**: GI values for diabetes management
- **Medical Guidelines**: ADA (American Diabetes Association) recommendations
- **Nutritional Science**: Evidence-based dietary guidelines

### Key Nutritional Rules

1. **Diabetes Management**:
   - GI < 55: Low (recommended)
   - GI 55-70: Medium (moderate consumption)
   - GI > 70: High (avoid or limit)

2. **Weight Loss**:
   - Calorie deficit principle
   - High fiber for satiety
   - Lean proteins

3. **Weight Gain**:
   - Calorie surplus
   - High protein for muscle
   - Healthy fats

4. **General Health**:
   - Balanced macronutrients
   - Micronutrient diversity
   - Whole foods preference

## Model Training (Future Enhancement)

### Data Collection
- User interactions (accept/reject recommendations)
- Food logs
- Goal progress
- Health outcomes

### Features
- User demographics
- Health conditions
- Food nutritional profiles
- Temporal patterns
- Budget constraints

### Algorithms
- **Collaborative Filtering**: Matrix factorization
- **Content-Based**: Feature similarity
- **Deep Learning**: Neural collaborative filtering (future)

## Performance Metrics

- **Accuracy**: % of accepted recommendations
- **Diversity**: Variety in recommendations
- **Coverage**: % of foods recommended
- **Explainability**: Quality of explanations

## Continuous Improvement

1. **Feedback Loop**: User accept/reject rates
2. **A/B Testing**: Different recommendation strategies
3. **Model Retraining**: Periodic updates with new data
4. **Rule Refinement**: Update based on nutritional research

## Limitations

1. **Data Availability**: Limited to Ugandan food database
2. **User Cold Start**: New users have limited history
3. **Price Accuracy**: Depends on market API updates
4. **Medical Disclaimer**: Not a substitute for medical advice

## Future Enhancements

1. **Deep Learning Models**: Neural networks for better predictions
2. **Real-time Learning**: Online learning from user feedback
3. **Multi-objective Optimization**: Balance multiple goals
4. **Recipe Recommendations**: Meal-level recommendations
5. **Social Features**: Community-based recommendations

