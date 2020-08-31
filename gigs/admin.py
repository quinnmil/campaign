from django.contrib import admin

# Register your models here.
from gigs.models import Campaign, Job

admin.site.register(Campaign)
admin.site.register(Job)