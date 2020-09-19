from django.db import models
from django.contrib.auth.models import AbstractUser
from gigs.models import Campaign, Job
from management.models import ClaimedJob

# Create your models here.


class User(AbstractUser):
    """Generic User object"""
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    # cell_number = models.CharField()


class Worker(models.Model):
    """Worker object, anyone who is able to complete jobs"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pay_earned = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    experience = models.IntegerField('Earned Experience', default=0)

    def __str__(self):
        return self.user.username


class Manager(models.Model):
    """Manager object, managers oversee campaigns"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField('date created')
    campaigns = models.ManyToManyField(Campaign, related_name='managers')
