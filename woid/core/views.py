from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from woid.core.models import Organization
from woid.core.forms import OrganizationForm

@login_required
def login_redirect(request):
    organization_name = request.user.account.organization.name
    return HttpResponseRedirect(reverse('home', args=(organization_name,)))

@login_required
def home(request, organization_name):
	return render(request, 'core/index.html')

@login_required
def manage(request, organization_name):
    organization = request.user.account.organization
    form = OrganizationForm(instance=organization)
    return render(request, 'core/manage.html', { 'form' : form })