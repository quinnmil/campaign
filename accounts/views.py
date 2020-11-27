from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, DetailView

from accounts.forms import WorkerSignUpForm
from accounts.models import Worker


class Index(TemplateView):
    template_name = 'index.html'


class WorkerDetailView(DetailView):
    model = Worker

    def get_object(self):
        if self.request.user.is_worker:
            return Worker.objects.get(user=self.request.user)
        return redirect(self.request, 'accounts/login.html')


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
        user, _ = Worker.create(username, password)
        login(request, user)
        return redirect('accounts:detail')
    return render(request, 'register_student.html', {'form': form})
