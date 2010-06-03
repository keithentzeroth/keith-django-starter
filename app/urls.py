from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template 
from django.conf import settings
from utils import dispatch
    
urlpatterns = patterns('django.views.generic.simple',
    (r'^code/?$', 'direct_to_template', {'template': 'code/1_css_glow_buttons.html'}),
    (r'^interests/?$', 'direct_to_template', {'template': 'interests/index.html'}),
    (r'^about/?$', 'direct_to_template', {'template': 'about.html'}),
    (r'^people/?$', 'direct_to_template', {'template': 'shouts.html'}),
    (r'^blog/?$', 'direct_to_template', {'template': 'blog/index.html'}),
)

#if settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#    )

urlpatterns += patterns('',
    (r'^latest_blogs/?$', 'views.scrapeLatestBlog'),    
    (r'^(.*)$', 'views.home'),
)
