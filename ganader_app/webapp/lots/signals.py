from django.db.models.signals import post_save
from django.dispatch import receiver
from cattle_countings.models import UploadedVideo
from cattle_countings.tasks import process_video

@receiver(post_save, sender=UploadedVideo)
def video_uploaded(sender, instance, created, **kwargs):
    if created and instance.processed_at is None:  # Only trigger if the video is newly created and not processed
        result = process_video.delay(instance.id, instance.cow_count.id)
        instance.task_id = result.task_id
        instance.save()