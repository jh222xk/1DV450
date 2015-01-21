from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),


    url(r'^api/1.0/positions/', include('positioningservice.urls', namespace = 'positioningservice')),
)
