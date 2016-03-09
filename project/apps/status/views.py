"""Views."""

from django.shortcuts import render
from django.conf import settings

import utils
import datetime
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
                'destination_country_iso3',
                'created_at',
                'tag'])

    response = raw_tracking['tracking']

    # Process checkpoints
    for checkpoint in response['checkpoints']:
            del checkpoint['created_at']
            del checkpoint['slug']
            del checkpoint['city']
            del checkpoint['zip']
            del checkpoint['country_name']
            del checkpoint['coordinates']
            checkpoint['checkpoint_time'] = utils.format_date_for_display(
                checkpoint['checkpoint_time'])
            checkpoints.append(checkpoint)
    checkpoints.reverse()
    response['checkpoints'] = checkpoints

    # Fix shipment_pickup_date
    if response['shipment_pickup_date'] is not None:
        response['shipment_pickup_date'] = \
            datetime.datetime.strptime(response['shipment_pickup_date'],
                                       '%Y-%m-%dT%H:%M:%S')

    # Guess the expected delivery for dhl-global-mail
    # when it isn't defined and we have shipment_pickup_date
    if carrier_slug == 'dhl-global-mail' and \
            response['shipment_pickup_date'] is not None and \
            response['expected_delivery'] is None:
        if response['destination_country_iso3'] == 'USA':
            # USA is 7 days
            response['expected_delivery'] = response['shipment_pickup_date'] \
                + datetime.timedelta(days=7)
        else:
            # International is 24 days
            response['expected_delivery'] = response['shipment_pickup_date'] \
                + datetime.timedelta(days=24)

    # Format expected_delivery for display
    if response['expected_delivery'] is not None:
        response['expected_delivery'] = {
            'dow': response['expected_delivery'].strftime("%A"),
            'mon': response['expected_delivery'].strftime("%b"),
            'day': response['expected_delivery'].strftime("%d")
        }

    # Format created_at for display
    response['created_at'] = utils.format_date_for_display(
        response['created_at'])

    # Cleanup response
    del response['shipment_pickup_date']
    del response['destination_country_iso3']

    return response
