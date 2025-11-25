# Run Redis
```docker run redis```
- Permission for a redis user should be in the following format to work with redis
```
ACL SETUSER demo-user on >your_password +@all &* -@dangerous ~your_key_prefix:
```

# Run Rabbit MQ
```docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management ```                                

# Run Celery Worker
```celery -A celery_worker.celery_setup.celery_app worker --loglevel=info --hostname=worker1@%h --pool=solo```               

- --pool = solo is windows dependency

# Show worker status using flower (localhost:5555) or use host address
```celery -A celery_worker.celery_setup.celery_app flower --port=5555 ```