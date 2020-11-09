from django.contrib import admin

# Register your models here.
from app.models import OfferCategory

class OfferCategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(OfferCategory, OfferCategoryAdmin)