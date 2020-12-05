from django import forms
from django.core.exceptions import ValidationError

from app.models import Offer, OfferCategory, Bid


class SearchForm(forms.Form):
    text = forms.CharField(
        label='Text',
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'search__input',
            'placeholder': "Search in all offers"
        })
    )
    condition = forms.CharField(
        label='Condition',
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'search__filter_input',
            },
            choices=(("", "---------"), *Offer.CONDITION_TYPE_CHOICES),
        )
    )
    category = forms.ModelChoiceField(
        label='Category',
        required=False,
        queryset=OfferCategory.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'search__filter_input',
            }
        )
    )
    price_from = forms.DecimalField(
        max_digits=19,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'search__filter_input',
        })
    )
    price_to = forms.DecimalField(
        max_digits=19,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'search__filter_input',
        })
    )

    def clean_price_to(self):
        price_from = self.cleaned_data.get("price_from")
        price_to = self.cleaned_data.get("price_to")
        if price_from and price_to and price_from > price_to:
            raise ValidationError(
                "Price upper limit cannot be below lower limit")
        return price_to


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

        if not offer:
            raise ValidationError('Offer not found')
        
        if offer_amount <= offer.current_price:
            raise ValidationError('Bid amount must be greater than the current price')
        
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
                'class': 'form__image_input',
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
    contact_person = forms.CharField(max_length=50)
    contact_email = forms.EmailField(required=False)
    contact_phone = forms.CharField(max_length=50)
    location = forms.CharField(max_length=50)
    active_for = forms.IntegerField(
        label='Active for', required=True, min_value=1, max_value=14)
