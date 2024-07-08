from django.shortcuts import render, get_object_or_404, redirect
from .models import Lot, Ranch
from .forms import LotForm
from cattle_countings.forms import ManualCountForm, VideoUploadForm
from cattle_countings.models import CountHistory, VideoUpload
from datetime import datetime
#import cv2  # Uncomment this if you need to use OpenCV

def lot_list(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    lots = Lot.objects.filter(ranch_id=ranch_id)
    return render(request, 'lots/lots_list.html', {'lots': lots, 'ranch': ranch})

def add_lot(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    if request.method == 'POST':
        form = LotForm(request.POST)
        if form.is_valid():
            lot = form.save(commit=False)
            lot.ranch = ranch
            lot.save()
            return redirect('lot-list', ranch_id=ranch.id)
    else:
        form = LotForm()
    return render(request, 'lots/add_lot.html', {'form': form, 'ranch': ranch})

def lot_detail(request, ranch_id, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    ranch = get_object_or_404(Ranch, id=ranch_id)

    count_history = lot.count_history.all()

    manual_count_form = ManualCountForm(initial={'date': datetime.now()})
    video_upload_form = VideoUploadForm()

    if request.method == 'POST':
        if 'manual_count' in request.POST:
            manual_count_form = ManualCountForm(request.POST)
            if manual_count_form.is_valid():
                count = manual_count_form.save(commit=False)
                count.lot = lot
                count.pasture = lot.pasture
                count.method = 'manual'
                count.save()
                
                # Save count to history
                CountHistory.objects.create(
                    lot=lot,
                    pasture=lot.pasture,
                    cow_count=count.count,  # Assuming count field name
                    method='manual',
                    count_date=datetime.now(),  # Adjust this as needed
                )

                return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot.id)
        elif 'upload_video' in request.POST:
            video_upload_form = VideoUploadForm(request.POST, request.FILES)
            if video_upload_form.is_valid():
                video_upload = video_upload_form.save(commit=False)
                video_upload.lot = lot
                video_upload.save()
                process_video(video_upload)  # Ensure this processes and sets processed=True
                
                # Retrieve cow count from video processing
                cow_count = ...  # Implement your logic to get cow count from video processing

                # Save count to history
                CountHistory.objects.create(
                    lot=lot,
                    pasture=lot.pasture,
                    cow_count=cow_count,
                    method='video',
                    count_date=datetime.now(),  # Adjust this as needed
                )

                return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot.id)

    lot_form = LotForm(instance=lot)

    context = {
        'lot': lot,
        'count_history': count_history,
        'manual_count_form': manual_count_form,
        'video_upload_form': video_upload_form,
        'form': lot_form,
        'ranch': ranch,
    }

    return render(request, 'lots/lot_detail.html', context)

def edit_delete_lot(request, ranch_id, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    ranch = get_object_or_404(Ranch, id=ranch_id)

    if request.method == 'POST':
        if request.POST.get('delete') == 'true':
            lot.delete()
            return redirect('lot-list', ranch.id)
        else:
            form = LotForm(request.POST, instance=lot)
            if form.is_valid():
                form.save()
                return redirect('lot-detail', ranch.id, lot.id)
    else:
        form = LotForm(instance=lot)

    context = {
        'form': form,
        'lot': lot,
        'ranch': ranch
    }

    return render(request, 'lots/lot_detail.html', context)

def change_cow_count(request, ranch_id, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    ranch = get_object_or_404(Ranch, id=ranch_id)

    if request.method == 'POST':
        date = request.POST.get('date', datetime.now())
        cow_count = request.POST.get('cow_count', None)
        video_file = request.FILES.get('video_file', None)

        if cow_count:
            count_history = CountHistory(
                lot=lot,
                pasture=lot.pasture,
                cow_count=cow_count,
                date=date,
                method='manual'
            )
            count_history.save()
        elif video_file:
            video_upload = VideoUpload(
                lot=lot,
                video=video_file,
                date_uploaded=date
            )
            video_upload.save()
            process_video(video_upload)

        if cow_count:
            lot.cow_count = cow_count
            lot.save()

        return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot_id)

    return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot_id)

def process_video(video_upload):
    video_path = video_upload.video.path
    #cap = cv2.VideoCapture(video_path)
    cow_count = 0

    # Implement your video processing logic here to count cows

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