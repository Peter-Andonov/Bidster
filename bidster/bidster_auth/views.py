from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login, logout

from bidster_auth.models import Profile
from bidster_auth.forms import LoginForm, RegistrationForm


def login_user(req):
    if req.method == 'GET':
        context = {
            'login_form': LoginForm(),
        }

        return render(req, 'bidster_auth/login.html', context)

    if req.method == 'POST':
        login_form = LoginForm(req.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                login(req, user)
                return redirect('index')
            else:
                login_form.errors['invalid_credentials'] = [
                    "Invalid email or password"]

        context = {
            'login_form': login_form,
        }

        return render(req, 'bidster_auth/login.html', context)


def logout_user(req):
    logout(req)

    return redirect('index')


@method_decorator(transaction.atomic, name='post')
class RegisterUserView(CreateView):
    form_class = RegistrationForm
    template_name = 'bidster_auth/register.html'

    def post(self, req, *args, **kwargs):
        register_form = RegistrationForm(req.POST)
        if register_form.is_valid():
            new_user = User.objects.create_user(
                username=register_form.cleaned_data['username'],
                password=register_form.cleaned_data['password1'],
            )

            new_profile = Profile()
            new_profile.user = new_user
            new_profile.save()

            login(req, new_user)

            return redirect('index')

        context = {
            'register_form': register_form
        }

        return render(req, 'bidster_auth/register.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_form"] = context["form"]
        return context
