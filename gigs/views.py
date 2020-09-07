import logging
from django.shortcuts import render, HttpResponse, redirect

from django.views import generic

from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from gigs.models import Job


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

    return render(request, 'job_list.html', data)


class JobsList(generic.ListView):
    model = Job
    context_object_name = 'jobs'

    # def results(self):
    #     # user.location is within 100mil of this job


class DetailView(generic.DetailView):
    model = Job
    context_object_name = 'job'

    # def get_context_data(self, **kwargs):
    #     # call base implementation first to get a context
    #     context = super().get_context_data(**kwargs)


MAX_JOBS = 2


def validate_job(current_jobs, new_job):
    if len(current_jobs.all()) > MAX_JOBS:
        raise Exception("Job limit exceeded")
    for job in current_jobs.all():
        if job.id == new_job.id:
            raise Exception("you've already added this job")


def claimJob(request):
    """Assigns job to current user"""
    context = {}
    if not request.user.is_worker:
        HttpResponse("non-worker accounts cannot claim jobs")
        raise PermissionDenied
    if request.method == 'POST':
        try:
            job_id = request.POST['job_id']
            job = get_object_or_404(Job, pk=job_id)
            current_jobs = request.user.worker.jobs_in_progress
            # audit current jobs, something like:
            validate_job(current_jobs, job)
            current_jobs.add(job)
            job.in_progress_count += 1
            job.save()
            context['job'] = job
        except Exception as e:
            context['error'] = e
        return render(request, "gigs/claim_status.html", context)
