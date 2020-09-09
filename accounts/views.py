from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView, DetailView

from accounts.forms import WorkerSignUpForm, ManagerSignUpForm
from accounts.models import User, Worker, Manager


class Index(TemplateView):
    template_name = 'index.html'


class WorkerDetailView(DetailView):
    model = Worker

    def get_object(self):
        return Worker.objects.get(user=self.request.user)


def logout_view(request):
    logout(request)
    return redirect('accounts:registerStudent')


def login_view(request):
    form = AuthenticationForm()
    return render(request, template_name='accounts/login.html', context={"form": form} )


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
