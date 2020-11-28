from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import IndexView, create_page, MyOffersView, details_page

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-offer/', create_page, name='create page'),
    path('my-offers/', MyOffersView.as_view(), name='my offers page'),
    path('offer-details/<int:offer_id>/', details_page, name='details page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)