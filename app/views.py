import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from google.appengine.api import urlfetch

def home(request, extraStuff=None):
    return render_to_response('index.html', dict(), context_instance=RequestContext(request))

import random
random.seed(3)
def multi_response_messages(request):
    if request.is_ajax():
        return HttpResponse('A Random Message '+ random.randint(1,25))
    else:
        return HttpResponse('Posted Form')



def scrapeLatestBlog( request):
    x = 0
    lb = dict()
    res = urlfetch.fetch( 'http://blog.entzeroth.com');
    rep = res.content
    start = rep.find('blog-posts hfeed')
    feed = rep[start:rep.find('blog-pager', start)]
    curdate_start = feed.find('<h2'); 
    while( curdate_start != -1):
        curdate = feed[curdate_start:feed.find('</h2>',curdate_start)]
        clean_date = curdate[curdate.find('>')+1:]
        clean_date = clean_date[clean_date.find('<span>')+6:clean_date.find('</span>')]
        cur_entry_start = feed.find('<h3', curdate_start)
        next_date_start = feed.find('<h2', curdate_start+1)
        while( cur_entry_start != -1 and (cur_entry_start < next_date_start or next_date_start == -1)):
            entry = feed[cur_entry_start:feed.find('</h3>', cur_entry_start)]
            clean_entry = entry[entry.find('>')+1:]
            lb.__setitem__(x, dict({'date':clean_date,'title':clean_entry}))
#            logging.info("adding:" + clean_date + " -- " + clean_entry)
            cur_entry_start = feed.find('<h3',cur_entry_start+1)
            x = x+1
        curdate_start = next_date_start
    return render_to_response('latest_blogs.html', dict({'latest_blogs': lb}), context_instance=RequestContext(request))

