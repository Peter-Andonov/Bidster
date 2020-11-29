from django.urls import path
from bidster_auth.views import RegisterUserView, LoginUserView, logout_user, ProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register user'),
    path('login/', LoginUserView.as_view(), name='login user'),
    path('logout/', logout_user, name='logout user'),
    path('profile/', ProfileView.as_view(), name='user profile'),
]