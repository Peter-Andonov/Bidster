from django import forms
from app.models import Offer, Image, OfferCategory


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ('image_gallery', 'published_on', 'view_counts')
        widgets = {
            'expires_in': forms.SelectDateWidget()
        }




class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('galery_id', )
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True})
        }
