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
            process_video(video_upload)
            return redirect('lot-detail', lot_id=lot.id)
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
            manual_count.save()
            return redirect('lot-detail', lot_id=lot.id)
    else:
        form = ManualCountForm(initial={'lot': lot})
    return render(request, 'counts/manual_count.html', {'form': form, 'lot': lot})

def process_video(video_upload):
    # Implement your video processing logic here
    # Example: Use OpenCV to count cows in the video
    video_path = video_upload.video.path
    cap = cv2.VideoCapture(video_path)
    cow_count = 0
    # Your processing logic to count cows

    # Assuming you have the cow_count after processing
    lot = video_upload.lot
    pasture = lot.pasture

    CountHistory.objects.create(
        lot=lot,
        pasture=pasture,
        cow_count=cow_count,
        method='video'
    )

    video_upload.processed = True
    video_upload.save()