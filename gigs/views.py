from django.shortcuts import render, HttpResponse, redirect

from django.views import generic

# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from gigs.models import Job

import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def index(request):
    user = request.user
    data = {
        "jobs": Job.objects.all()
    }
    if user.is_authenticated:
        data['email'] = user.email
        if user.is_worker:
            data['job'] = 'worker'

    return render(request, 'board.html', data)


class JobsList(generic.ListView):
    model = Job
    context_object_name = 'jobs'


class DetailView(generic.DetailView):
    model = Job
    context_object_name = 'job'

    # def get_context_data(self, **kwargs):
    #     # call base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
