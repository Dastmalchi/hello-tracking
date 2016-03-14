# Hello Tracking - AfterShip/Shopify

## Summary

This app provides data from the AfterShip API as a JSONP response to be consumed by a front-end application on Shopify.

## Hosting

The application is written in Django and hosted on Heroku as `quiet-wave-63225`. Deploys are done manually from the `master` branch of `Dastmalchi/hello-tracking`.

### Configuration

* The AfterShip API key is set as and environment variable as `AFTERSHIP_API_KEY`. 
* Shopify carriers are manually mapped in the liquid templates for customer order details and email. At this time there isn't a better way to do this. This means that if a new Shopify carrier is added (or Shipwire is pushing new carriers into `tracking_company`) then additional mappings will need to be made anywhere the tracking link appears. If a carrier is missing, a fallback to Shopify's tracking URL is used. 
* The tracking page itself is added using the Shopify CMS and a custom page template. Both are included in `/shopify-samples`.
* Customization to the order details template and email notifications needs to be made to deploy. See the example in `customer.order.liquid`.


##  Notes

* Most of the application logic is in the Django view. This needs to be moved.
* All checkpoint data is returned and specific properties are popped off. This could be a problem if sensitive data is added to the response in the future. Only data that is needed should be returned.
* Dates from AfterShip's pip package were not consistent. i.e. Varying string format dates and some datetime.
* AfterShip just added estimated delivery for DHL eCommerce so our guessing method shouldn't be needed but it left as a fallback.
