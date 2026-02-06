"""
Clean startup - No reloader, no watchdog issues
"""
import os
import sys

def main():
    print("=" * 70)
    print("ZOE NutriTech - Starting Server")
    print("=" * 70)
    print()
    
    # Disable Flask reloader to prevent watchdog issues
    # Don't set WERKZEUG_RUN_MAIN as it causes issues
    if 'WERKZEUG_RUN_MAIN' in os.environ:
        del os.environ['WERKZEUG_RUN_MAIN']
    if 'WERKZEUG_SERVER_FD' in os.environ:
        del os.environ['WERKZEUG_SERVER_FD']
    
    try:
        from app import create_app
        app = create_app()
        print("[OK] Application initialized")
    except Exception as e:
        print(f"[ERROR] {e}")
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
    
    # Run without reloader to avoid watchdog issues
    try:
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,  # Set to False to avoid debugger issues
            use_reloader=False,  # Disable reloader
            use_debugger=False,  # Disable debugger to avoid issues
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

