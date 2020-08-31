from django.db import models
from django.contrib.auth.models import AbstractUser
from gigs.models import Campaign, Job

# Create your models here.
class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField('date created')
    jobs_in_progress = models.ManyToManyField(Job, related_name='current_workers')
    jobs_completed = models.ManyToManyField(Job, related_name='finished_workers')
    pay_earned = models.DecimalField(max_digits=8, decimal_places=2)

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField('date created')
    campaigns = models.ManyToManyField(Campaign)