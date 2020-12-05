from celery import shared_task
from time import sleep


@shared_task(bind=True)
def expire_offer(self, duration):
    sleep(duration)
    return "Done"