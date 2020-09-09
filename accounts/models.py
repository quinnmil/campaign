from django.db import models
from django.contrib.auth.models import AbstractUser
from gigs.models import Campaign, Job

# Create your models here.


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    # cell_number = models.CharField()


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField('date created')
    jobs_in_progress = models.ManyToManyField(
        Job, related_name='current_workers', blank=True)
    jobs_completed = models.ManyToManyField(
        Job, related_name='completed_workers', blank=True)
    pay_earned = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField('date created')
    campaigns = models.ManyToManyField(Campaign, related_name='managers')
