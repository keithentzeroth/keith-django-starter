class UserAgentMiddleware(object):
    '''UserAgentMiddleware only responsible for making sure that the session contains a platform entry.  Also populates request.platform and request.basetemplate.
    request.platform - current values can be 'mobile' or 'desktop' and these values map directly to static content folders
    request.basetemplate - is populated with the value of the base templatename for this type of request i.e. base-mobile.html '''
    def process_request(self, request):
        request.platform = detectAgent(request)
        return None
    
    
def detectAgent( request):
    if mobileBrowser( request):
        return 'mobile'
    else:
        return 'desktop'
    
    
# list of mobile User Agents
mobile_uas = [
    'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
    'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
    'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
    'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
    'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
    'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
    'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
    'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
    'wapr','webc','winw','winw','xda','xda-'
    ]
 
mobile_ua_hints = [ 'SymbianOS', 'Opera Mini', 'iPhone', 'Android' ]
 
def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''
 
    mobile_browser = False
    ua = request.META.get('HTTP_USER_AGENT', '').lower()[0:4]
 
    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True
 
    return mobile_browser