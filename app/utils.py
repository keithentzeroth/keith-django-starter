from django.http import HttpResponseNotAllowed


def dispatch(**methods):
    """Calls a view by request.method value.

    To use this dispatcher write your urls.py like this:

    urlpatterns = pattern('',
        url(r'^foo/$', dispatch(head=callable1,
                                get=callable2,
                                delete=callable3)),
    )

    If request.method is equal to head, callable1 will be called as your usual view function;
    if it is "get", callable2 will be called; et cetera.
    If the method specified in request.method is not one handled by dispatch(..),
    HttpResponseNotAllowed is returned.
    """

    lc_methods = dict( (method.lower(), handler) for (method, handler) in methods.iteritems() )

    def __dispatch(request, *args, **kwargs):
        handler = lc_methods.get(request.method.lower())
        if handler:
            return handler(request, *args, **kwargs)
        else:
            return HttpResponseNotAllowed(m.upper() for m in lc_methods.keys())
    return __dispatch
