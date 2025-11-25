from typing import Any

from flask import jsonify


def apiResponse(
    status: str,
    message: str,
    payload: Any = {},
    status_code: int = 200,
):
    response = {"status": status, "message": message, "payload": payload}

    return jsonify(response), status_code
