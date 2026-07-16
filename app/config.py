import os

# Root of the project (one level above the /app package)
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
instance_dir = os.path.join(basedir, "instance")
os.makedirs(instance_dir, exist_ok=True)


class Config:
    """
    All sensitive values come from environment variables — nothing
    secret is hard-coded here, so this file is safe to commit and deploy.

    Local dev:  copy .env.example -> .env and fill in values
                (python-dotenv loads .env automatically, see app/__init__.py)
    Production: set SECRET_KEY / DATABASE_URL in your host's dashboard
                (Render, Railway, Heroku, etc.)
    """

    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable is not set.\n"
            "Local dev: copy .env.example to .env and set a random SECRET_KEY.\n"
            "Production: set SECRET_KEY in your hosting provider's environment settings."
        )

    # Falls back to a local SQLite file so the app runs out-of-the-box,
    # but uses DATABASE_URL (e.g. Postgres) automatically when deployed.
    _database_url = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(instance_dir, "todo.db")
    )
    # Render/Heroku hand out "postgres://" but SQLAlchemy needs "postgresql://"
    if _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookie hardening
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
