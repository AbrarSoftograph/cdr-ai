from flask import request
from app.services.celery_service.test import addition
from app.utils.api_response import apiResponse
from app.utils.logger import logger
from . import api_blueprint
from flask_jwt_extended import jwt_required
from celery.result import AsyncResult
from celery_worker.celery_setup import celery_app
import traceback


@api_blueprint.route("/celery/worker", methods=["POST"])
@jwt_required()
def celery_check():
    try:
        data = request.get_json()
        x = data.get("x", 0)
        y = data.get("y", 0)
        task_id = addition.delay(x, y)
        """Celery worker endpoint check"""
        logger.info("Worker endpoint check performed")
        return apiResponse(
            status="success", message="Task queued", payload={"task_id": str(task_id)}
        )
    except Exception as e:
        error_trace = traceback.format_exc()
        logger.error(error_trace)
        return apiResponse(
            status="error",
            message="Failed to process celery_check",
            status_code=500,
            payload={"error_msg": str(e), "traceback": error_trace},
        )


@api_blueprint.route("/celery/task/<task_id>", methods=["GET"])
@jwt_required()
def get_task_status(task_id):
    try:
        task_result = AsyncResult(task_id, backend=celery_app.backend)
        task_state = task_result.state
        task_status = "Task is in state: {}".format(task_state)

        payload = {"task_id": task_id, "state": task_state}
        logger.info(str(payload))
        if task_result.ready():
            payload["result"] = (
                task_result.result if task_state == "SUCCESS" else str(task_result.result)
            )
            task_status += " - Result: {}".format(payload["result"])
        else:
            payload["progress"] = "Task is still running or pending"

        logger.info(f"Task status checked for task_id: {task_id} - State: {task_state}")
        return apiResponse(status="success", message=task_status, payload=payload)
    except Exception as e:
        return apiResponse(
            status="error",
            message="Failed to get task status",
            status_code=500,
            payload={"error_msg": str(e)},
        )
