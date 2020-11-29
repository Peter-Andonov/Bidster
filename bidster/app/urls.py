from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import IndexView, CreateOfferView, MyOffersView, OfferDetailsView, SearchResultsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-offer/', CreateOfferView.as_view(), name='create page'),
    path('my-offers/', MyOffersView.as_view(), name='my offers page'),
    path('offer-details/<int:offer_id>/', OfferDetailsView.as_view(), name='details page'),
    path('search-results/', SearchResultsView.as_view(), name='search results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)