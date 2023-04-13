from django.urls import path, include
from . import views
urlpatterns = [
    path('computations', views.computations, name='computations'),
    path('computations/<str:username>/<int:computation_id>/', views.computation_results, name='computation_results'),
    path('computations/<str:username>/<int:computation_id>/dump_json', views.dump_json, name='dump_json'),
    path('computations/<str:username>/<int:computation_id>/dump_pdf', views.dump_pdf, name='dump_pdf'),
]

