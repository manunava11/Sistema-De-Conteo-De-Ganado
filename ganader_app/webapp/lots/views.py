from django.shortcuts import render, get_object_or_404, redirect
from .models import Lot, Ranch
from cattle_countings.models import CowCount, UploadedVideo
from .forms import LotForm, CowCountForm
from cattle_countings.forms import ManualCountForm, VideoUploadForm
from datetime import datetime
from cattle_countings.tasks import process_video
from django_celery_results.models import TaskResult
from django.http import JsonResponse
from celery.result import AsyncResult

def lot_list(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    lots = Lot.objects.filter(ranch_id=ranch_id)
    lots_tuple = []
    for lot in lots:
        latest_cow_count = CowCount.objects.filter(lot=lot).latest('date').cow_count
        lot_data = (lot, latest_cow_count)
        lots_tuple.append(lot_data)

    return render(request, 'lots/lots_list.html', {'lots_tuple': lots_tuple, 'ranch': ranch})

def add_lot(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    if request.method == 'POST':
        lot_form = LotForm(request.POST)
        cow_count_form = CowCountForm(request.POST)

        if lot_form.is_valid() and cow_count_form.is_valid():
            lot = lot_form.save(commit=False)
            lot.ranch = ranch
            lot.save()
            cow_count = cow_count_form.save(commit=False)
            cow_count.lot = lot
            cow_count.method = 'Manual'
            cow_count.save()
            return redirect('lot-list', ranch_id=ranch.id)
    else:
        lot_form = LotForm()
        cow_count_form = CowCountForm()
    return render(request, 'lots/add_lot.html', {'lot_form': lot_form, 'cow_count_form': cow_count_form, 'ranch': ranch})

def lot_detail(request, ranch_id, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    ranch = get_object_or_404(Ranch, id=ranch_id)

    lot_cow_count = CowCount.objects.filter(lot=lot).order_by('-date')
    latest_cow_count = CowCount.objects.filter(lot=lot).latest('date').cow_count

    manual_count_form = ManualCountForm()
    video_upload_form = VideoUploadForm()

    if request.method == 'POST':
        if 'manual_count' in request.POST:
            manual_count_form = ManualCountForm(request.POST)
            if manual_count_form.is_valid():
                manual_count = manual_count_form.save(commit=False)
                manual_count.lot = lot
                manual_count.pasture = lot.pasture
                manual_count.method = 'Manual'
                manual_count.save()
                return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot.id)

        elif 'upload_video' in request.POST:
            video_upload_form = VideoUploadForm(request.POST, request.FILES)
            if video_upload_form.is_valid():
                video_upload = video_upload_form.save(commit=False)
                cow_count_record = CowCount.objects.create(
                    lot=lot,
                    pasture=lot.pasture,
                    cow_count=0,  # Initial count, will be updated later
                    method='video',
                    date=video_upload_form.cleaned_data['date'],
                    comment=video_upload_form.cleaned_data['comment']
                )
                video_upload.cow_count = cow_count_record
                video_upload.save()
                return redirect('lot-detail', ranch_id=ranch_id, lot_id=lot.id)

    lot_form = LotForm(instance=lot)

    # Fetch ongoing tasks' statuses
    #ongoing_tasks = {}
    for video in UploadedVideo.objects.filter(cow_count__lot=lot):
        if video.task_id:
            #result = AsyncResult(video.task_id)
            task_id = video.task_id
            #ongoing_tasks[video.task_id] = result.status

    context = {
        'lot': lot,
        'lot_cow_count': lot_cow_count,
        'manual_count_form': manual_count_form,
        'video_upload_form': video_upload_form,
        'lot_form': lot_form,
        'ranch': ranch,
        'latest_cow_count': latest_cow_count,
        #'tasks_info': ongoing_tasks,
        'task_id': task_id,
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
