"""
Comprehensive system test to identify and fix errors
"""
import sys
import traceback

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    errors = []
    
    try:
        from flask import Flask
        print("  [OK] Flask")
    except Exception as e:
        errors.append(f"Flask: {e}")
        print(f"  [ERROR] Flask: {e}")
    
    try:
        from app import create_app, db
        print("  [OK] App module")
    except Exception as e:
        errors.append(f"App module: {e}")
        print(f"  [ERROR] App module: {e}")
        traceback.print_exc()
        return errors
    
    try:
        from app.models import User, FoodItem, Recommendation, DiabetesRecord, Goal, ChatHistory
        print("  [OK] Models")
    except Exception as e:
        errors.append(f"Models: {e}")
        print(f"  [ERROR] Models: {e}")
        traceback.print_exc()
    
    try:
        from app.services.recommendation_engine import RecommendationEngine
        print("  [OK] Recommendation Engine")
    except Exception as e:
        errors.append(f"Recommendation Engine: {e}")
        print(f"  [ERROR] Recommendation Engine: {e}")
        traceback.print_exc()
    
    try:
        from app.services.search_engine import SearchEngine
        print("  [OK] Search Engine")
    except Exception as e:
        errors.append(f"Search Engine: {e}")
        print(f"  [ERROR] Search Engine: {e}")
        traceback.print_exc()
    
    try:
        from app.services.chatbot_service import ChatbotService
        print("  [OK] Chatbot Service")
    except Exception as e:
        errors.append(f"Chatbot Service: {e}")
        print(f"  [ERROR] Chatbot Service: {e}")
        traceback.print_exc()
    
    return errors

def test_app_creation():
    """Test app creation"""
    print("\nTesting app creation...")
    try:
        from app import create_app
        app = create_app()
        print("  [OK] App created successfully")
        return app, None
    except Exception as e:
        print(f"  [ERROR] App creation failed: {e}")
        traceback.print_exc()
        return None, str(e)

def test_database():
    """Test database operations"""
    print("\nTesting database...")
    try:
        from app import create_app, db
        from app.models import User, FoodItem
        
        app = create_app()
        with app.app_context():
            # Test query
            user_count = User.query.count()
            food_count = FoodItem.query.count()
            print(f"  [OK] Database accessible")
            print(f"    Users: {user_count}, Foods: {food_count}")
        return None
    except Exception as e:
        print(f"  [ERROR] Database error: {e}")
        traceback.print_exc()
        return str(e)

def test_services():
    """Test service initialization"""
    print("\nTesting services...")
    errors = []
    
    try:
        from app.services.recommendation_engine import RecommendationEngine
        engine = RecommendationEngine()
        print("  [OK] Recommendation Engine initialized")
    except Exception as e:
        errors.append(f"Recommendation Engine: {e}")
        print(f"  [ERROR] Recommendation Engine: {e}")
        traceback.print_exc()
    
    try:
        from app.services.search_engine import SearchEngine
        search = SearchEngine()
        print("  [OK] Search Engine initialized")
    except Exception as e:
        errors.append(f"Search Engine: {e}")
        print(f"  [ERROR] Search Engine: {e}")
        traceback.print_exc()
    
    try:
        from app.services.chatbot_service import ChatbotService
        chatbot = ChatbotService()
        print("  [OK] Chatbot Service initialized")
    except Exception as e:
        errors.append(f"Chatbot Service: {e}")
        print(f"  ✗ Chatbot Service: {e}")
        traceback.print_exc()
    
    return errors

def test_routes():
    """Test route registration"""
    print("\nTesting routes...")
    try:
        from app import create_app
        app = create_app()
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(str(rule))
        
        print(f"  [OK] {len(routes)} routes registered")
        print(f"    Sample routes: {routes[:5]}")
        return None
    except Exception as e:
        print(f"  [ERROR] Route error: {e}")
        traceback.print_exc()
        return str(e)

def main():
    print("=" * 60)
    print("ZOE NutriTech - System Diagnostic Test")
    print("=" * 60)
    
    all_errors = []
    
    # Test imports
    import_errors = test_imports()
    if import_errors:
        all_errors.extend(import_errors)
        print("\n[ERROR] Critical import errors found. Fix these first.")
        return 1
    
    # Test app creation
    app, error = test_app_creation()
    if error:
        all_errors.append(error)
        return 1
    
    # Test database
    db_error = test_database()
    if db_error:
        all_errors.append(db_error)
    
    # Test services
    service_errors = test_services()
    if service_errors:
        all_errors.extend(service_errors)
    
    # Test routes
    route_error = test_routes()
    if route_error:
        all_errors.append(route_error)
    
    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print(f"[ERROR] Found {len(all_errors)} error(s)")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        return 1
    else:
        print("[SUCCESS] All tests passed! System is ready.")
        print("=" * 60)
        print("\nTo start the server, run:")
        print("  python start.py")
        print("  or")
        print("  python run.py")
        return 0

if __name__ == '__main__':
    sys.exit(main())

