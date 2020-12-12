from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import IndexView, BrowseView, SearchResultsView, CreateOfferView, OfferDetailsView, MyOffersView, MyBidsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('browse-offers/', BrowseView.as_view(), name='browse page'),
    path('search-results/', SearchResultsView.as_view(), name='search results'),
    path('create-offer/', CreateOfferView.as_view(), name='create page'),
    path('offer-details/<int:offer_id>/<slug:slug>/', OfferDetailsView.as_view(), name='details page'),
    path('my-offers/', MyOffersView.as_view(), name='my offers page'),
    path('my-bids/', MyBidsView.as_view(), name='my bids page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)