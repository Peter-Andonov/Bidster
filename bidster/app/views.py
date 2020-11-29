from datetime import timedelta

from django.db import transaction
from django.db.models import Prefetch
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

from app.forms import SearchForm, OfferForm, BidForm
from app.models import ImageGalery, Offer, OfferCategory, Image, Bid
from app.utils.db_requests import get_offers, get_offer_by_id, get_offer_bids, get_bids_by_user_id
from app.utils.file_upload import save_to_galery


class IndexView(FormView):
    form_class = SearchForm
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = OfferCategory.objects.all()
        context['last_five_offers'] = get_offers(limit=5)
        return context


class SearchResultsView(ListView):
    template_name = 'app/search_results.html'

    def get(self, *args, **kwargs):
        search_form = SearchForm(self.request.GET)
        if search_form.is_valid():
            category_id = search_form.cleaned_data['category'].id if search_form.cleaned_data['category'] else None
            offers = get_offers(
                text=search_form.cleaned_data['text'],
                category_id=category_id,
                condition=search_form.cleaned_data['condition'],
                price_from=search_form.cleaned_data['price_from'],
                price_to=search_form.cleaned_data['price_to'],
            )

            context = {
                'search_form': SearchForm(),
                'offers': offers,
            }

            return render(self.request, self.template_name, context)
        else:
            context = {
                'search_form': search_form,
            }

            return render(self.request, self.template_name, context)


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
                current_price=offer_form.cleaned_data['starting_price'],
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
        else:
            return super().form_invalid(offer_form)


@method_decorator(login_required, name='post')
@method_decorator(transaction.atomic, name='post')
class OfferDetailsView(FormView):
    form_class = BidForm
    template_name = 'app/offer_details.html'
    success_url = reverse_lazy('index')

    def post(self, req, *args, **kwargs):
        offer_id = self.kwargs['offer_id']
        offer = Offer.objects.get(pk=offer_id)
        bid_form = BidForm(req.POST, offer_id=offer_id)
        if bid_form.is_valid():
            amount = bid_form.cleaned_data.get('amount')
            message = bid_form.cleaned_data.get('message')
            bid = Bid(amount=amount, message=message,
                      for_offer=offer, created_by=req.user)
            bid.save()
            offer.current_price = amount
            offer.save()
            return redirect("index")
        else:
            return super().form_invalid(bid_form)

    def get_context_data(self, **kwargs):
        context = super(OfferDetailsView, self).get_context_data(**kwargs)
        offer_id = self.kwargs['offer_id']
        offer = get_offer_by_id(offer_id=offer_id)
        offer_bids = None
        user_is_creator = self.request.user.id == offer.created_by.id

        if user_is_creator:
            offer_bids = get_offer_bids(offer_id=offer_id)
        
        offer.view_counts += 1
        offer.save()

        context["user_is_creator"] = user_is_creator
        context["offer"] = offer
        context["offer_bids"] = offer_bids
        context["bid_form"] = context["form"]
        return context


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


class MyBidsView(LoginRequiredMixin, ListView):
    context_object_name = 'my_bids'
    template_name = 'app/my_bids.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        req = self.request
        self.bids = get_bids_by_user_id(user_id=req.user.id)
        return self.bids

    def get_context_data(self, *args, **kwargs):
        context = super(MyBidsView, self).get_context_data(*args, **kwargs)
        context['my_bids'] = self.bids
        return context