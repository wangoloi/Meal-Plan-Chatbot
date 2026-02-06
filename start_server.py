"""
Clean startup script for ZOE NutriTech
"""
import os
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def main():
    print("=" * 70)
    print("ZOE NutriTech - Smart Nutrition & Diabetes Support System")
    print("=" * 70)
    print()
    
    # Test imports first
    print("Initializing system...")
    try:
        from app import create_app
        print("[OK] Application module loaded")
    except Exception as e:
        print(f"[ERROR] Failed to import application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Create app
    try:
        app = create_app()
        print("[OK] Application created successfully")
    except Exception as e:
        print(f"[ERROR] Failed to create application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Get configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print()
    print("=" * 70)
    print("SERVER READY")
    print("=" * 70)
    print(f"URL:        http://localhost:{port}")
    print(f"Debug Mode: {debug}")
    print("=" * 70)
    print()
    print("Press CTRL+C to stop the server")
    print()
    
    # Run the app
    # Disable reloader to prevent watchdog issues on Windows
    try:
        app.run(host='127.0.0.1', port=port, debug=debug, use_reloader=False, use_debugger=debug)
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("Server stopped by user")
        print("=" * 70)
        return 0
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

