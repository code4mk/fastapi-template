To run the Celery worker and beat, you'll need to use the `celery` command-line interface. Here are the commands:

1. To run a Celery worker:
```bash
celery -A app.celery:app worker --loglevel=INFO
```

2. To run Celery beat (scheduler):
```bash
celery -A app.celery:app beat --loglevel=INFO
```

You can also run both worker and beat in a single command:
```bash
celery -A app.celery:app worker --beat --loglevel=INFO
```

Explanation of the commands:
- `-A app.celery:app`: Specifies the Celery application instance (the path to your app)
- `worker`: Starts a worker process
- `beat`: Starts the scheduler
- `--loglevel=INFO`: Sets the logging level (you can use DEBUG for more detailed logs)

Additional tips:
1. Make sure Redis is running (since you're using it as a broker)
2. You might want to run these commands from the root directory of your project
3. In development, you can add `-P solo` on Windows or if you encounter multiprocessing issues:
```bash
celery -A app.celery:app worker -P solo --loglevel=INFO
```

Would you like me to explain any specific part in more detail?