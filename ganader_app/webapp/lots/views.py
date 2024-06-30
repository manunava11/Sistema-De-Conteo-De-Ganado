from django.shortcuts import render, get_object_or_404, redirect
from .models import Lot, Ranch
from .forms import LotForm

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
