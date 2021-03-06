from django.conf.urls.defaults import *
from django.contrib import admin
from mysite.utils import dispatch

admin.autodiscover()

urlpatterns = patterns('',
    (r'^login/?$', 'mysite.views.login_view'),
    (r'^logout/?$', 'mysite.views.logout_view'),
    (r'^polls/?$', include('mysite.polls.urls')),
    (r'^proxy/?', include('mysite.proxy.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^(.*)', 'mysite.views.home_view'),
)
