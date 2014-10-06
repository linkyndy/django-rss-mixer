from django.conf.urls import patterns, url

from mixer.views import MixerView, DeleteView


urlpatterns = patterns('',
    url(r'^$', MixerView.as_view(), name='mixer'),
    url(r'^delete/(?P<feed>.+)$', DeleteView.as_view(), name='delete'),
)
