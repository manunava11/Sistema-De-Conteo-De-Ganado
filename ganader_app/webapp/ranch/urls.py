from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_ranch, name='create-ranch'),
    path('<int:ranch_id>/', views.ranch_detail, name='ranch-detail'),
    path('<int:ranch_id>/add-member', views.add_member, name='add-member'),
]