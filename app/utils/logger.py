import logging
import logging.handlers
import threading
from datetime import datetime, timedelta
import os
from config import config
from flask import request
from dotenv import load_dotenv

load_dotenv()

proj_name = config[os.getenv("FLASK_ENV")].PROJECT_NAME


class RequestFormatter(logging.Formatter):
    """Custom formatter that includes IP address in log messages"""

    def format(self, record):
        record.ip = get_client_ip()
        return super().format(record)


def get_client_ip() -> str:
    """Get client IP address from Flask request"""
    try:
        # Handle proxy headers
        if request.headers.get("X-Forwarded-For"):
            return request.headers.get("X-Forwarded-For").split(",")[0].strip()
        elif request.headers.get("X-Real-IP"):
            return request.headers.get("X-Real-IP")
        else:
            return request.remote_addr or "unknown"
    except RuntimeError:
        return "N/A"


def setup_logger(
    name: str = proj_name, log_level: int = logging.DEBUG, log_dir: str = "logs"
) -> logging.Logger:
    """Setup logger with midnight rotation and IP tracking

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_dir: Directory to store log files

    Returns:
        Configured logger instance
    """

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.getcwd(), log_dir)
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()

    # Create timed rotating file handler (rotates at midnight)
    log_filename = os.path.join(log_dir, "app.log")
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_filename,
        when="midnight",  # Rotate at midnight
        interval=1,
        backupCount=30,  # Keep 30 days of logs
    )
    file_handler.setLevel(log_level)

    # Create formatter with IP
    formatter = RequestFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(ip)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set formatter
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    # Schedule automatic rollover at midnight
    def schedule_rollover():
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        delay = (next_midnight - now).total_seconds()
        timer = threading.Timer(delay, lambda: (file_handler.doRollover(), schedule_rollover()))
        timer.daemon = True
        timer.start()

    schedule_rollover()

    return logger


def get_logger(name: str = proj_name) -> logging.Logger:
    """Get logger instance - creates it if it doesn't exist"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger = setup_logger(name)
    return logger


# Global logger instance
logger = get_logger()
