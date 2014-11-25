from django import forms
from woid.core.models import Organization

class OrganizationForm(forms.ModelForm):

    allow_domain = forms.CharField(widget=forms.TextInput(),
        max_length=255,
        required=True,
        help_text=u'''
        <p>Specify the domains allowed to sign up on the network. 
        Use comma to separate multiple domains. 
        e.g. <strong>@woid.io</strong>, <strong>@sales.woid.io</strong></p>
        <p>Use <strong>?</strong> character to deny every domain and invite people separetly using the Invite menu.</p>
        <p>Use <strong>*</strong> to allow every domain to register to your network.</p>
        ''')

    class Meta:
        model = Organization
        fields = ['title', 'description', 'url', 'allow_domain']