from django.conf.urls import patterns, include, url

urlpatterns = patterns('woid.notifications.views',
    url(r'^post/$', 'post', name='post'),
    url(r'^like/$', 'like', name='like'),
)