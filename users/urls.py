from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('profile', views.profile, name='profile'),
]