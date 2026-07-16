from dotenv import load_dotenv

# Loads variables from a local .env file if present (local dev only —
# in production the host injects real environment variables directly).
load_dotenv()

from flask import Flask

from .config import Config
from .extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth_bp
    from .routes.todos import todos_bp
    from .routes.profile import profile_bp
    from .routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(todos_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(main_bp)

    return app
