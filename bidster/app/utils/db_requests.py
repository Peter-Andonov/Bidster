from django.db.models import Prefetch, Q

from app.models import Offer, Image, Bid


def get_offers(text='', category_id=None, created_by=None, condition=None, limit=None):
    q = Q()

    if text:
        q = q & Q(name__icontains=text)

    if category_id:
        q = q & Q(category_id=category_id)

    if condition:
        q = q & Q(condition=condition)

    if created_by:
        q = q & Q(created_by=created_by)

    offers = Offer.objects.filter(q)\
        .order_by('-id')\
        .prefetch_related(
        Prefetch(
            'imagegalery__image_set',
            queryset=Image.objects.all(), to_attr='images'
        ))\
        .prefetch_related(
        Prefetch(
            'bid_set',
            queryset=Bid.objects.all().order_by('-amount'), to_attr='bids'
        ))[:limit]

    return offers
