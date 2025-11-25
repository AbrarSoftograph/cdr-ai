import os
from celery import Celery
from configs.celery_config import celery_config_dict
from dotenv import load_dotenv

load_dotenv()


def make_celery():
    celery = Celery(
        main="Test_Project",
        broker=celery_config_dict["CELERY_BROKER_URL"],
        backend=celery_config_dict["CELERY_BACKEND_URL"],
    )
    celery.conf.update(include=["app.api", "app.services"])
    celery.conf.result_backend_transport_options = {
        "global_keyprefix": os.getenv(("REDIS_KEY_PREFIX"), "ai_api_service")
    }
    celery.autodiscover_tasks(force=True)
    return celery


# Global Celery app for entire project
celery_app = make_celery()
