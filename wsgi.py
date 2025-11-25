# /your_project_name/wsgi.py

import os
from app import create_app
from app.utils.logger import logger

# Create the Flask application instance using the factory
project = os.environ.get("PROJECT_NAME", "TEST PROJECT")
logger.info(f"Starting {project}.....")
ai_server = create_app()

if __name__ == "__main__":
    ai_server.run(host="0.0.0.0")
