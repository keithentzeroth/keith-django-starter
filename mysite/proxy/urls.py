from django.conf.urls.defaults import *
from mysite.proxy.models import Invite, Relation

urlpatterns = patterns('',
    (r'^invite/?$', 'mysite.proxy.views.invites'),
    (r'^(.*)', 'mysite.proxy.views.relations'),
)
