from django.shortcuts import render, get_object_or_404, redirect
from .models import Pasture, Ranch
from lots.models import Lot
from .forms import PastureForm, LotSelectionForm

def pasture_list(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    pastures = Pasture.objects.filter(ranch_id=ranch_id)
    available_lots = Lot.objects.filter(ranch_id=ranch_id, pasture__isnull=True)

    if request.method == 'POST':
        form = LotSelectionForm(request.POST)
        if form.is_valid():
            lot_id = form.cleaned_data['lot_id']
            pasture_id = request.POST.get('pasture_id')
            pasture = get_object_or_404(Pasture, id=pasture_id)

            # Free the current lot assigned to this pasture if exists
            if pasture.lot_set.exists():
                current_lot = pasture.lot_set.first()
                current_lot.pasture = None
                current_lot.save()

            # Assign the new lot to the pasture if one is selected
            if lot_id:
                new_lot = get_object_or_404(Lot, id=lot_id.id)
                new_lot.pasture = pasture
                new_lot.save()

            return redirect('pasture-list', ranch_id=ranch_id)
    else:
        form = LotSelectionForm()

    return render(request, 'pastures/pasture_list.html', {'pastures': pastures, 'form': form, 'available_lots': available_lots, 'ranch': ranch})

def add_pasture(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    if request.method == 'POST':
        form = PastureForm(request.POST)
        if form.is_valid():
            pasture = form.save(commit=False)
            pasture.ranch = ranch
            pasture.save()
            return redirect('pasture-list', ranch_id=ranch.id)
    else:
        form = PastureForm()
    return render(request, 'pastures/add_pasture.html', {'form': form, 'ranch': ranch})
