from django.db import models

# Create your models here.


class Campaign(models.Model):
    """
    Object representing a campaign.
    Campaigns create jobs, and are managed by 'managers'" 
    """
    name = models.CharField(max_length=30)
    candidate = models.CharField(max_length=20)
    description = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Job(models.Model):
    """Object representing an unclaimed job"""
    headline = models.CharField(max_length=200)
    description = models.TextField(default='')
    instructions = models.TextField(default='')
    initial_count = models.IntegerField(
        'Initial number of jobs available', default=0)
    in_progress_count = models.IntegerField('Total jobs claimed', default=0)
    created_on = models.DateTimeField('Date Created', auto_now_add=True)
    starts_on = models.DateTimeField('Job begins on')
    ends_on = models.DateTimeField('Job ends on')
    zipcode = models.CharField('Zipcode of Job location', max_length=5)
    pay = models.DecimalField('Pay for completed job',
                              max_digits=5, decimal_places=2)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    def remaining_count(self):
        return self.initial_count - self.in_progress_count

    def __str__(self):
        return self.headline
