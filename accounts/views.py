from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

from accounts.forms import WorkerSignUpForm, ManagerSignUpForm

class Index(TemplateView): 
    template_name = 'index.html'

def select_type_view(request):
    return render(request, 'select.html')

def register_worker_view(request):
    form = WorkerSignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        user.is_worker = True
        user.save()
        login(request, user)
        return redirect('index')
    return render(request, 'register_student.html', {'form': form})

def register_manager_view(request):
    form = ManagerSignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        user.is_manager = True
        user.save()
        login(request, user)
        return redirect('index')
    return render(request, 'register_manager.html', {'form': form})

