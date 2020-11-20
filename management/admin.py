from django.contrib import admin
from django.contrib import messages
from management.models import ClaimedJob
from django.utils.html import format_html
from django.urls import path, reverse
from django.template.response import TemplateResponse

from django.http import HttpResponseRedirect

from .forms import ApproveForm, RejectForm
from . import errors


@admin.register(ClaimedJob)
class ClaimedJobAdmin(admin.ModelAdmin):
    """
    custom admin panel for the claimedJob objects
    allows filtering by status as well as custom actions for approval
    """
    fields = (
        ('job', 'worker'),
        'status',
        'proof',
        'comment'
    )
    list_display = (
        'job',
        'worker',
        'status',
        'claimed_actions'
    )
    list_filter = (
        'status',
    )
    list_select_related = (
        'worker',
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:claimed_job_id>/approve',
                 self.admin_site.admin_view(self.process_approve),
                 name='approve-complete'),
            path('<int:claimed_job_id>/reject',
                 self.admin_site.admin_view(self.process_reject),
                 name='reject-complete')
        ]
        return urls + my_urls

    def process_action(
        self,
        request,
        claimed_job_id,
        action_form,
        action_title
    ):
        claimed_job = self.get_object(request, claimed_job_id)
        all_urls = self.get_urls()

        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    # comment = form.cleaned_data.get('comment')
                    form.save(claimed_job)
                except errors.Error as e:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'management_claimedjob_change',
                        args=[claimed_job.pk],
                        current_app=self.admin_site.name
                    )
                    return HttpResponseRedirect(url)

        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['claimed_job'] = claimed_job
        context['title'] = action_title

        return TemplateResponse(
            request,
            'admin/claimed_job/review.html',
            context=context
        )

    def claimed_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Approve</a>&nbsp; \
             <a class="button" href="{}">Reject</a>',
            reverse('admin:approve-complete', args=[obj.pk]),
            reverse('admin:reject-complete', args=[obj.pk])
        )

    def process_approve(self, request, claimed_job_id, *args, **kwargs):
        return self.process_action(
            request=request,
            claimed_job_id=claimed_job_id,
            action_form=ApproveForm,
            action_title='Approve Completed Job',
        )

    def process_reject(self, request, claimed_job_id, *args, **kwargs):
        return self.process_action(
            request=request,
            claimed_job_id=claimed_job_id,
            action_form=RejectForm,
            action_title='Reject Incomplete Job'
        )
