from django.contrib import admin
from django.contrib import messages
from management.models import ClaimedJob

# Register your models here.


@admin.register(ClaimedJob)
class ClaimedJobAdmin(admin.ModelAdmin):
    """
    custom admin panel for the claimedJob objects
    allows filtering by status as well as custom actions for approval
    """
    fields = (('job', 'worker'), 'status', 'proof')
    list_display = ('job', 'worker', 'status')
    list_filter = ('status',)
    actions = ['verify_complete']

    def verify_complete(self, request, queryset):
        approved = queryset.update(status='C')
        # fixme
        self.message_user(request,
                          '%d jobs verified and marked as completed',
                          approved, messages.success)
