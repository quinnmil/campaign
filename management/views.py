from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied
from .forms import SubmitProofForm
from .models import ClaimedJob
# Create your views here.


def complete_job(request, job_id):
    # check user is worker
    if request.user.is_worker:
        claimed_job = request.user.worker.claimed_jobs.get(
            job_id=job_id
        )
        if claimed_job:
            form = SubmitProofForm()
            if request.method == 'POST':
                form = SubmitProofForm(request.POST)
                if form.is_valid():
                    proof = form.cleaned_data.get('proof', None)
                    # change job status to pending
                    claimed_job.status = 'S'
                    claimed_job.proof = proof
                    claimed_job.save()
                    return redirect("submitted_status.html")
            context = {
                "form": form,
                "claimed_job": claimed_job
            }
            return render(request, "gigs/complete_gig.html", context=context)
    # TODO implement proper error status page with django messaging
    raise PermissionDenied
