from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/login/'}, name='logout'),
    url(r'^login-redirect/$', 'woid.core.views.login_redirect', name='login_redirect'),
    url(r'^(?P<organization_name>[^/]+)/$', 'woid.core.views.home', name='home'),
    url(r'^(?P<organization_name>[^/]+)/manage/$', 'woid.core.views.manage', name='manage'),
	url(r'^(?P<organization_name>[^/]+)/feed/$', include('woid.feed.urls')),
)
