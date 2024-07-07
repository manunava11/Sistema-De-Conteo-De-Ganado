from django.urls import path
from. import views

urlpatterns = [
    path('', views.lot_list, name='lot-list'),
    path('add/', views.add_lot, name='add-lot'),
]