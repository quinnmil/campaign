from django.db import models
from datetime import datetime
# Create your models here.


class CurrentJobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='P')


class ClaimedJob(models.Model):
    """Job object, created when gig.Job claimed by worker"""
    IN_PROGRESS = 'P'
    COMPLETED = 'C'
    QUIT = 'Q'
    REJECTED = 'R'
    SUBMITTED = 'S'

    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (QUIT, 'Quit'),
        (REJECTED, 'R'),
        (SUBMITTED, 'S')
    ]

    job = models.ForeignKey(
        "gigs.Job", verbose_name='Job', on_delete=models.CASCADE)
    worker = models.ForeignKey(
        'accounts.Worker', verbose_name="worker", related_name='claimed_jobs',
        on_delete=models.CASCADE)
    status = models.CharField(
        verbose_name='job status', max_length=1, choices=STATUS_CHOICES, default=IN_PROGRESS)
    proof = models.TextField(
        verbose_name='proof that job was completed', blank=True)
    started_on = models.DateTimeField('Job claimed on', auto_now_add=True)
    objects = models.Manager()  # default manager
    in_progress_jobs = CurrentJobManager()

    def in_progress(self):
        return self.status is IN_PROGRESS

    def is_completed(self):
        return self.status is COMPLETED

    def time_remaining(self):
        return datetime.now - self.job.ends_on

    def is_expired(self):
        return datetime.now() > self.job.ends_on

    def __str__(self):
        return self.job.headline
