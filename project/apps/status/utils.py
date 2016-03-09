"""Utils."""

from django.http import HttpResponse
try:
    from django.utils import json
except:
    import json as json


def json_response(func):
    """json_response.

    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.GET:
                # a jsonp response!
                data = '%s(%s);' % (request.GET['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator


def format_date_for_display(s):
    """Format datetime as string for display."""
    return s.strftime("%b %d, %I:%M %p")
