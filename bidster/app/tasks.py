from celery import shared_task

@shared_task
def expire_offer(x, y):
    return x + y