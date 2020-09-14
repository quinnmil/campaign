from django.db import models
from datetime import datetime
# Create your models here.


class ClaimedJob(models.Model):
    """Job object, created when gig.Job claimed by worker"""
    IN_PROGRESS = 'P'
    COMPLETED = 'C'
    QUIT = 'Q'
    REJECTED = 'R'

    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (QUIT, 'Quit'),
        (REJECTED, 'R')
    ]

    job = models.models.ForeignKey(
        "gigs.Job", verbose_name=_("Job"), on_delete=models.CASCADE)
    worker = models.ForeignKey("accounts.Worker", verbose_name=_(
        "worker"), on_delete=models.CASCADE)
    status = models.CharField(
        _("job status"), max_length=1, choices=STATUS_CHOICES, default=IN_PROGRESS)
    proof = models.TextField(_('proof that job was completed', blank=True))
    started_on = models.DateTimeField('Job claimed on', auto_now_add=True)

    def in_progress(self):
        return self.status is IN_PROGRESS

    def is_completed(self):
        return self.status is COMPLETED

    def time_remaining(self):
        return datetime.now - self.job.ends_on

    def is_expired(self):
        return datetime.now() > self.job.ends_on
