from django.urls import path
from . import views

urlpatterns = [
    path('upload/<int:lot_id>/', views.video_upload, name='video-upload'),
    path('manual/<int:lot_id>/', views.manual_count, name='manual-count'),
]