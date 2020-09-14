import logging
from django.shortcuts import render, HttpResponse, redirect

from django.views import generic

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from gigs.models import Job
from management.models import ClaimedJob

MAX_JOBS = 2

logger = logging.getLogger(__name__)
User = get_user_model()


class JobsList(generic.ListView):
    """Job List"""
    model = Job
    context_object_name = 'jobs'


class DetailView(generic.DetailView):
    """Job detail view"""
    model = Job
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        user = self.request.user
        claimed = user.worker.jobs_in_progress.filter(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['jobClaimed'] = False
        if user.is_worker and claimed:
            context['jobClaimed'] = True
        return context

class ValidationError(Exception):
    """Raised when new job validation fails"""

def validate_job(current_jobs, new_job):
    """checks that user can add jobs"""
    if len(current_jobs.all()) > MAX_JOBS:
        raise ValidationError("Job limit exceeded")
    for claimed in current_jobs.all():
        if claimed.job.id == new_job.id:
            raise ValidationError("you've already added this job")


def claim_job(request):
    """Assigns job to current user"""
    context = {}
    if not request.user.is_worker:
        HttpResponse("non-worker accounts cannot claim jobs")
        raise PermissionDenied
    if request.method == 'POST':
        try:
            job_id = request.POST['job_id']
            base_job = get_object_or_404(Job, pk=job_id)
            current_jobs = request.user.worker.jobs_in_progress
            # audit current jobs, something like:
            validate_job(current_jobs, base_job)
            claimed_job = ClaimedJob(job=Job, worker=request.user.worker)
            current_jobs.add(claimed_job)
            job.in_progress_count += 1
            job.save()
            claimed_job.save()
            context['job'] = job
        except ValidationError as err:
            logger.exception('Unable to add new job %s', err)

    return render(request, "gigs/claim_status.html", context)
