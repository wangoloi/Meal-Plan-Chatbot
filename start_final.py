"""
Final clean startup - No environment variable issues
"""
import os
import sys

def main():
    # Clean up any problematic environment variables
    for var in ['WERKZEUG_RUN_MAIN', 'WERKZEUG_SERVER_FD']:
        if var in os.environ:
            del os.environ[var]
    
    print("=" * 70)
    print("ZOE NutriTech - Starting Server")
    print("=" * 70)
    print()
    
    try:
        from app import create_app
        app = create_app()
        print("[OK] Application initialized")
    except Exception as e:
        print(f"[ERROR] Failed to create application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    port = int(os.environ.get('PORT', 5000))
    
    print()
    print("=" * 70)
    print("SERVER STARTING")
    print("=" * 70)
    print(f"Local URL:  http://127.0.0.1:{port}")
    print(f"Network URL: http://localhost:{port}")
    print("=" * 70)
    print()
    print("NOTE: This is a development server.")
    print("For production, use: python run_production.py")
    print()
    print("Press CTRL+C to stop the server")
    print()
    print("-" * 70)
    print()
    
    # Run without reloader and debugger to avoid all issues
    try:
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,  # No debug mode to avoid issues
            use_reloader=False,  # No reloader
            use_debugger=False,  # No debugger
            threaded=True
        )
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("Server stopped")
        print("=" * 70)
        return 0
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

