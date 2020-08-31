from django.contrib import admin

# Register your models here.

from accounts.models import Worker, Manager

admin.site.register(Worker)
admin.site.register(Manager)