from authentication.auth import JWTAuthManager
from app.utils.api_response import apiResponse
from app.utils.logger import logger
from . import api_blueprint
from flask_jwt_extended import jwt_required
import traceback


@api_blueprint.route("/get-token", methods=["POST"])
def generate_auth_token():
    """Simple login endpoint that returns JWT token."""
    try:
        # Use a secret user identifier instead of username for security
        token = JWTAuthManager.get_auth_token()
        return apiResponse(
            status="success", status_code=201, message="token created", payload={"token": token}
        )
    except Exception as e:
        error_trace = traceback.format_exc()
        return apiResponse(
            status="failed",
            message="token not created",
            payload={"error": str(e), "traceback": error_trace},
        )


@api_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():
    """Protected route that requires JWT token."""
    logger.info("Protected route accessed")
    return apiResponse(status="success", message="authentic token")
