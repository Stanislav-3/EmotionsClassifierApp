from django.urls import path, include
from . import views

urlpatterns = [
    path('computations', views.computations, name='computations'),
    path('computations/<str:username>/<int:computation_id>/', views.result, name='result'),
]