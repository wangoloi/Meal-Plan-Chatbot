"""
Final system verification - All errors fixed
"""
import sys

def main():
    print("=" * 70)
    print("ZOE NutriTech - Final System Verification")
    print("=" * 70)
    print()
    
    # Test 1: Imports
    print("1. Testing imports...")
    try:
        from app import create_app
        print("   [OK] Application imports")
    except Exception as e:
        print(f"   [ERROR] {e}")
        return 1
    
    # Test 2: App creation
    print("2. Testing app creation...")
    try:
        app = create_app()
        print("   [OK] App created successfully")
    except Exception as e:
        print(f"   [ERROR] {e}")
        return 1
    
    # Test 3: Templates
    print("3. Testing templates...")
    try:
        from flask import render_template_string
        with app.app_context():
            render_template_string("Test")
        print("   [OK] Templates accessible")
    except Exception as e:
        print(f"   [ERROR] {e}")
        return 1
    
    # Test 4: Routes
    print("4. Testing routes...")
    try:
        from flask.testing import FlaskClient
        client = app.test_client()
        
        routes = [
            ('/', 'Home'),
            ('/auth/register', 'Register'),
            ('/auth/login', 'Login'),
        ]
        
        all_ok = True
        for route, name in routes:
            response = client.get(route)
            if response.status_code == 200:
                print(f"   [OK] {name:15} {route}")
            else:
                print(f"   [ERROR] {name:15} {route} - Status: {response.status_code}")
                all_ok = False
        
        if not all_ok:
            return 1
    except Exception as e:
        print(f"   [ERROR] {e}")
        return 1
    
    # Test 5: Database
    print("5. Testing database...")
    try:
        with app.app_context():
            from app.models import FoodItem
            count = FoodItem.query.count()
            print(f"   [OK] Database accessible ({count} foods)")
    except Exception as e:
        print(f"   [ERROR] {e}")
        return 1
    
    # Test 6: Services
    print("6. Testing services...")
    try:
        from app.services.recommendation_engine import RecommendationEngine
        from app.services.search_engine import SearchEngine
        from app.services.chatbot_service import ChatbotService
        
        engine = RecommendationEngine()
        search = SearchEngine()
        chatbot = ChatbotService()
        
        print("   [OK] All services initialized")
    except Exception as e:
        print(f"   [ERROR] {e}")
        return 1
    
    print()
    print("=" * 70)
    print("[SUCCESS] All systems operational!")
    print("=" * 70)
    print()
    print("To start the server:")
    print("  python start_clean.py       (Development, no reloader)")
    print("  python run_production.py    (Production with Waitress)")
    print()
    print("Access at: http://127.0.0.1:5000")
    print("=" * 70)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

