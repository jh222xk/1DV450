from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

template_name = {'template_name': 'rest_framework/login.html'}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),


    url(r'^accounts/profile/$', RedirectView.as_view(pattern_name='positioningservice:list')),

    # API authentication
    url(r'^$', 'django.contrib.auth.views.login', template_name, name='login'),
    url(r'', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'', include('rest_framework.urls',\
        namespace='rest_framework')),


    # Positions endpoint
    url(r'^api/1.0/positions/', include('positioningservice.urls', namespace = 'positioningservice')),
)
