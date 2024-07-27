from django.db import models
from pastures.models import Pasture
from lots.models import Lot
from django.utils import timezone


class CowCount(models.Model):
    lot = models.ForeignKey(Lot, related_name='count_history', on_delete=models.CASCADE)
    pasture = models.ForeignKey(Pasture, null=True, blank=True, on_delete=models.CASCADE)
    cow_count = models.IntegerField()
    method = models.CharField(max_length=10, choices=[('manual', 'Manual'), ('video', 'Video')], default='manual')
    date = models.DateField(default=timezone.now)
    comment = models.TextField(max_length=250)

    def __str__(self):
        return f'{self.lot.name} - {self.cow_count} cows'

class UploadedVideo(models.Model):
    uploaded_video = models.FileField(upload_to='uploaded_videos/')
    processed_video = models.FileField(upload_to='processed_videos/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    cow_count = models.OneToOneField('CowCount', on_delete=models.CASCADE, related_name='video', null=True, blank=True)

    def __str__(self):
        return f"Video {self.id} - Uploaded at {self.uploaded_at}"
    