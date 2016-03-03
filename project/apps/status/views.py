"""Views."""

from django.shortcuts import render
from django.conf import settings
import utils
import aftership


def index(request):
    """Index."""
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


@utils.json_response
def checkpoints(request, carrier_slug, tracking_number):
    """Checkpoints."""
    api = aftership.APIv4(getattr(settings, "AFTERSHIP_API_KEY", None))
    checkpoints = []
    raw_tracking = api.trackings.get(
        carrier_slug,
        tracking_number,
        fields=['title',
                'checkpoints',
                'expected_delivery',
                'delivery_time',
                'active'])

    response = raw_tracking['tracking']

    for checkpoint in response['checkpoints']:
            del checkpoint['created_at']
            del checkpoint['slug']
            del checkpoint['city']
            del checkpoint['zip']
            del checkpoint['country_name']
            checkpoint['checkpoint_time'] = \
                checkpoint['checkpoint_time'].strftime("%s")
            checkpoints.append(checkpoint)

    response['checkpoints'] = checkpoints
    # response['expected_delivery'] = \
    #     response['expected_delivery'].strftime("%s")

    # import pprint
    # # pprint.pprint(raw_tracking['tracking']['checkpoints'])
    # pprint.pprint(checkpoints)

    return response
    # return {'this will be': 'JSON',
    #         'carrier_slug': carrier_slug,
    #         'tracking_number': tracking_number}
