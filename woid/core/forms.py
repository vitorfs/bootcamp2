from django import forms
from woid.core.models import Organization

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ['title', 'description', 'url', 'allow_domain']