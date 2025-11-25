from app.utils.logger import logger
from wsgi import ai_server

logger.info("Starting app")
entry = ai_server
