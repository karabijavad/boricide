from django.conf.urls import patterns, include, url
from django.contrib import admin
from boricide.models import Artist, Venue, Concert
from tastypie.api import Api
from boricide.api.resources import ArtistResource, VenueResource, ConcertResource

v1_api = Api(api_name='v1')
v1_api.register(ArtistResource())
v1_api.register(VenueResource())
v1_api.register(ConcertResource())

admin.autodiscover()
admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(Concert)

urlpatterns = patterns('',
    (r'^admin/',  include(admin.site.urls)),
    (r'^api/',    include(v1_api.urls)),
)
