from django.shortcuts import render, get_object_or_404, redirect
from .models import Pasture
from .forms import PastureForm

# Create your views here.

def pasture_list(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    pastures = Pasture.objects.filter(ranch=ranch)
    return render(request, 'pastures/pasture_list.html', {'pastures': pastures})

def add_pasture(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    if request.method == 'POST':
        form = PastureForm(request.POST)
        if form.is_valid():
            pasture = form.save(commit=False)
            pasture.ranch = ranch
            pasture.save()
            return redirect('pasture_list', ranch_id=ranch.id)
    else:
        form = PastureForm()
    return render(request, 'pastures/add_pasture.html', {'form': form, 'ranch': ranch})
