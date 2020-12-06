from celery import shared_task
from app.utils.db_requests import get_offer_by_id

@shared_task
def expire_offer(offer_id):
    offer = get_offer_by_id(offer_id)
    offer.is_active = False
    offer.save()
    return offer.id
