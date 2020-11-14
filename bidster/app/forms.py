from django import forms

from app.models import Offer, OfferCategory


class OfferForm(forms.Form):
    name = forms.CharField(label='name', required=True, max_length=200)
    images = forms.ImageField(label='upload images', required=False,
                              widget=forms.ClearableFileInput(attrs={'accept': 'image/*',
                                                                     'multiple': True}))
    description = forms.CharField(
        label='offer description', widget=forms.Textarea)
    condition = forms.CharField(
        label='select condition',
        widget=forms.Select(choices=Offer.CONDITION_TYPE_CHOICES)
    )
    starting_price = forms.DecimalField(max_digits=19, decimal_places=2)
    category = forms.ModelChoiceField(
        label='category', required=True, queryset=OfferCategory.objects.all())
    location = forms.CharField(max_length=50)
    active_for = forms.IntegerField(
        label='active for', required=True, min_value=1, max_value=14)
