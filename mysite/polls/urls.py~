from django.conf.urls.defaults import *
from mysite.polls.models import Poll

info_dict = {
    'queryset': Poll.objects.all(),
}

urlpatterns = patterns('',
    (r'^$', 'mysite.polls.views.index'),
    (r'^(?P<poll_id>\d+)/(proxy-id=?P<proxy_id>\w*)?$', 'mysite.polls.views.detail'),
    (r'^(?P<poll_id>\d+)/results/(proxy-id=?P<proxy_id>\w*)?$', 'mysite.polls.views.results'),
    (r'^(?P<poll_id>\d+)/vote/(proxy-id=?P<proxy_id>\w*)?$', 'mysite.polls.views.vote'),
    (r'^(proxy-id=?P<proxy_id>\w*)?$', 'mysite.polls.views.index'),
)

