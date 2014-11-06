from django import forms
from woid.core.models import Organization

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization