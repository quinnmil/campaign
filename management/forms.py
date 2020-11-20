"""management forms"""
from django import forms
from django.core.mail import send_mail
from django.urls import path, reverse

from .models import ClaimedJob
from . import errors


class SubmitProofForm(forms.Form):
    """Form displayed to submit proof of job completion"""
    # FIXME these rows/columns aren't being rendered
    proof = forms.CharField(widget=forms.Textarea(attrs={
        "class": "proof-form-class",
        "rows": 5,
        "cols": 20
    }))


class ClaimedJobActionForm(forms.Form):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
    send_email = forms.BooleanField(
        required=False
    )

    @property
    def email_subject_template(self):
        raise NotImplementedError()

    @property
    def email_body_template(self):
        raise NotImplementedError()

    def form_action(self, claimed_job, comment):
        raise NotImplementedError()

    def save(self, claimed_job):
        try:
            comment = self.cleaned_data.get('comment', '')
            action = self.form_action(claimed_job, comment)
        except errors.Error as err:
            self.add_error(None, str(err))

        if self.cleaned_data.get('send_email', False):
            pass
            # todo implement this later
            # https://stackoverflow.com/questions/2809547/creating-email-templates-with-django
        return action


class ApproveForm(ClaimedJobActionForm):

    def form_action(self, claimed_job, comment):
        return claimed_job.approve(comment=comment)


class RejectForm(ClaimedJobActionForm):
    def form_actions(self, claimed_job, comment):
        raise NotImplementedError()
