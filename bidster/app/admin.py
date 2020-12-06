from django.contrib import admin

from app.models import OfferCategory, Offer, ImageGalery, Bid


class OfferCategoryAdmin(admin.ModelAdmin):
    pass


class OfferAdmin(admin.ModelAdmin):
    list_display  = ('name', 'is_active', 'created_by', 'published_on', 'expires_on')


class ImageGaleryAdmin(admin.ModelAdmin):
    pass


class BidAdmin(admin.ModelAdmin):
    pass


admin.site.register(OfferCategory, OfferCategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(ImageGalery, ImageGaleryAdmin)
admin.site.register(Bid, BidAdmin)
