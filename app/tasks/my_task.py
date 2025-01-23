from celery import shared_task

@shared_task(name="my_test_task")
def my_task():
    print("My task is running, pundra")