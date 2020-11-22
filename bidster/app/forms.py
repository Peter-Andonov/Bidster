from django import forms
from django.core.exceptions import ValidationError

from app.models import Offer, OfferCategory, Bid


class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.offer_id = kwargs.pop('offer_id', None)
        super(BidForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' details__bid_form_input '

    def clean_amount(self):
        offer = Offer.objects.get(pk=self.offer_id)
        offer_amount = self.cleaned_data.get('amount')
        if offer_amount < offer.starting_price:
            raise ValidationError("Bid amount cannot be less than starting price")
        return offer_amount

    class Meta:
        fields = ('message', 'amount')
        model = Bid
        widgets = {
            'message': forms.Textarea(),
        }


class OfferForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form__input '

    name = forms.CharField(label='Name', required=True, max_length=200)
    images = forms.ImageField(
        label='Upload images',
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'accept': 'image/*',
                'multiple': True,
                'style': 'display:none',
            })
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea()
    )
    condition = forms.CharField(
        label='Condition',
        widget=forms.Select(choices=Offer.CONDITION_TYPE_CHOICES)
    )
    starting_price = forms.DecimalField(max_digits=19, decimal_places=2)
    category = forms.ModelChoiceField(
        label='Category', required=True, queryset=OfferCategory.objects.all())
    location = forms.CharField(max_length=50)
    active_for = forms.IntegerField(
        label='Active for', required=True, min_value=1, max_value=14)
