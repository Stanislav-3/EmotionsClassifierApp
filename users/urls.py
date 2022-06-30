from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from .views import CustomPasswordChangeView

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('profile', views.profile, name='profile'),
    path('password_change/',
         CustomPasswordChangeView.as_view(template_name="registration/change_password.html"),
         name='password_change'),
]