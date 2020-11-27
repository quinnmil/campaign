import logging
from django.shortcuts import render, HttpResponse, get_object_or_404

from django.views import generic
from django.urls import reverse

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.http import Http404

from gigs.models import Job
from management.models import ClaimedJob

from management.errors import *


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


def claim_job(request):
    """Assigns job to current user"""
    context = {}
    if request.method == 'POST':
        try:
            job_id = request.POST.get('job_id', None)
            context['claimedJob'] = ClaimedJob.create(request.user, job_id)
        except (UserRollError, OverworkedError, AlreadyClaimedError) as err:
            logger.exception('Unable to claimed job: %s', err)
            context['error'] = err
        except InternalError as err:
            raise Http404('The requested gig does not exist') from err

    return render(request, "gigs/claim_status.html", context)


def quit_job(request):
    """removes job from current user"""
    context = {}
    if request.method == 'POST':
        try:
            job_id = request.POST['job_id']
            claimed_job = request.user.worker.claimed_jobs.get(
                job_id=job_id)
            context['claimedJob'] = claimed_job.quit_job()
        except (UserRollError, ClaimedJob.DoesNotExist) as err:
            logger.exception('Unable to quit job: %s', err)
            context['error'] = err
    return render(request, "gigs/quit_status.html", context)
