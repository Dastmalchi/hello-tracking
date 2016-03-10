"""Views."""

from django.shortcuts import render
from django.conf import settings

import utils
import datetime
import aftership


# TODOs
# Carrier display name


def index(request):
    """Index."""
    return render(request, 'index.html')


@utils.json_response
def trackings(request, carrier_slug, tracking_number):
    """Checkpoints."""
    api = aftership.APIv4(getattr(settings, "AFTERSHIP_API_KEY", None))
    checkpoints = []
    try:
        raw_tracking = api.trackings.get(
            carrier_slug,
            tracking_number,
            fields=['title',
                    'checkpoints',
                    'expected_delivery',
                    'delivery_time',
                    'active',
                    'shipment_pickup_date',
                    'shipment_delivery_date',
                    'shipment_type',
                    'destination_country_iso3',
                    'destination_country_iso3',
                    'created_at',
                    'tag'])
        response = raw_tracking['tracking']
    except aftership.APIv4RequestException, e:
        print e
        # Create dummy response
        response = {
            'checkpoints': [{
                'checkpoint_time': datetime.datetime.now(),
                'coordinates': '',
                'country_iso3': '',
                'location': 'CA, USA',
                'message': 'Tracking number not found. Please try back later.',
                'state': '',
                'tag': 'Exception',
            }],
            'shipment_pickup_date': None,
            'shipment_delivery_date': None,
            'expected_delivery': None,
            'created_at': None,
            'destination_country_iso3': None,
            'tag': 'Exception',
        }

    # Process checkpoints
    for checkpoint in response['checkpoints']:
            try:
                del checkpoint['created_at']
                del checkpoint['slug']
                del checkpoint['city']
                del checkpoint['zip']
                del checkpoint['country_name']
                del checkpoint['coordinates']
            except Exception, e:
                pass
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

    # Fix shipment_delivery_date
    if response['shipment_delivery_date'] is not None:
        response['shipment_delivery_date'] = \
            datetime.datetime.strptime(response['shipment_delivery_date'],
                                       '%Y-%m-%dT%H:%M:%S')

    # Guess the expected delivery for dhl-global-mail
    # when it isn't defined and we have shipment_pickup_date
    if carrier_slug == 'dhl-global-mail' and \
            response['shipment_pickup_date'] is not None and \
            response['expected_delivery'] is None and \
            response['shipment_delivery_date'] is None:
        if response['destination_country_iso3'] == 'USA':
            # USA is 7 days
            response['expected_delivery'] = response['shipment_pickup_date'] \
                + datetime.timedelta(days=7)
        else:
            # International is 24 days
            response['expected_delivery'] = response['shipment_pickup_date'] \
                + datetime.timedelta(days=24)

    # Override expected_delivery when shipment_delivery_date available
    if response['shipment_delivery_date'] is not None:
        response['expected_delivery'] = response['shipment_delivery_date']

    # Format expected_delivery for display
    if response['expected_delivery'] is not None:
        response['expected_delivery'] = {
            'dow': response['expected_delivery'].strftime("%A"),
            'mon': response['expected_delivery'].strftime("%b"),
            'day': response['expected_delivery'].strftime("%d")
        }

    # Format created_at for display
    if response['created_at'] is not None:
        response['created_at'] = utils.format_date_for_display(
            response['created_at'])

    # Handle no checkpoints
    if len(response['checkpoints']) is 0:
        response['checkpoints'].append({
            'checkpoint_time': response['created_at'],
            'coordinates': '',
            'country_iso3': '',
            'location': 'CA, USA',
            'message': 'Tracking Pending. Please try back later.',
            'state': '',
            'tag': 'Pending',
        })

    response['carrier'] = utils.get_carrier_name(carrier_slug)

    # Cleanup response
    del response['shipment_pickup_date']
    del response['destination_country_iso3']
    del response['shipment_delivery_date']

    return response
