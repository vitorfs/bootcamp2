from django.conf.urls import patterns, include, url

urlpatterns = patterns('woid.notifications.views',
    url(r'^$', 'notifications', name='notifications'),
    url(r'^check/$', 'check_notifications', name='check_notifications'),
    url(r'^last/$', 'last_notifications', name='last_notifications'),
)