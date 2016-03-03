"""Views."""

from django.shortcuts import render
from django.conf import settings

import utils
import aftership


# TODOs
# Add shipment_pickup_date
# Add shipment_type
# Add tag to get current status
# Get list of possible trackings for final status
# Map Shopify carriers to Aftership carriers in JS
# Sanitize request.GET in template

def index(request):
    """Index."""
    # import pdb
    # pdb.set_trace()
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

    if response['expected_delivery'] is not None:
        response['expected_delivery'] = \
            response['expected_delivery'].strftime("%s")

    return response
