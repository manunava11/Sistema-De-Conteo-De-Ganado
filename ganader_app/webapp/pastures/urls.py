from django.urls import path
from . import views

urlpatterns = [
    path('', views.pasture_list, name='pasture-list'),
    path('add/', views.add_pasture, name='add-pasture'),
]
