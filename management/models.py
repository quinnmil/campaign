from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User
from . import errors
from gigs.models import Job
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
        verbose_name='proof that job was completed', null=True, blank=True)
    started_on = models.DateTimeField('Job claimed on', auto_now_add=True)
    completed_on = models.DateTimeField(
        'Job completed on', null=True, blank=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    comment = models.TextField(
        verbose_name='Explanation why approved or rejected', default='')
    objects = models.Manager()  # default manager
    in_progress_jobs = CurrentJobManager()

    def in_progress(self):
        return self.status is self.IN_PROGRESS

    def is_completed(self):
        return self.status is self.COMPLETED

    def time_remaining(self):
        return timezone.now() - self.job.ends_on

    def is_expired(self):
        return timezone.now() > self.job.ends_on

    def __str__(self):
        return self.job.headline

    def approve(self, comment):
        self.status = self.COMPLETED
        self.comment = comment
        self.completed_on = timezone.now()
        # future feature -> add logic to check that user is manager for job's campaign
        self.save()

    def reject(self, comment):
        raise NotImplementedError()

    @classmethod
    def create(
        cls,
        user,
        job_id
    ):
        if not user.is_worker:
            raise errors.UserRollError
        if not user.worker.can_claim:
            raise errors.OverworkedError
        if user.worker.claimed_jobs.filter(job_id=job_id).exists():
            raise errors.AlreadyClaimedError
        try:
            job = Job.objects.get(pk=job_id)
            job.increment_count()
            claimed_job = cls.objects.create(
                status=cls.IN_PROGRESS,
                job=job,
                worker=user.worker
            )
        except Job.DoesNotExist:
            raise errors.InternalError

        return claimed_job

    def quit_job(self):
        self.status = self.QUIT
        self.job.decrement_count()
        self.save()
        return self
