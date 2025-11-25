import datetime
import os

from jwt import DecodeError
from jwt import ExpiredSignatureError
from jwt import InvalidAudienceError
from jwt import InvalidIssuerError
from jwt import InvalidTokenError
from jwt import MissingRequiredClaimError
from flask_jwt_extended.exceptions import InvalidHeaderError
from flask_jwt_extended.exceptions import NoAuthorizationError
from app.utils.api_response import apiResponse
from config import config
from flask_jwt_extended import JWTManager, create_access_token

JWT_SECRET_KEY = config[os.getenv("FLASK_ENV")].JWT_SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(
    days=int(config[os.getenv("FLASK_ENV")].JWT_ACCESS_TOKEN_EXPIRES)
)


class JWTAuthManager:
    """
    JWT Authentication Manager for handling JWT setup and custom error responses.
    """

    def __init__(self, app):
        JWTManager(app)

        @app.errorhandler(DecodeError)
        @app.errorhandler(ExpiredSignatureError)
        @app.errorhandler(InvalidTokenError)
        @app.errorhandler(InvalidAudienceError)
        @app.errorhandler(InvalidIssuerError)
        @app.errorhandler(MissingRequiredClaimError)
        @app.errorhandler(MissingRequiredClaimError)
        @app.errorhandler(InvalidHeaderError)
        @app.errorhandler(NoAuthorizationError)
        def handle_jwt_error(error_string):
            return apiResponse(
                status="error",
                status_code=401,
                message="Authentication Failed",
                payload={"error_msg": str(error_string)},
            )

    def get_auth_token():
        """
        Generate a JWT access token for a user.

        Args:
            user_identity (str/int): Identifier for the user (user ID recommended)

        Returns:
            str: JWT access token
        """

        return create_access_token(
            identity=JWT_SECRET_KEY,
            expires_delta=JWT_ACCESS_TOKEN_EXPIRES,
        )
