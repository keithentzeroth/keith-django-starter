from django.conf.urls.defaults import *
from django.contrib import admin
from utils import dispatch
from starter import views
from django.views.generic.simple import direct_to_template 
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
    
urlpatterns += patterns('starter',

    (r'^login/?$', dispatch(post=views.plogin, get=views.glogin)),
    (r'^logout/?$', 'views.vlogout'),
    (r'^account/?$', dispatch(post=views.paccount, get=views.gaccount)),
    (r'^(.*)', 'views.home'),

)
