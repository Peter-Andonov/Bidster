from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import index_page, create_page

urlpatterns = [
    path('', index_page, name='index'),
    path('create-offer/', create_page, name='create page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)