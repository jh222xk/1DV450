from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # API authentication
    url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
    url(r'^api-auth/', include('rest_framework.urls',\
        namespace='rest_framework')),


    # Positions endpoint
    url(r'^api/1.0/positions/', include('positioningservice.urls', namespace = 'positioningservice')),
)
