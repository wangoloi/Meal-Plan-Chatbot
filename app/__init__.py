import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables as early as possible
load_dotenv()

# Extension instances (global style - common and works well for most medium apps)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='development'):
    """
    Application factory - creates and configures Flask app.
    Use different config names or config classes later for prod/test.
    """
    # Use project root (one level up from app/) for templates/static
    basedir = Path(__file__).resolve().parents[1]

    app = Flask(__name__,
                template_folder=basedir / 'templates',
                static_folder=basedir / 'static') 

    # ── Basic configuration ────────────────────────────────────────
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if not app.config['SECRET_KEY']:
        if app.env == 'production':
            raise RuntimeError("SECRET_KEY environment variable is required in production")
        app.config['SECRET_KEY'] = 'dev-only-insecure-key-change-me'

    # Database configuration - Use AppData to avoid OneDrive sync issues
    # This ensures the database works even if project is in OneDrive folder
    if os.name == 'nt':  # Windows
        # Use user's AppData\Local folder (not synced by OneDrive)
        appdata_dir = Path(os.getenv('LOCALAPPDATA', os.path.expanduser('~/.local')))
        db_dir = appdata_dir / 'Glocusense'
        db_dir.mkdir(exist_ok=True)
        db_file = db_dir / 'glocusense.db'
        db_path = str(db_file.resolve()).replace('\\', '/')
        db_uri = f"sqlite:///{db_path}"
    else:
        # Linux/Mac - use instance directory
        instance_dir = basedir / 'instance'
        instance_dir.mkdir(exist_ok=True)
        db_file = instance_dir / 'glocusense.db'
        db_path = str(db_file.resolve()).replace('\\', '/')
        db_uri = f"sqlite:///{db_path}"
    
    # Allow override via environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', db_uri)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.env = os.getenv('FLASK_ENV', config_name)
    
    # Disable template caching in development for easier debugging
    if app.env == 'development':
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.jinja_env.auto_reload = True

    # ── Initialize extensions ──────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'          # Blueprint + view function name

    # User loader for Flask-Login (late import avoids circular imports)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # ── Register blueprints ───────────────────────
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.diabetes import diabetes_bp
    from app.routes.search import search_bp
    from app.routes.recommendations import recommendations_bp
    from app.routes.chatbot import chatbot_bp
    from app.routes.goals import goals_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(diabetes_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # Optional: basic health check route (good for first phase verification)
    @app.route('/health')
    def health():
        return {"status": "ok", "env": app.env}, 200
    
    # Add cache-busting headers for static files in development
    @app.after_request
    def add_no_cache_headers(response):
        if app.env == 'development':
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response

    return app