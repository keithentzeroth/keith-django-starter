from django.conf.urls.defaults import *
from mysite.polls.models import Poll

urlpatterns = patterns('',
    (r'^$', 'mysite.polls.views.index'),
    (r'^(?P<poll_id>\d+)/$', 'mysite.polls.views.detail'),
    (r'^(?P<poll_id>\d+)/results/$', 'mysite.polls.views.results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),
)

