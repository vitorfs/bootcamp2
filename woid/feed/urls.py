from django.conf.urls import patterns, include, url

urlpatterns = patterns('woid.feed.views',
    url(r'^$', 'feed', name='feed'),
    
)