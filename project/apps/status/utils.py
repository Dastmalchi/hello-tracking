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


def get_carrier_name(s):
    """Return carrier name from slug."""
    matrix = {
        "dhl-global-mail": "DHL eCommerce",
        "usps": "USPS",
        "fedex": "FedEx",
        "canada-post": "Canada Post",
        "purolator": "Purolator",
        "tnt-reference": "TNT Reference",
        "tnt": "TNT",
        "uk-mail": "UK Mail",
        "hermes": "Hermesworld",
        "tnt-uk-reference": "TNT UK Reference",
        "tnt-uk": "TNT UK",
        "royal-mail": "Royal Mail",
        "myhermes-uk": "myHermes UK",
        "new-zealand-post": "New Zealand Post",
        "australia-post": "Australia Post",
    }
    return matrix[s]
