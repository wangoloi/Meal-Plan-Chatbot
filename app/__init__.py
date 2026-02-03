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

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        "sqlite:///{basedir / 'instance' / 'zoenutritech.db'}" 
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.env = os.getenv('FLASK_ENV', config_name)

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

    # ── Register blueprints (add more later) ───────────────────────
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # Optional: basic health check route (good for first phase verification)
    @app.route('/health')
    def health():
        return {"status": "ok", "env": app.env}, 200

    return app