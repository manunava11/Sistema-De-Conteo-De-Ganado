from django.urls import path
from. import views

urlpatterns = [
    path('', views.lot_list, name='lot-list'),
    path('add/', views.add_lot, name='add-lot'),
    path('<int:lot_id>/', views.lot_detail, name='lot-detail'),
    path('<int:lot_id>/edit-delete/', views.edit_delete_lot, name='edit-delete-lot'),
    path('<int:lot_id>/update-count/', views.lot_detail, name='update-count'),
]