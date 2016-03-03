"""URLs."""

from django.conf.urls import include, url

from django.contrib import admin
import apps.status.views

admin.autodiscover()

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', apps.status.views.index, name='index'),
    url(r'^checkpoints/(?P<carrier_slug>[\w-]+)/(?P<tracking_number>[\w-]+)/$',
        apps.status.views.checkpoints),
    url(r'^admin/', include(admin.site.urls)),
]
