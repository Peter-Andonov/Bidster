from django.urls import path
from app.views import index_page

urlpatterns = [
    path('', index_page, name='index'),
]