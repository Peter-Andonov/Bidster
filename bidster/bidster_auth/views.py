from django.db import transaction
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from app.utils.db_requests import get_user_data
from bidster_auth.models import Profile
from bidster_auth.forms import LoginForm, RegistrationForm, UserForm, ProfileForm


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

        return render(req, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["register_form"] = context["form"]
        return context


class LoginUserView(FormView):
    form_class = LoginForm
    template_name = 'bidster_auth/login.html'

    def post(self, req, *args, **kwargs):
        login_form = LoginForm(req, req.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=email, password=password)
            if user:
                login(req, user)
                return redirect('index')
        else:
            login_form.errors['invalid_credentials'] = [
                "Invalid username or password"]

        context = {
            'login_form': login_form,
        }

        return render(req, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = context["form"]
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'bidster_auth/profile.html'

    def post(self, req, *args, **kwargs):
        user_data = get_user_data(self.request.user.id)
        user_form = UserForm(req.POST, instance=user_data)
        profile_form = ProfileForm(
            req.POST, req.FILES, instance=user_data.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('user profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
            }

            return render(req, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = get_user_data(self.request.user.id)
        current_pic_url = user_data.profile.profile_pic.url if user_data.profile.profile_pic else None

        context["user_form"] = UserForm(initial={
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'email': user_data.email,
        })
        context["profile_form"] = ProfileForm(initial={
            'profile_pic': user_data.profile.profile_pic,
            'phone_number': user_data.profile.phone_number,
            'location': user_data.profile.location,
        })
        context["current_pic_url"] = current_pic_url
        return context
