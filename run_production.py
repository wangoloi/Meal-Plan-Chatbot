"""
Production-ready server startup
Uses waitress for Windows (no compilation needed)
"""
import os
import sys

def main():
    print("=" * 70)
    print("ZOE NutriTech - Production Server")
    print("=" * 70)
    print()
    
    try:
        from app import create_app
        app = create_app()
        print("[OK] Application created")
    except Exception as e:
        print(f"[ERROR] Failed to create application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Try to use waitress (Windows-friendly WSGI server)
    try:
        from waitress import serve
        port = int(os.environ.get('PORT', 5000))
        
        print("=" * 70)
        print("Starting production server with Waitress...")
        print(f"URL: http://localhost:{port}")
        print("=" * 70)
        print("Press CTRL+C to stop")
        print()
        
        serve(app, host='127.0.0.1', port=port, threads=4)
        return 0
    except ImportError:
        print("[INFO] Waitress not installed. Using Flask development server.")
        print("[INFO] For production, install: pip install waitress")
        print()
        
        # Fall back to development server
        port = int(os.environ.get('PORT', 5000))
        print(f"Starting development server on http://127.0.0.1:{port}")
        print("Press CTRL+C to stop")
        print()
        
        app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)
        return 0
    except KeyboardInterrupt:
        print("\nServer stopped")
        return 0
    except Exception as e:
        print(f"[ERROR] Server error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

