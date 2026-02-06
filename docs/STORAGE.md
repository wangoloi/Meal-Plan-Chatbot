# Storage Architecture Documentation

## Overview

ZOE NutriTech uses a multi-tier storage architecture to efficiently manage data, cache frequently accessed information, and support offline functionality.

## Storage Layers

### 1. Primary Database (SQLite/PostgreSQL)

**Purpose**: Primary data storage

**Technology**:
- Development: SQLite
- Production: PostgreSQL

**Stored Data**:
- User accounts and profiles
- Food items database
- Recommendations
- Diabetes records
- Goals and progress
- Chat history
- Food prices

**Characteristics**:
- ACID compliance
- Relational data model
- Indexed for performance
- Backed up regularly

### 2. File System Storage

**Purpose**: Static files and cache

**Directories**:
```
project/
├── models/              # ML model files
├── offline_cache/      # Offline data cache
├── uploads/            # User uploads (future)
└── static/             # Static assets
```

**Stored Data**:
- ML model files (`.pkl`)
- Offline cache files (JSON)
- User-uploaded images (future)

### 3. In-Memory Cache (Future: Redis)

**Purpose**: Fast data access

**Technology**: Redis (planned)

**Cached Data**:
- Session data
- Frequently accessed food items
- Search results
- Recommendation results
- User preferences

**Cache Strategy**:
- TTL-based expiration
- LRU eviction
- Cache invalidation on updates

## Database Schema

### Tables Overview

#### users
- Primary key: `id`
- Indexes: `username`, `email`
- Relationships: One-to-many with recommendations, goals, records

#### food_items
- Primary key: `id`
- Indexes: `name`, `category`, `diabetes_friendly`
- Relationships: One-to-many with recommendations, food_logs

#### recommendations
- Primary key: `id`
- Foreign keys: `user_id`, `food_item_id`
- Indexes: `user_id`, `created_at`
- Stores: Recommendations with explanations

#### diabetes_records
- Primary key: `id`
- Foreign key: `user_id`
- Indexes: `user_id`, `created_at`, `record_type`
- Stores: Blood glucose, insulin, HbA1c records

#### goals
- Primary key: `id`
- Foreign key: `user_id`
- Indexes: `user_id`, `status`
- Stores: User goals and progress

#### food_logs
- Primary key: `id`
- Foreign keys: `user_id`, `food_item_id`
- Indexes: `user_id`, `consumed_at`
- Stores: User food consumption

#### chat_history
- Primary key: `id`
- Foreign key: `user_id`
- Indexes: `user_id`, `created_at`
- Stores: Chatbot conversations

#### food_prices
- Primary key: `id`
- Foreign key: `food_item_id`
- Indexes: `food_item_id`, `recorded_at`
- Stores: Price history

## Data Models

### User Model
```python
class User:
    - id
    - username, email
    - password_hash
    - Personal info (name, age, gender, height, weight)
    - Health info (diabetes, goals, budget)
    - Relationships: recommendations, goals, records
```

### Food Item Model
```python
class FoodItem:
    - id
    - name, local_name, category
    - Nutritional data (calories, protein, carbs, etc.)
    - Price information
    - Flags (diabetes_friendly, etc.)
```

### Recommendation Model
```python
class Recommendation:
    - id
    - user_id, food_item_id
    - recommendation_type, confidence_score
    - reasoning, explanation
    - serving_size, estimated_cost
    - ML metadata
```

## Data Access Patterns

### Read Operations

**Frequent Reads**:
- Food items (cached)
- User profile (session)
- Recent recommendations
- Active goals

**Optimization**:
- Database indexes
- Query optimization
- Result caching

### Write Operations

**Frequent Writes**:
- Food logs
- Diabetes records
- Goal progress updates
- Chat messages

**Optimization**:
- Batch inserts
- Transaction management
- Async writes (future)

## Offline Storage

### Offline Cache Structure

```json
{
    "user": {...},
    "food_items": [...],
    "recommendations": [...],
    "goals": [...],
    "cached_at": "2024-01-01T00:00:00Z"
}
```

### Cache Management

**Creation**:
- When offline mode enabled
- Includes essential data
- JSON format for portability

**Usage**:
- Load when offline
- Fallback for slow connections
- Sync when online

**Expiration**:
- Time-based (24 hours)
- Manual refresh
- Auto-sync on connection

## Backup Strategy

### Database Backups

**Frequency**: Daily

**Method**:
- Automated SQL dumps
- Point-in-time recovery
- Backup verification

**Storage**:
- Local backup server
- Cloud storage (future)
- Encrypted backups

### File Backups

**Frequency**: Weekly

**Method**:
- Archive old files
- Compress storage
- Version control

## Data Migration

### Schema Changes

**Tool**: Flask-Migrate

**Process**:
1. Create migration script
2. Test on development
3. Apply to staging
4. Apply to production

### Data Migration

**Process**:
1. Backup existing data
2. Run migration script
3. Verify data integrity
4. Update application code

## Performance Optimization

### Database Optimization

**Indexes**:
- Primary keys (automatic)
- Foreign keys
- Frequently queried columns
- Composite indexes for complex queries

**Query Optimization**:
- Use indexes effectively
- Avoid N+1 queries
- Limit result sets
- Use pagination

### Caching Strategy

**Cache Levels**:
1. Application cache (in-memory)
2. Database query cache
3. CDN cache (static assets)

**Cache Invalidation**:
- Time-based (TTL)
- Event-based (on updates)
- Manual refresh

## Data Security

### Encryption

**At Rest**:
- Database encryption (PostgreSQL)
- File encryption (sensitive files)
- Backup encryption

**In Transit**:
- HTTPS/TLS
- Encrypted API calls
- Secure database connections

### Access Control

**Database**:
- User-based permissions
- Read-only replicas
- Connection limits

**File System**:
- File permissions
- Restricted access
- Audit logging

## Scalability Considerations

### Database Scaling

**Vertical Scaling**:
- Increase server resources
- Optimize queries
- Add indexes

**Horizontal Scaling**:
- Read replicas
- Sharding (future)
- Database clustering

### Storage Scaling

**File Storage**:
- Object storage (S3)
- CDN for static assets
- Distributed file system

## Monitoring

### Database Monitoring

**Metrics**:
- Query performance
- Connection pool usage
- Storage usage
- Replication lag

**Tools**:
- Database logs
- Performance monitoring
- Alerting system

### Storage Monitoring

**Metrics**:
- Disk usage
- Cache hit rates
- Backup status
- File access patterns

## Disaster Recovery

### Recovery Procedures

1. **Database Recovery**:
   - Restore from backup
   - Point-in-time recovery
   - Verify data integrity

2. **File Recovery**:
   - Restore from backup
   - Rebuild cache
   - Verify files

### Recovery Time Objectives (RTO)

- Database: < 1 hour
- Application: < 30 minutes
- Cache: < 15 minutes

## Future Enhancements

1. **Redis Integration**: In-memory caching
2. **Object Storage**: S3 for files
3. **CDN**: Global content delivery
4. **Data Warehouse**: Analytics storage
5. **Time-Series DB**: Metrics storage

