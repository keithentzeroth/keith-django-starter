import re

class ProxyMiddleware(object):

    def process_request(self, request):
        old_path = request.path
        #TODO should this regex be better...maybe no digits, special chars, etc..?
        p = re.compile(r"(.*/)?(?P<tag>proxy=(?P<name>(.*))/?)$")
        x = p.match(old_path)        
        if( x != None):
            path= old_path[:x.start('tag')]
            request.path = path
            request.path_info = path                    
            request.META['PATH_INFO'] = path
            print('new path = '+ request.path)
            if request.method=='GET':
                q = request.GET.copy();
                q.__setitem__('proxy', x.group('name'))
                request.GET = q
            else:
                q = request.POST.copy();
                q.__setitem__('proxy', x.group('name'))
                request.POST = q
            #TODO change context of user to make requests pull back proxied data?
        return None

    def process_response(self, request, response):
        print('Content-Type:' + response['Content-Type'])
#        print('content:' + response.content)
        #check request for proxy attribute
        #add proxy attribute to "href's"
        #add proxy attribute to form actions
        #if proxy, remove code within proxy tags
        #else remove proxy tags and leave code
        return response
