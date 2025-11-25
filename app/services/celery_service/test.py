from time import sleep
from celery_worker.celery_setup import celery_app


@celery_app.task(name="addition_task")  # explicitly name it 'addition'
def addition(x, y):
    sleep(20)
    return x + y
