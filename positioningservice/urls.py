from django.conf.urls import patterns, url
from .views import api_root, PositionListView, PositionDetailView, EventListView, EventDetailView, TagListView, TagDetailView

urlpatterns = patterns('positioningservice.views',
                      url(r'^$', api_root),

                       # Positions API
                       url(r'^positions/$', PositionListView.as_view(),
                           name='position-list'),
                       url(r'^positions/(?P<pk>[-_\w]+)$',
                           PositionDetailView.as_view(), name='position-detail'),

                       # Events API
                       url(r'^events/$', EventListView.as_view(),
                           name='event-list'),
                       url(r'^events/(?P<pk>[-_\w]+)$',
                           EventDetailView.as_view(), name='event-detail'),

                       # Tags API
                       url(r'^tags/$', TagListView.as_view(),
                           name='tag-list'),
                       url(r'^tags/(?P<pk>[-_\w]+)$',
                           TagDetailView.as_view(), name='tag-detail'),
                       )
