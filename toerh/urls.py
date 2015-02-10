from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

from accounts.views import SignUpFormView

template_name = {'template_name': 'rest_framework/login.html'}

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # Accounts
    url(r'^register/$', SignUpFormView.as_view(), name='register'),
    url(r'^accounts/profile/$', RedirectView.as_view(pattern_name='tokens:list')),
    url(r'^accounts/login/$', RedirectView.as_view(pattern_name='login')),

    url(r'^tokens/', include('tokens.urls', namespace='tokens')),

    # API authentication
    url(r'^$', 'django.contrib.auth.views.login', template_name, name='login'),
    url(r'', include('rest_framework.urls',\
        namespace='rest_framework')),


    # API endpoint version 1
    url(r'^api/v1/', include('positioningservice.urls', namespace='positioningservice')),

    # Version 2 could be here
)
