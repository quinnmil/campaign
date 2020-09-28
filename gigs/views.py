import logging
from django.shortcuts import render, HttpResponse

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
        claimed = ClaimedJob.objects.filter(
            worker=user.worker, job_id=self.kwargs.get(self.pk_url_kwarg)
        )
        context = super().get_context_data(**kwargs)
        context['jobClaimed'] = False
        if user.is_worker and claimed:
            context['jobClaimed'] = True
        return context


class ValidationError(Exception):
    """Raised when new job validation fails"""


def validate_job(current_jobs, new_job):
    """checks that user can add jobs"""
    if new_job.jobs_remaning < 1:
        raise ValidationError(
            'No jobs remaining to claim, someone might have beat you to it')
    if len(current_jobs.all()) > MAX_JOBS:
        raise ValidationError('Job limit exceeded')
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
            job_id = request.POST.get('job_id', None)
            base_job = get_object_or_404(Job, pk=job_id)
            current = ClaimedJob.objects.filter(job_id=job_id).filter(
                worker_id=request.user.worker.id)

            other_current = request.user.worker.claimed_jobs.filter(
                job_id=job_id)
            if current:
                raise ValidationError("you've already claimed this job")
            # validate_job(current_jobs, base_job)
            claimed_job = ClaimedJob.objects.create(
                job=base_job, worker=request.user.worker)
            base_job.in_progress_count += 1
            base_job.save()
            context['claimedJob'] = claimed_job
            context['job'] = base_job
        except ValidationError as err:
            logger.exception('Unable to add new job %s', err)
            context['error'] = err

    return render(request, "gigs/claim_status.html", context)


def quit_job(request):
    """removes job from current user"""
    context = {}
    if not request.user.is_worker:
        HttpResponse("non-worker accounts cannot claim jobs")
        raise PermissionDenied
    if request.method == 'POST':
        try:
            job_id = request.POST['job_id']
            base_job = get_object_or_404(Job, pk=job_id)
            claimed_job = request.user.worker.claimed_jobs.get(
                job_id=job_id)
            claimed_job.status = 'Q'
            claimed_job.save()

            base_job.in_progress_count -= 1
            base_job.save()
            context['claimedJob'] = claimed_job
            context['job'] = base_job
        except ValidationError as err:
            logger.exception('Unable to add new job %s', err)
            context['error'] = err
    return render(request, "gigs/quit_status.html", context)
