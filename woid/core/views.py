from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from woid.core.models import Organization
from woid.core.forms import OrganizationForm

def home(request):
    user = request.user
    if user.is_authenticated():
        organization_name = user.account.organization.name
        return HttpResponseRedirect(reverse('organization', args=(organization_name,)))
    else:
        return render(request, 'core/cover.html')

@login_required
def organization(request, organization_name):
	return render(request, 'core/index.html')

@login_required
def manage(request, organization_name):
    organization = request.user.account.organization
    form = OrganizationForm(instance=organization)
    return render(request, 'core/manage.html', { 'form' : form })
