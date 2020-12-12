from django.contrib import admin

from app.models import OfferCategory, Offer, ImageGalery, Image, Bid


class ImageInline(admin.TabularInline):
    model = Image


class OfferCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_by',
                    'published_on', 'expires_on')


class ImageGaleryAdmin(admin.ModelAdmin):
    list_display = ('id',)
    inlines = [ImageInline]


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'galery', 'image')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'for_offer', 'created_by', 'created_on')


admin.site.register(OfferCategory, OfferCategoryAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(ImageGalery, ImageGaleryAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Bid, BidAdmin)
