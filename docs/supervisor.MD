# Demo Supervisor Configuration (Ready to Use)

```ini
# /etc/supervisor/conf.d/ai_server_template_demo.conf
# ——————————————————————————————————————————————————
# Demo instance of ai_server_template
# • Runs on port 8001 (change if you need more instances)
# • Completely isolated from production
# • Simple log structure

[program:ai_server_template]
command=/home/abrar/projects/ai_server_template/.venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 server:entry   # Change the path to .venv
directory=/home/abrar/projects/ai_server_template # Change directory
user=abrar # Change user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/abrar/projects/ai_server_template/var/log/supervisor/ai_server_template/gunicorn.log # Change to your need
stderr_logfile=/home/abrar/projects/ai_server_template/var/log/supervisor/ai_server_template/gunicorn.err.log # Change to your need
environment=PATH="/home/abrar/projects/ai_server_template/.venv/bin",USER="abrar" # Change to path and user

[program:celery]
command=/home/abrar/projects/ai_server_template/.venv/bin/celery -A celery_worker. # Change the path to .venvcelery_setup.celery_app worker --loglevel=info --concurrency=4
directory=/home/abrar/projects/ai_server_template # Change directory
user=abrar # Change user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/abrar/projects/ai_server_template/var/log/supervisor/ai_server_template/celery.log # Change to your need
stderr_logfile=/home/abrar/projects/ai_server_template/var/log/supervisor/ai_server_template/celery.err.log # Change to your need
environment=PATH="/home/abrar/projects/ai_server_template/.venv/bin",USER="abrar" # Change to path and user