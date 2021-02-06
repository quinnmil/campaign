from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, DetailView

from accounts.forms import WorkerSignUpForm
from accounts.models import Worker
from django.urls import reverse, reverse_lazy


class Index(TemplateView):
    template_name = 'index.html'


class WorkerDetailView(DetailView):
    model = Worker

    def get_object(self):
        if self.request.user.is_authenticated and self.request.user.is_worker:
            return Worker.objects.get(user=self.request.user.id)
        # fixme - this redirect doesn't work
        return redirect('accounts:login')


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'


def logout_view(request):
    logout(request)
    return redirect('accounts:registerStudent')


def select_type_view(request):
    return render(request, 'select.html')


def register_worker_view(request):
    """registers worker, creates new user"""
    form = WorkerSignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        user, _ = Worker.create(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        return redirect('accounts:detail')
    return render(request, 'register_student.html', {'form': form})
