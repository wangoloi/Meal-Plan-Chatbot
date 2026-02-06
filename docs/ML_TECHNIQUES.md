# Machine Learning Techniques Documentation

## Overview

ZOE NutriTech uses a combination of machine learning and rule-based approaches to provide personalized food recommendations. This document explains the ML techniques used and their implementation.

## ML Approaches

### 1. Hybrid Recommendation System

**Combination of**:
- Rule-based logic (explicit rules)
- Collaborative filtering (user similarity)
- Content-based filtering (item similarity)
- Matrix factorization (future)

### 2. Feature Engineering

#### User Features
```python
user_features = {
    'age': user.age,
    'gender': user.gender,
    'bmi': user.calculate_bmi(),
    'has_diabetes': 1 if user.has_diabetes else 0,
    'diabetes_type': user.diabetes_type,
    'primary_goal': user.primary_goal,
    'activity_level': user.activity_level,
    'budget_range': user.budget_range,
    'monthly_budget': user.monthly_budget
}
```

#### Food Features
```python
food_features = {
    'calories': food.calories,
    'protein': food.protein,
    'carbohydrates': food.carbohydrates,
    'fiber': food.fiber,
    'fat': food.fat,
    'sugar': food.sugar,
    'glycemic_index': food.glycemic_index,
    'sodium': food.sodium,
    'vitamin_c': food.vitamin_c,
    'iron': food.iron,
    'calcium': food.calcium,
    'current_price': food.current_price,
    'diabetes_friendly': 1 if food.diabetes_friendly else 0,
    'weight_loss_friendly': 1 if food.weight_loss_friendly else 0,
    'weight_gain_friendly': 1 if food.weight_gain_friendly else 0
}
```

#### Interaction Features
```python
interaction_features = {
    'user_food_similarity': cosine_similarity(user_vector, food_vector),
    'price_affordability': user.monthly_budget / (food.current_price * 30),
    'goal_alignment': calculate_goal_alignment(user.goal, food),
    'diabetes_compatibility': calculate_diabetes_compatibility(user, food)
}
```

### 3. Scoring Models

#### Current Implementation: Rule-Based + Similarity

**Rule-Based Scoring**:
```python
score = base_score
if user.has_diabetes:
    if food.glycemic_index < 55:
        score += 30
    elif food.glycemic_index > 70:
        score -= 30

if user.primary_goal == 'lose_weight':
    if food.calories < 100:
        score += 15
    if food.fiber > 3:
        score += 10
```

**Similarity-Based Scoring**:
```python
# User-item similarity
user_vector = [age, bmi, has_diabetes, ...]
food_vector = [calories, protein, gi, ...]
similarity = cosine_similarity(user_vector, food_vector)
score += similarity * 20
```

### 4. Future ML Models

#### Collaborative Filtering

**User-Item Matrix**:
```
        Food1  Food2  Food3  ...
User1    1      0      1
User2    1      1      0
User3    0      1      1
```

**Matrix Factorization**:
- Decompose matrix into user and item factors
- Predict missing ratings
- Find similar users/items

**Implementation** (Future):
```python
from sklearn.decomposition import NMF

# Non-negative Matrix Factorization
model = NMF(n_components=50)
user_factors, item_factors = model.fit_transform(user_item_matrix)

# Predict rating
predicted_rating = user_factors[user_id] @ item_factors[food_id]
```

#### Content-Based Filtering

**TF-IDF Vectorization**:
```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
food_descriptions = [food.description for food in foods]
tfidf_matrix = vectorizer.fit_transform(food_descriptions)

# Find similar foods
similarity = cosine_similarity(tfidf_matrix[food_id], tfidf_matrix)
```

**Feature-Based Similarity**:
```python
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

scaler = StandardScaler()
food_features_scaled = scaler.fit_transform(food_features_matrix)
similarity = cosine_similarity(food_features_scaled)
```

#### Deep Learning (Future)

**Neural Collaborative Filtering**:
```python
import torch
import torch.nn as nn

class NCF(nn.Module):
    def __init__(self, num_users, num_items, embedding_dim=50):
        super().__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.item_embedding = nn.Embedding(num_items, embedding_dim)
        self.fc_layers = nn.Sequential(
            nn.Linear(embedding_dim * 2, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
    
    def forward(self, user_ids, item_ids):
        user_emb = self.user_embedding(user_ids)
        item_emb = self.item_embedding(item_ids)
        concat = torch.cat([user_emb, item_emb], dim=1)
        return self.fc_layers(concat)
```

## Model Training

### Data Collection

**User Interactions**:
- Accepted recommendations
- Rejected recommendations
- Food logs
- Goal progress

**Features**:
- User demographics
- Health conditions
- Food nutritional profiles
- Temporal patterns

### Training Process

**1. Data Preparation**:
```python
# Load data
user_interactions = load_user_interactions()
food_features = load_food_features()
user_features = load_user_features()

# Create training set
X = combine_features(user_features, food_features)
y = user_interactions['rating']  # 1 for accepted, 0 for rejected
```

**2. Model Training**:
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
```

**3. Evaluation**:
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
```

### Model Persistence

```python
import joblib

# Save model
joblib.dump(model, 'models/recommendation_model.pkl')

# Load model
model = joblib.load('models/recommendation_model.pkl')
```

## Explainability

### Feature Importance

**Random Forest Feature Importance**:
```python
feature_importance = model.feature_importances_
feature_names = ['age', 'bmi', 'calories', 'protein', ...]

for name, importance in zip(feature_names, feature_importance):
    print(f"{name}: {importance}")
```

### SHAP Values (Future)

```python
import shap

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Visualize
shap.summary_plot(shap_values, X_test)
```

### Rule Extraction

**Extract Rules from Model**:
```python
# For decision trees
tree = model.estimators_[0]
rules = extract_rules(tree)

# Example rule:
# IF diabetes=True AND gi<55 AND calories<200 THEN recommend=True
```

## Model Updates

### Online Learning

**Incremental Updates**:
```python
from sklearn.linear_model import SGDClassifier

model = SGDClassifier()
model.partial_fit(X_new, y_new)
```

### Batch Retraining

**Scheduled Retraining**:
- Daily: Update with new interactions
- Weekly: Full model retraining
- Monthly: Feature engineering review

## Performance Metrics

### Recommendation Metrics

**Precision@K**:
```python
def precision_at_k(recommendations, accepted, k=10):
    top_k = recommendations[:k]
    relevant = sum(1 for r in top_k if r in accepted)
    return relevant / k
```

**Recall@K**:
```python
def recall_at_k(recommendations, accepted, k=10):
    top_k = recommendations[:k]
    relevant = sum(1 for r in top_k if r in accepted)
    return relevant / len(accepted)
```

**NDCG (Normalized Discounted Cumulative Gain)**:
```python
def ndcg_at_k(recommendations, accepted, k=10):
    # Calculate NDCG
    dcg = sum(1 / np.log2(i + 2) for i, r in enumerate(recommendations[:k]) if r in accepted)
    idcg = sum(1 / np.log2(i + 2) for i in range(min(k, len(accepted))))
    return dcg / idcg if idcg > 0 else 0
```

### Business Metrics

- **Acceptance Rate**: % of recommendations accepted
- **Engagement**: User interaction frequency
- **Goal Achievement**: % of users reaching goals
- **Health Outcomes**: Improvement in health metrics

## Challenges & Solutions

### Cold Start Problem

**Problem**: New users have no interaction history

**Solutions**:
1. Use demographic features
2. Content-based recommendations
3. Popular items fallback
4. Onboarding questionnaire

### Data Sparsity

**Problem**: Few user-food interactions

**Solutions**:
1. Matrix factorization
2. Content-based filtering
3. Hybrid approaches
4. Data augmentation

### Scalability

**Problem**: Large user/item base

**Solutions**:
1. Approximate nearest neighbors
2. Distributed computing
3. Model compression
4. Caching

## Future Enhancements

1. **Deep Learning**: Neural networks for better predictions
2. **Reinforcement Learning**: Learn optimal recommendations
3. **Multi-Armed Bandits**: Explore-exploit trade-off
4. **Graph Neural Networks**: User-item graph learning
5. **Transfer Learning**: Pre-trained models
6. **AutoML**: Automated model selection

## Best Practices

1. **Data Quality**: Clean, validated data
2. **Feature Engineering**: Domain knowledge
3. **Model Selection**: Try multiple approaches
4. **Evaluation**: Multiple metrics
5. **Monitoring**: Track model performance
6. **Iteration**: Continuous improvement
7. **Explainability**: Transparent decisions
8. **Ethics**: Fair, unbiased recommendations

