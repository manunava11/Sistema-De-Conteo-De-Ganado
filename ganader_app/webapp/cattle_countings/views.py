from django.shortcuts import render, get_object_or_404, redirect
from .models import VideoUpload, CountHistory
from .forms import VideoUploadForm, ManualCountForm
from lots.models import Lot
import cv2  # Assuming you are using OpenCV for processing

def video_upload(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_upload = form.save(commit=False)
            video_upload.lot = lot
            video_upload.save()
            # Process the video file here
            cow_count = process_video(video_upload)
            lot.cow_count = cow_count
            lot.save()
            return redirect('lot-detail', ranch_id=lot.ranch.id, lot_id=lot.id)
    else:
        form = VideoUploadForm()
    return render(request, 'counts/video_upload.html', {'form': form, 'lot': lot})

def manual_count(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    if request.method == 'POST':
        form = ManualCountForm(request.POST)
        if form.is_valid():
            manual_count = form.save(commit=False)
            manual_count.method = 'manual'
            manual_count.lot = lot
            manual_count.pasture = lot.pasture
            manual_count.save()
            lot.cow_count = manual_count.cow_count
            lot.save()
            return redirect('lot-detail', ranch_id=lot.ranch.id, lot_id=lot.id)
    else:
        form = ManualCountForm(initial={'lot': lot})
    return render(request, 'counts/manual_count.html', {'form': form, 'lot': lot})

def process_video(video_upload):
    video_path = video_upload.video.path
    # Implement your video processing logic here to count cows
    cow_count = 0  # Replace this with the actual cow counting logic

    lot = video_upload.lot
    pasture = lot.pasture

    CountHistory.objects.create(
        lot=lot,
        pasture=pasture,
        cow_count=cow_count,
        method='video'
    )

    # Update lot's cow count
    lot.cow_count = cow_count
    lot.save()

    video_upload.processed = True
    video_upload.save()