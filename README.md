# AI Server Template

A comprehensive Flask-based boilerplate for building AI-powered web services with asynchronous task processing and secure authentication.

## Features

- **Flask Web Framework**: RESTful API with Blueprint architecture
- **Asynchronous Task Processing**: Celery with Redis backend and RabbitMQ broker
- **Authentication**: JWT-based security with customizable token expiration
- ~~**Database**: SQLAlchemy ORM with SQLite/PostgreSQL support~~ (Not implemented yet)
- **Monitoring**: Flower dashboard for Celery task monitoring
- **Production Ready**: Gunicorn WSGI server
- **Environment Management**: Multi-environment configuration (development/production)
- **Logging**: Structured logging with configurable levels

## Quick Start

### Prerequisites

- Python 3.12+
- Docker (for Redis/RabbitMQ, optional but recommended)
- uv (for dependency management)

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd ai-server-template
   uv sync
   ```

2. **Environment Configuration:**
   Create a `.env` file in the root directory:
   ```bash
   # JWT Configuration
   JWT_SECRET_KEY=your-super-secret-jwt-key
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRES=30

   # Celery Configuration (RabbitMQ)
   CELERY_BROKER_USERNAME=guest
   CELERY_BROKER_PASSWORD=guest
   CELERY_BROKER_HOST=localhost
   CELERY_BROKER_PORT=5672

   # Redis Configuration
   REDIS_USERNAME=
   REDIS_PASSWORD=
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   REDIS_KEY_PREFIX=ai_api_service

   # Application Configuration
   FLASK_ENV=development
   PROJECT_NAME=AI Server Template
   ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5000"]
   ```

### Running the Application

1. **Start Redis (required for Celery backend):**
   ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```

2. **Start RabbitMQ (optional, for message broker):**
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
   ```

3. **Start the Flask application:**
   ```bash
   # Development
   uv run python wsgi.py

   # Production
   uv run gunicorn -w 4 -b 0.0.0.0:8000 wsgi:ai_server
   ```

4. **Start Celery Worker:**
   ```bash
   # With Redis as broker (default)
   uv run celery -A celery_worker.celery_setup.celery_app worker --loglevel=info --hostname=worker1@%h 

   # With RabbitMQ as broker
   # Set CELERY_BROKER_URL in .env to: amqp://guest:guest@localhost:5672//
   uv run celery -A celery_worker.celery_setup.celery_app worker --loglevel=info --hostname=worker1@%h
   ```

   - Use ```--pool = solo``` for windows systems.

5. **Monitor Celery Tasks (Flower):**
   ```bash
   uv run celery -A celery_worker.celery_setup.celery_app flower --port=5555
   ```
   Visit `http://localhost:5555` to access the Flower monitoring dashboard.

## Architecture

```
ai-server-template/
├── app/                    # Flask application
│   ├── __init__.py        # Application factory
│   ├── api/               # API blueprints
│   │   ├── __init__.py
│   │   ├── auth_token.py  # Authentication endpoints
│   │   ├── celery_test.py # Celery task endpoints
│   │   └── health.py      # Health check
│   ├── services/          # Business logic and Celery tasks
│   │   └── celery_service/
│   │       └── test.py    # Sample async tasks
│   ├── models/            # SQLAlchemy models
│   ├── ml_models/         # ML model storage
│   ├── utils/             # Utilities (logging, responses)
│   └── __init__.py
├── authentication/        # JWT authentication setup
├── celery_worker/         # Celery configuration
├── configs/               # Environment configurations
├── docs/                  # Documentation
├── notebooks/             # Jupyter notebooks
└── tests/                 # Test suite
```

## Using Celery for Asynchronous Tasks

### Why Celery?

Celery enables asynchronous task execution, allowing your AI server to:
- Process long-running ML inference tasks without blocking API responses
- Scale task processing with multiple workers
- Monitor task progress and results
- Handle task failures gracefully
- Queue and prioritize tasks intelligently

### Defining Tasks

Create tasks in the `app/services/` directory. Tasks are automatically discovered from modules specified in `celery_setup.py`.

```python
# app/services/ml_tasks.py
from celery_worker.celery_setup import celery_app

@celery_app.task(name="ml_inference")
def ml_inference(model_name, input_data):
    # Simulate ML processing time
    import time
    time.sleep(10)

    # Your ML inference logic here
    result = {"prediction": "example_prediction", "confidence": 0.95}
    return result
```

### Calling Tasks from API

Create API endpoints that trigger Celery tasks:

```python
# app/api/ml_api.py
from flask import request
from flask_jwt_extended import jwt_required
from app.services.ml_tasks import ml_inference
from app.utils.api_response import apiResponse
from . import api_blueprint

@api_blueprint.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    try:
        data = request.get_json()
        model_name = data.get("model_name")
        input_data = data.get("input_data")

        # Queue the task asynchronously
        task = ml_inference.delay(model_name, input_data)

        return apiResponse(
            status="success",
            message="Prediction task queued",
            payload={"task_id": str(task.id)}
        )
    except Exception as e:
        return apiResponse(
            status="error",
            message="Failed to queue prediction task",
            status_code=500,
            payload={"error": str(e)}
        )
```

### Checking Task Status

Create endpoints to monitor task progress:

```python
@api_blueprint.route("/task/<task_id>", methods=["GET"])
@jwt_required()
def get_task_status(task_id):
    from celery.result import AsyncResult
    from celery_worker.celery_setup import celery_app

    task_result = AsyncResult(task_id, backend=celery_app.backend)
    task_state = task_result.state

    response = {"task_id": task_id, "state": task_state}

    if task_result.ready():
        if task_state == "SUCCESS":
            response["result"] = task_result.result
        else:
            response["error"] = str(task_result.result)
    else:
        response["progress"] = "Task is still running or pending"

    status_message = f"Task is in state: {task_state}"
    return apiResponse(status="success", message=status_message, payload=response)
```

### Task Examples

**Queue a task:**
```bash
curl -X POST http://localhost:5000/api/celery/worker \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"x": 10, "y": 20}'
```

**Check task status:**
```bash
curl -X GET http://localhost:5000/api/celery/task/TASK_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Authentication Implementation

### JWT Authentication Flow

The template uses Flask-JWT-Extended for secure authentication:

1. **Token Generation**: Generate JWT tokens
2. **Token Validation**: Validate tokens on protected routes
3. **Token Expiration**: Automatic token expiration

### Configuration

Set JWT parameters in your `.env` file:

```bash
JWT_SECRET_KEY=your-random-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES=30  # days
```

### Authentication Endpoints

**Generate Token:**
```bash
# POST /api/get-token
curl -X POST http://localhost:5000/api/get-token
```

**Use Protected Route:**
```bash
curl -X GET http://localhost:5000/api/protected \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Protecting Routes

Use the `@jwt_required()` decorator to secure endpoints:

```python
from flask_jwt_extended import jwt_required

@api_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():
    return {"message": "You are authenticated!"}
```

### Custom Authentication Logic

Extend the `JWTAuthManager` class in `authentication/auth.py` to customize error handling and authentication behavior as needed.

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/get-token` | Get JWT authentication token | No |
| GET | `/api/protected` | Test protected route | Yes |
| POST | `/api/celery/worker` | Queue an async addition task | Yes |
| GET | `/api/celery/task/<task_id>` | Check task status | Yes |
| GET | `/api/health` | Health check | No |

## Configuration

### Environment Variables

Key environment variables supported:

- `FLASK_ENV`: `development` or `production`
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `JWT_ACCESS_TOKEN_EXPIRES`: Token expiration in days
- `CELERY_BROKER_URL`: Message broker URL (RabbitMQ/Redis)
- `CELERY_BACKEND_URL`: Result backend URL (Redis)
- `REDIS_*`: Redis connection settings
- `DATABASE_URL`: Database connection string
- `ALLOWED_ORIGINS`: CORS allowed origins (JSON array)

### Configuration Files

- `configs/config.py`: App configurations
- `configs/celery_config.py`: Celery broker/backend settings
- `celery_worker/celery_setup.py`: Celery application setup

## Development

### Linting and Formatting

```bash
# Run linter
uv run ruff check .

# Auto-fix linting issues
uv run ruff check . --fix

# Format code
uv run format
```

### Testing

```bash
# Run tests
python -m pytest tests/

# Run Redis connection test
python tests/redis_test.py
```

### Adding New Features

1. **Add API Endpoints**: Create new files in `app/api/`
2. **Add Business Logic**: Add services in `app/services/`
3. **Add Models**: Define SQLAlchemy models in `app/models/`
4. **Add Celery Tasks**: Define tasks in `app/services/` with `@celery_app.task` decorator

## Deployment

### Using Gunicorn

For production deployment:

```bash
# Install with production dependencies
pip install -e .[production]

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 --access-logfile - wsgi:ai_server
```

### Docker Deployment

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:ai_server"]
```

### Supervisor Setup

For production Celery worker management, see `docs/supervisor.MD`.

## Contributing

1. Follow the existing code structure
2. Add comprehensive tests for new features
3. Update this README for any configuration changes
4. Ensure all code passes linting

## License

