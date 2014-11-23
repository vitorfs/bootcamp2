from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from woid.feed.models import Feed
from woid.activities.models import Activity, Notification
import json

FEEDS_PER_PAGE = 20

def _stream(feeds, user):
    html = []
    for feed in feeds:
        html.append(render_to_string('feed/partial/feed.html', { 'feed' : feed, 'user': user }))
    return u'\n'.join(html)

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
    user = request.user
    organization = request.user.account.organization
    feeds = Feed.get_feeds(organization, from_feed)

    paginator = Paginator(feeds, FEEDS_PER_PAGE)
    try:
        paginated_feeds = paginator.page(page)
    except PageNotAnInteger:
        paginated_feeds = paginator.page(1)
    except EmptyPage:
        return HttpResponse(u'')
    
    return HttpResponse(_stream(paginated_feeds, user))

@login_required
def load_new(request):
    user = request.user
    organization = request.user.account.organization
    last_feed = request.POST.get('last_feed')
    feeds = Feed.get_feeds_after(organization, last_feed)
    return HttpResponse(_stream(feeds, user))

@login_required
def post(request):
    organization = request.user.account.organization
    post = request.POST.get('post').strip()
    user = request.user
    feed = Feed(organization=organization, post=post, user=user)
    feed.save()
    return load_new(request)

@login_required
def like(request):
    feed_id = request.POST.get('feed_id')
    feed = Feed.objects.get(pk=feed_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, feed=feed_id, user=user)

    if like:
        Notification.unotify_liked(user, feed)
        like.delete()
    else:
        like = Activity(activity_type=Activity.LIKE, feed=feed_id, user=user)
        like.save()
        Notification.notify_liked(user, feed)

    data = json.dumps({ 'feed_likes': feed.calculate_likes() })
    return HttpResponse(data, content_type='application/json')

@login_required
def check(request):
    organization = request.user.account.organization
    last_feed = request.GET.get('last_feed')
    feeds = Feed.get_feeds_after(organization, last_feed)
    count = feeds.count()
    return HttpResponse(count)
