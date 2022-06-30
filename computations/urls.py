from django.urls import path, include
from . import views

urlpatterns = [
    path('computations', views.computations, name='computations'),
]