from app.utils.api_response import apiResponse
from app.utils.logger import logger
from . import api_blueprint
from flask_jwt_extended import jwt_required


@api_blueprint.route("/health", methods=["GET"])
@jwt_required()
@jwt_required()
def health_check():
    """Health check endpoint that requires JWT authentication."""
    logger.info("Health check performed")
    return apiResponse(status="success", message="ai api running")
