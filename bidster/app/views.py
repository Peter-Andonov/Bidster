from datetime import timedelta

from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from app.forms import OfferForm, BidForm
from app.models import ImageGalery, Offer, OfferCategory, Image, Bid
from app.utils.file_upload import save_to_galery

# Create your views here.


def index_page(req):
    if req.method == 'GET':
        context = {
            'offers_count': Offer.objects.count(),
            'categories': OfferCategory.objects.all(),
            'last_five_offers': Offer.objects.all()
            .prefetch_related(Prefetch(
                'imagegalery__image_set',
                queryset=Image.objects.all(), to_attr='images'
            ))
            .prefetch_related(Prefetch(
                'bid_set',
                queryset=Bid.objects.all().order_by('-amount'), to_attr='bids'
            )),
        }
        return render(req, 'app/index.html', context)


@login_required
def create_page(req):
    if req.method == 'GET':

        context = {
            'offer_form': OfferForm()
        }

        return render(req, 'app/create_offer.html', context)

    if req.method == 'POST':

        offer_form = OfferForm(req.POST, req.FILES)

        if offer_form.is_valid():
            offer = Offer(
                name=offer_form.cleaned_data['name'],
                description=offer_form.cleaned_data['description'],
                condition=offer_form.cleaned_data['condition'],
                starting_price=offer_form.cleaned_data['starting_price'],
                category=offer_form.cleaned_data['category'],
                location=offer_form.cleaned_data['location'],
                created_by=req.user,
                expires_on=now() +
                timedelta(days=offer_form.cleaned_data['active_for'])
            )
            offer.save()

            image_gallery = ImageGalery(offer=offer)
            image_gallery.save()

            for f in req.FILES.getlist('images'):
                save_to_galery(image_gallery, f)

            return redirect('index')


def details_page(req, offer_id):
    offer = Offer.objects.prefetch_related(Prefetch(
        'imagegalery__image_set', queryset=Image.objects.all(), to_attr='images')).get(pk=offer_id)
    offer_bids = Bid.objects.filter(offer=offer_id).order_by('-amount')
    highest_bid = offer_bids[0].amount if offer_bids else None
    if req.method == "GET":
        offer.view_counts += 1
        offer.save()

        context = {
            'offer': offer,
            'highest_bid': highest_bid,
            'bid_form': BidForm(offer_id=offer_id),
        }

        return render(req, 'app/offer_details.html', context)

    if req.method == "POST":
        bid_form = BidForm(req.POST, offer_id=offer_id)
        if bid_form.is_valid():
            amount = bid_form.cleaned_data.get('amount')
            message = bid_form.cleaned_data.get('message')
            bid = Bid(amount=amount, message=message,
                      offer=offer, created_by=req.user)
            bid.save()
            return redirect("index")
        else:
            context = {
                'offer': offer,
                'highest_bid': highest_bid,
                'bid_form': bid_form,
            }

            return render(req, 'app/offer_details.html', context)


@login_required
def my_offers_page(req):
    if req.method == 'GET':
        my_offers = Offer.objects.filter(created_by=req.user.id).prefetch_related(Prefetch('imagegalery__image_set', queryset=Image.objects.all(
        ), to_attr='images')).prefetch_related(Prefetch('bid_set', queryset=Bid.objects.all().order_by('-amount'), to_attr='bids'))
        context = {
            'my_offers': my_offers,
        }
        return render(req, 'app/my_offers.html', context)
