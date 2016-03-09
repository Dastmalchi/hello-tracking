"""Views."""

from django.shortcuts import render
from django.conf import settings

import utils
from datetime import datetime
import aftership


def index(request):
    """Index."""
    return render(request, 'index.html')


@utils.json_response
def trackings(request, carrier_slug, tracking_number):
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
                'active',
                'shipment_pickup_date',
                'shipment_type',
                'tag'])

    response = raw_tracking['tracking']

    for checkpoint in response['checkpoints']:
            del checkpoint['created_at']
            del checkpoint['slug']
            del checkpoint['city']
            del checkpoint['zip']
            del checkpoint['country_name']
            checkpoint['checkpoint_time'] = \
                checkpoint['checkpoint_time'].strftime("%b %d, %I:%M %p")
            checkpoints.append(checkpoint)

    checkpoints.reverse()
    response['checkpoints'] = checkpoints

    if response['expected_delivery'] is not None:
        response['expected_delivery'] = {
            'dow': response['expected_delivery'].strftime("%A"),
            'mon': response['expected_delivery'].strftime("%b"),
            'day': response['expected_delivery'].strftime("%d")
        }

    response['shipment_pickup_date'] = \
        datetime.strptime(response['shipment_pickup_date'],
                          '%Y-%m-%dT%H:%M:%S')
    response['shipment_pickup_date'] = \
        response['shipment_pickup_date'].strftime("%b %d, %I:%M %p")

    return response
