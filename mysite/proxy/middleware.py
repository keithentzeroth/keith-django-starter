import re

class ProxyMiddleware(object):
    globals()["proxy_name"] = 'proxy'

    def process_request(self, request):
        old_path = request.path
        #TODO should this regex be better...maybe no digits, special chars, etc..?
        p = re.compile(r"(.*/)?(?P<tag>proxy=(?P<name>(.*))/?)$")
        #TODO check name and lookup necessary attributes about proxy...return 404 if can't find
        #TODO change context of user to make requests pull back proxied data?
        x = p.match(old_path)        
        if( x != None):
            path= old_path[:x.start('tag')]
            request.path = path
            request.path_info = path                    
            request.META['PATH_INFO'] = path
            #TODO consider using a dict instead of adding attribute directly to request
            if request.method=='GET':
                q = request.GET.copy();
                q.__setitem__(proxy_name, x.group('name'))
                request.GET = q
            else:
                q = request.POST.copy();
                q.__setitem__(proxy_name, x.group('name'))
                request.POST = q
        return None

    def process_response(self, request, response):
        #todo only muck if text/html
        if request.method=='GET':
            p = request.GET.get(proxy_name,'none')
        else:
            p = request.POST.get(proxy_name,'none')
        if p != 'none':
            r = re.compile(r'<a(.*)href="(?P<href>([\w/]*))"')
            response.content = self.getnewcontent( r, 'href', response.content, p)
            r = re.compile(r'<form(.*)action="(?P<href>([\w/]*))/?"')
            response.content = self.getnewcontent( r, 'href', response.content, p)
        return response

    def getnewcontent( self,regex, tag, curcontent, p):
        iterator = regex.finditer(curcontent)
        new_cont = ''
        start = 0
        for match in iterator:
            new_cont = new_cont + curcontent[start:match.end(tag)]
            if curcontent[match.end(tag)-1] == "/":
                addp = proxy_name+"="+p+"\""
            else:
                addp = "/"+proxy_name+"="+p+"\""
            new_cont = new_cont + addp
            start = match.end(tag)+1
        new_cont = new_cont + curcontent[start:]
        return new_cont
        

