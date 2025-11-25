import os
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

redisUsername = os.getenv("REDIS_USERNAME", "")
redisPassword = quote(os.getenv("REDIS_PASSWORD", ""))
redisHost = os.getenv("REDIS_HOST", "localhost")
redisPort = os.getenv("REDIS_PORT", "6379")
redisDb = os.getenv("REDIS_DB", "0")
redisUrl = f"redis://{redisUsername}:{redisPassword}@{redisHost}:{redisPort}/{redisDb}"

celeryUsername = os.getenv("CELERY_BROKER_USERNAME", "guest")
celeryPassword = quote(os.getenv("CELERY_BROKER_PASSWORD", "guest"))
celeryHost = os.getenv("CELERY_BROKER_HOST", "localhost")
celeryPort = os.getenv("CELERY_BROKER_PORT", "5729")
celeryBrokerUrl = f"amqp://{celeryUsername}:{celeryPassword}@{celeryHost}:{celeryPort}//"


celery_config_dict = {
    "CELERY_BROKER_URL": celeryBrokerUrl,
    "CELERY_BACKEND_URL": redisUrl,
    "CELERY_TASK_SERIALIZER": "json",
    "CELERY_ACCEPT_CONTENT": ["json"],
    "CELERY_TIMEZONE": "Asia/Dhaka",
}
