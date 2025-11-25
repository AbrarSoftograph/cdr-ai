import json
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class Config:
    """Base configuration class with settings common to all environments."""

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRES = os.getenv("JWT_ACCESS_TOKEN_EXPIRES")
    PROJECT_NAME = os.getenv("PROJECT_NAME", "Project-X")


class DevelopmentConfig(Config):
    """Configuration for the development environment."""

    DEBUG = True
    # Specifies the database URI. For development, we use a simple SQLite database.
    # It can be overridden by the DEV_DATABASE_URL environment variable if needed.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "dev-database.db"
    )
    ALLOWED_ORIGINS = json.loads(os.getenv("ALLOWED_ORIGINS", []))


class ProductionConfig(Config):
    """Configuration for the production environment."""

    # DEBUG must be False in production for security and performance.
    DEBUG = False

    # In production, the database URI must be set via an environment variable.
    # There is no fallback, so the application will fail to start if it's missing,
    # which is a good safety measure.
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "dev-database.db"
    )


# A dictionary to map string names to the actual configuration classes.
# This makes it easy to select the configuration in the application factory.
