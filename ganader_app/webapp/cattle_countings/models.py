from django.db import models
from lots.models import Lot
from pastures.models import Pasture

class CountHistory(models.Model):
    COUNT_METHODS = [
        ('manual', 'Manual'),
        ('video', 'Video'),
    ]

    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='count_history')
    pasture = models.ForeignKey(Pasture, on_delete=models.CASCADE, null=True, blank=True)
    cow_count = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10, choices=COUNT_METHODS, default='manual')

class VideoUpload(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='video_uploads')
    video = models.FileField(upload_to='videos/')
    processed = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)