"""
Enhanced startup script with clear output
"""
import os
import sys
from app import create_app

def main():
    print("=" * 60)
    print("ZOE NutriTech - Smart Nutrition & Diabetes Support System")
    print("=" * 60)
    print()
    
    # Check environment
    print("Checking environment...")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Create app
    print("Initializing application...")
    try:
        app = create_app()
        print("✓ Application initialized successfully!")
        print()
    except Exception as e:
        print(f"✗ Error initializing application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Get configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("=" * 60)
    print("Server Configuration:")
    print(f"  Host: 0.0.0.0 (all interfaces)")
    print(f"  Port: {port}")
    print(f"  Debug: {debug}")
    print("=" * 60)
    print()
    print("Starting Flask development server...")
    print(f"Access the application at: http://localhost:{port}")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    # Run the app
    try:
        app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("Server stopped by user")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"✗ Error running server: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

