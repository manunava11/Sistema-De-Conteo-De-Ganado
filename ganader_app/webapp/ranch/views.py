from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Ranch, RanchMembership
from .forms import RanchForm, AddMemberForm

@login_required
def create_ranch(request):
    if request.method == 'POST':
        form = RanchForm(request.POST)
        if form.is_valid():
            ranch = form.save(commit=False)
            ranch.owner = request.user
            ranch.save()
            RanchMembership.objects.create(user=request.user, ranch=ranch)
            return redirect('ranch-detail', ranch_id=ranch.id)
    else:
            form = RanchForm()
    return render(request, 'ranch/create_ranch.html', {'form': form})
    
@login_required
def ranch_detail(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    members = RanchMembership.objects.filter(ranch=ranch)
    return render(request, 'ranch/ranch_detail.html', {'ranch': ranch, 'members': members})

@login_required
def add_member(request, ranch_id):
    ranch = get_object_or_404(Ranch, id=ranch_id)
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            RanchMembership.objects.create(user=user, ranch=ranch)
            return redirect('ranch-detail', ranch_id=ranch.id)
    else:
         form = AddMemberForm()
    return render(request, 'ranch/add_member.html', {'form': form, 'ranch': ranch})


