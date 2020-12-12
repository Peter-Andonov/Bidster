from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from bidster_auth.models import Profile
from common.form_mixins import DefaultFormMixin


class RegistrationForm(DefaultFormMixin, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()


class LoginForm(DefaultFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()


class UserForm(DefaultFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(DefaultFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_fields__()

    class Meta():
        model = Profile
        fields = ('profile_pic', 'phone_number', 'location')
        widgets = {
            'profile_pic': forms.FileInput(
                attrs={
                    'accept': 'image/*',
                    'class': 'form__image_input',
                    'style': 'display:none',
                })
        }
