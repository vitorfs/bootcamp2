from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from woid.feed.models import Feed

FEEDS_PER_PAGE = 20

@login_required
def feed(request, organization_name):
    organization = request.user.account.organization
    feeds = Feed.get_feeds(organization)
    paginator = Paginator(feeds, FEEDS_PER_PAGE)
    stream = paginator.page(1)
    return render(request, 'feed/index.html', { 'stream': stream })

@login_required
def load(request):
    from_feed = request.GET.get('from_feed')
    page = request.GET.get('page')
    organization = request.user.account.organization
    feeds = Feed.get_feeds(organization, from_feed)

    paginator = Paginator(feeds, FEEDS_PER_PAGE)
    try:
        stream = paginator.page(page)
    except PageNotAnInteger:
        stream = paginator.page(1)
    except EmptyPage:
        return HttpResponse(u'')

    html = []

    for feed in stream:
        html.append(render_to_string('feed/partial/feed.html', { 'feed' : feed }))
    response = u'\n'.join(html)
    
    return HttpResponse(response)

@login_required
def post(request):
    feed = Feed()
    feed.user = request.user
    feed.organization = request.user.account.organization
    feed.post = request.POST['post'].strip()
    feed.save()
    return HttpResponse()