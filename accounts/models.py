from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate
from gigs.models import Campaign


class User(AbstractUser):
    """Generic User object"""
    is_manager = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)


class Worker(models.Model):
    """Worker object, anyone who is able to complete jobs"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pay_earned = models.DecimalField(
        max_digits=8, decimal_places=2, default=0.00)
    experience = models.IntegerField('Earned Experience', default=0)
    max_current_jobs = models.PositiveSmallIntegerField(
        'maximum simultaneous jobs', default=2)

    def can_claim(self):
        """returns if the user is able to claim a requested job"""
        return len(self.claimed_jobs.all()) < self.max_current_jobs

    @classmethod
    def create(
        cls,
        username,
        password
    ):
        """Create User and associated Worker account

        Returns (tuple)
            [0] User
            [1] Worker
        """
        user = authenticate(username=username, password=password)
        user.is_worker = True
        user.save()
        worker = cls.objects.create(
            user=user,
            pay_earned=0,
            experience=0
        )
        return user, worker

    def __str__(self):
        return self.user.username


class Manager(models.Model):
    """Manager object, managers oversee campaigns"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField('date created')
    campaigns = models.ManyToManyField(Campaign, related_name='managers')
