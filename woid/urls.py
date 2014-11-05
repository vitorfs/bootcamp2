from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'woid.core.views.home', name='home'),
	url(r'^feed/', include('woid.feed.urls')),
)
