from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'woid.core.views.home', name='home'),
	url(r'^icons/$', 'woid.core.views.icons', name='icons'),
)
