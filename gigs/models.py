from django.db import models

# Create your models here.

class Campaign(models.Model):
    name = models.CharField(max_length=30)
    candidate = models.CharField(max_length=20)
    description = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='')
    total_count = models.IntegerField('total jobs at time of creation')
    in_progress_count = models.IntegerField('total jobs claimed', default=0)
    created_on = models.DateTimeField('date created', auto_now_add=True)
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()
    zip_code = models.CharField(max_length=5)
    pay = models.DecimalField(max_digits=5, decimal_places=2)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    def remaining_count(self):
        return self.total_count - self.in_progress_count

    def __str__(self):
        return self.title
