from flask import Blueprint

api_blueprint = Blueprint("api", __name__)
from . import health  # noqa: E402, F401
from . import auth_token  # noqa: E402, F401
from . import celery_test  # noqa: E402, F401
