from django.shortcuts import render, get_object_or_404, redirect
from .models import Lot, Ranch
from .forms import LotForm
from cattle_countings.forms import ManualCountForm, VideoUploadForm

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

    # Get count history for the lot
    count_history = lot.count_history.all()

    # Initialize forms
    manual_count_form = ManualCountForm()
    video_upload_form = VideoUploadForm()

    if request.method == 'POST':
        if 'cow_count' in request.POST:
            manual_count_form = ManualCountForm(request.POST)
            if manual_count_form.is_valid():
                count = manual_count_form.save(commit=False)
                count.lot = lot
                count.pasture = lot.pasture
                count.method = 'manual'
                count.save()
                return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot.id)
        elif 'video_file' in request.FILES:
            video_upload_form = VideoUploadForm(request.POST, request.FILES)
            if video_upload_form.is_valid():
                # Process video and count cows (implement this functionality)
                # For now, let's just pretend the count is 100
                cow_count = 100  # Replace with actual count from video processing
                CountHistory.objects.create(
                    lot=lot,
                    pasture=lot.pasture,
                    cow_count=cow_count,
                    method='video'
                )
                return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot.id)

    context = {
        'lot': lot,
        'count_history': count_history,
        'manual_count_form': manual_count_form,
        'video_upload_form': video_upload_form,
        'ranch': ranch,  # Add ranch to context
    }

    return render(request, 'lots/lot_detail.html', context)