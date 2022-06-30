from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView
from .views import CustomPasswordChangeView, CustomPasswordResetConfirmView

urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),

    path('sign-up', views.sign_up, name='sign_up'),
    path('password_change/',
         CustomPasswordChangeView.as_view(template_name="registration/password_change.html"),
         name='password_change'),
    path('password_reset/',
         PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name='password_reset'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='registration/password_reset_done2.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm2.html"),
         name='password_reset_confirm'),
]