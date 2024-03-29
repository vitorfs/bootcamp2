from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'woid.core.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^feed/', include('woid.feed.urls')),
    url(r'^(?P<organization_name>[^/]+)/$', 'woid.core.views.organization', name='organization'),
    url(r'^(?P<organization_name>[^/]+)/notifications/$', include('woid.notifications.urls')),
    url(r'^(?P<organization_name>[^/]+)/manage/$', 'woid.core.views.manage', name='manage'),
    url(r'^(?P<organization_name>[^/]+)/feed/$', 'woid.feed.views.feed', name='feed'),
)
