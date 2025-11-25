import os
from flask import Flask
from authentication.auth import JWTAuthManager
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # Load the configuration object from the imported dictionary.
    config_name = os.getenv("FLASK_ENV", "default")
    app.config.from_object(config[config_name])
    CORS(app=app, origins=app.config["ALLOWED_ORIGINS"], supports_credentials=True)
    JWTAuthManager(app)

    # Register blueprints here
    from .api import api_blueprint

    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
