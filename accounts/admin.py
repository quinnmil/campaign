from django.contrib import admin

# Register your models here.

from accounts.models import Worker, Manager, User

admin.site.register(Worker)
admin.site.register(Manager)
admin.site.register(User)
