from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template 
from django.conf import settings
    
urlpatterns = patterns('django.views.generic.simple',
    (r'^home/?$', 'direct_to_template', {'template': 'index.html'}),
    (r'^test/?$', 'direct_to_template', {'template': 'modtagtest.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

