from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request, extraStuff=None):
    return render_to_response('index.html', dict(), context_instance=RequestContext(request))
