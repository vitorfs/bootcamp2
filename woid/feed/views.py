from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from woid.feed.models import Feed

@login_required
def feed(request, organization_name):
    stream = Feed.objects.filter(organization__name=organization_name)
    return render(request, 'feed/index.html', { 'stream': stream })

@login_required
def post(request):
    feed = Feed()
    feed.user = request.user
    feed.organization = request.user.account.organization
    feed.post = request.POST['post'].strip()
    feed.save()
    return HttpResponse()