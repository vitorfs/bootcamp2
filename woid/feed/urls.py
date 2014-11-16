from django.conf.urls import patterns, include, url

urlpatterns = patterns('woid.feed.views',
    url(r'^post/$', 'post', name='post'),
    url(r'^load/$', 'load', name='load'),
    url(r'^load_new/$', 'load_new', name='load_new'),
    url(r'^check/$', 'check', name='check'),    
)