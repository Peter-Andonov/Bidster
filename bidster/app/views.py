from datetime import timedelta

from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from app.forms import OfferForm
from app.models import ImageGalery, Offer, OfferCategory, Image
from app.utils.file_upload import save_to_galery

# Create your views here.


def index_page(req):
    if req.method == 'GET':
        context = {
            'offers_count': Offer.objects.count(),
            'categories': OfferCategory.objects.all(),
            'last_five_offers': Offer.objects.all().prefetch_related(Prefetch('imagegalery__image_set', queryset=Image.objects.all(), to_attr='images')),
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


@login_required
def my_offers_page(req):
    if req.method == 'GET':
        context = {
            'my_offers': Offer.objects.filter(created_by=req.user.id).prefetch_related(Prefetch('imagegalery__image_set', queryset=Image.objects.all(), to_attr='images')),
        }
        return render(req, 'app/my_offers.html', context)
