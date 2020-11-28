from django.urls import path
from bidster_auth.views import RegisterUserView, login_user, logout_user

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('login/', login_user, name='login user'),
    path('logout/', logout_user, name='logout user'),
]