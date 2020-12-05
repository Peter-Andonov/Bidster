from django.db.models import Prefetch, Q
from django.contrib.auth.models import User

from app.models import Offer, Image, Bid
from bidster_auth.models import Profile


def get_offer_by_id(offer_id):
    offer = Offer.objects\
        .prefetch_related(
            Prefetch(
                'imagegalery__image_set',
                queryset=Image.objects.all(), to_attr='images'
            ))\
        .get(pk=offer_id)

    return offer


def get_user_data(user_id):
    user_data = User.objects\
    .prefetch_related('profile')\
    .get(pk=user_id)

    return user_data


def get_offer_bids(offer_id):
    offer_bids = Bid.objects.filter(for_offer=offer_id)\
        .prefetch_related('created_by')\
        .order_by('-amount')

    return offer_bids


def get_bids_by_user_id(user_id):
    user_bids = Bid.objects.filter(created_by=user_id)\
        .prefetch_related('for_offer')\
        .order_by('-amount')

    return user_bids


def get_offers(text='', category_id=None, created_by=None, condition=None, price_from=None, price_to=None, limit=None):
    q = Q()

    if text:
        q = q & Q(name__icontains=text)

    if category_id:
        q = q & Q(category_id=category_id)

    if condition:
        q = q & Q(condition=condition)

    if price_from:
        q = q & Q(current_price__gte=price_from)

    if price_to:
        q = q & Q(current_price__lte=price_to)

    if created_by:
        q = q & Q(created_by=created_by)

    offers = Offer.objects.filter(q)\
        .order_by('-id')\
        .prefetch_related(
        Prefetch(
            'imagegalery__image_set',
            queryset=Image.objects.all(), to_attr='images'
        ))[:limit]

    return offers
