from django.db import models
from pastures.models import Pasture
from lots.models import Lot
from django.utils import timezone


class CowCount(models.Model):
    lot = models.ForeignKey(Lot, related_name='count_history', on_delete=models.CASCADE)
    pasture = models.ForeignKey(Pasture, null=True, blank=True, on_delete=models.CASCADE)
    cow_count = models.IntegerField()
    method = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.lot.name} - {self.cow_count} cows'

#class VideoUpload(models.Model):
#    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='video_uploads')
#    video = models.FileField(upload_to='videos/')
#    processed = models.BooleanField(default=False)
#    date_uploaded = models.DateTimeField(auto_now_add=True)