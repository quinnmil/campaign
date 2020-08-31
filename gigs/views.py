from django.shortcuts import render, HttpResponse, redirect

from django.views.generic import ListView

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


def jobDetails(request):
    return HttpResponse("You're looking at a job detail page")

class JobsList(ListView): 
    model = Job
    context_object_name = 'jobs'

