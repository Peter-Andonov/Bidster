from django.contrib import admin

# Register your models here.
from app.models import OfferCategory, Offer, ImageGalery

class OfferCategoryAdmin(admin.ModelAdmin):
    pass

class OfferAdmin(admin.ModelAdmin):
    pass

class ImageGaleryAdmin(admin.ModelAdmin):
    pass

admin.site.register(OfferCategory, OfferCategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(ImageGalery, ImageGaleryAdmin)