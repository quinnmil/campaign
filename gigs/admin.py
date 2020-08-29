from django.contrib import admin

# Register your models here.
from .models import Campaign, Job, Worker

admin.site.register(Campaign)
admin.site.register(Job)
admin.site.register(Worker)