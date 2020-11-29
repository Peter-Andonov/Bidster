from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form__input '


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form__input '


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form__input '

    profile_pic = forms.ImageField(
        label='Upload images',
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                'accept': 'image/*',
                'class': 'form__image_input',
                'style': 'display:none',
            })
    )
    first_name = forms.CharField(
        required=False,
        max_length=50
    )
    last_name = forms.CharField(
        required=False,
        max_length=50
    )
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(
        required=False,
        max_length=50
    )
    location = forms.CharField(
        required=False,
        max_length=200
    )
