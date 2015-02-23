from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

from accounts.views import SignUpFormView
from positioningservice.views import PositionViewSet, EventViewSet, TagViewSet, PositionSearchViewSet


router = routers.DefaultRouter()
router.register(r'positions', PositionViewSet)
router.register(r'events', EventViewSet)
router.register(r'tags', TagViewSet)
router.register(r'search', PositionSearchViewSet, base_name='search')

template_name = {'template_name': 'rest_framework/login.html'}

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),

                       # Accounts
                       url(r'^register/$', SignUpFormView.as_view(), name='register'),

                       # Tokens
                       url(r'^tokens/', include('tokens.urls', namespace='tokens')),

                       # API authentication
                       url(r'^$', 'django.contrib.auth.views.login', template_name, name='login'),
                       url(r'', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token', name='token-auth'),

                       # Available API versions
                       url(r'^api/$', TemplateView.as_view(template_name="api_list.html"), name='api-list'),

                       # API endpoint version 1
                       url(r'^api/v1/', include(router.urls, namespace='api-v1')),

                       # API endpoint version 2 could be here
)
