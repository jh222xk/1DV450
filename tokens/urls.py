from django.conf.urls import patterns, url

from .views import TokenListView, TokenCreate, TokenDelete

urlpatterns = patterns('tokens.views',
                       url(r'^$', TokenListView.as_view(), name='list'),
                       url(r'^new$', TokenCreate.as_view(), name='new'),
                       url(r'^delete/(?P<pk>[-_\w]+)$', TokenDelete.as_view(), name='delete'),
)
