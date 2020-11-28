from datetime import timedelta

from django.db import transaction
from django.db.models import Prefetch
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

from app.forms import OfferForm, BidForm
from app.models import ImageGalery, Offer, OfferCategory, Image, Bid
from app.utils.db_requests import get_offers, get_offer_by_id, get_offer_bids
from app.utils.file_upload import save_to_galery


class IndexView(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offers_count'] = Offer.objects.count()
        context['categories'] = OfferCategory.objects.all()
        context['last_five_offers'] = get_offers(limit=5)
        return context


@method_decorator(transaction.atomic, name='post')
class CreateOfferView(LoginRequiredMixin, FormView):
    form_class = OfferForm
    template_name = 'app/create_offer.html'

    def get_context_data(self, **kwargs):
        context = super(CreateOfferView, self).get_context_data(**kwargs)
        context["offer_form"] = context["form"]
        return context

    def post(self, req, *args, **kwargs):
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

    offer = get_offer_by_id(offer_id=offer_id)
    offer_bids = get_offer_bids(offer_id=offer_id)
    highest_bid = offer_bids[0].amount if offer_bids else None
    user_is_creator = req.user.id == offer.created_by.id

    if req.method == "GET":
        offer.view_counts += 1
        offer.save()

        context = {
            'user_is_creator': user_is_creator,
            'offer': offer,
            'offer_bids': offer_bids,
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
                'user_is_creator': user_is_creator,
                'offer': offer,
                'offer_bids': offer_bids,
                'highest_bid': highest_bid,
                'bid_form': bid_form,
            }

            return render(req, 'app/offer_details.html', context)


class MyOffersView(LoginRequiredMixin, ListView):
    context_object_name = 'my_offers'
    template_name = 'app/my_offers.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        req = self.request
        self.offers = get_offers(created_by=req.user.id)
        return self.offers

    def get_context_data(self, *args, **kwargs):
        context = super(MyOffersView, self).get_context_data(*args, **kwargs)
        context['my_offers'] = self.offers
        return context
