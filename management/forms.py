from django import forms

from .models import ClaimedJob


class SubmitProofForm(forms.Form):
    # FIXME these rows/columns aren't being rendered
    proof = forms.CharField(widget=forms.Textarea(attrs={
        "class": "proof-form-class",
        "rows": 5,
        "cols": 20
    }))
