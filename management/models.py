from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.


class CurrentJobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='P')

    def current_job(self, job_id, worker_id):
        """returns claimedJob of worker matching the job_id"""
        return self.get_queryset().filter(job_id=job_id, worker_id=worker_id)

    def create(self, job, worker):
        """creates new claimedJob or raises exception"""
        if self.current_job(job.id, worker.id):
            raise ValidationError('Job already claimed by worker')
        if not job.can_claim():
            raise ValidationError('Unable to claim job')
        if not worker.can_claim():
            raise ValidationError('Worker is unable to claim another job')
        job.in_progress_count += 1
        job.save()
        return super(CurrentJobManager, self).create(
            job=job, worker=worker)


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
        (REJECTED, 'Rejected'),
        (SUBMITTED, 'Submitted')
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
    completed_on = models.DateTimeField('Job completed on', blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    objects = models.Manager()  # default manager
    in_progress_jobs = CurrentJobManager()

    def in_progress(self):
        return self.status is IN_PROGRESS

    def is_completed(self):
        return self.status is COMPLETED

    def time_remaining(self):
        return datetime.now - self.job.ends_on

    def is_expired(self):
        return timezone.now() > self.job.ends_on

    def __str__(self):
        return self.job.headline

    def approve(self, _user, comment):
        self.status = COMPLETED
        self.completed_on = timezone.now()
        # future feature -> add logic to check that user is manager for job's campaign
