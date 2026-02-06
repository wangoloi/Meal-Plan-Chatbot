"""
Test all routes to identify browser errors
"""
from app import create_app
from flask.testing import FlaskClient

def test_routes():
    app = create_app()
    client = app.test_client()
    
    print("=" * 70)
    print("Testing All Routes")
    print("=" * 70)
    print()
    
    routes_to_test = [
        ('/', 'GET', 'Home page'),
        ('/auth/register', 'GET', 'Register page'),
        ('/auth/login', 'GET', 'Login page'),
    ]
    
    errors = []
    
    for route, method, description in routes_to_test:
        try:
            if method == 'GET':
                response = client.get(route)
                status = response.status_code
                
                if status == 200:
                    print(f"[OK] {description:30} {route:30} Status: {status}")
                elif status == 302 or status == 301:
                    print(f"[REDIRECT] {description:30} {route:30} Status: {status}")
                else:
                    print(f"[ERROR] {description:30} {route:30} Status: {status}")
                    errors.append(f"{route}: Status {status}")
                    # Print error details
                    try:
                        print(f"         Response: {response.data[:200]}")
                    except:
                        pass
        except Exception as e:
            print(f"[EXCEPTION] {description:30} {route:30} Error: {e}")
            errors.append(f"{route}: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 70)
    if errors:
        print(f"Found {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1
    else:
        print("All routes working correctly!")
        return 0

if __name__ == '__main__':
    import sys
    sys.exit(test_routes())

