from django.conf.urls import patterns, include, url
from django.contrib import admin
from boricide.models import Artist, Venue, Concert, UserPref, Event
from tastypie.api import Api
from boricide.api.resources import ArtistResource, VenueResource, ConcertResource, EventResource
from boricide.scrape import emptybottle

v1_api = Api(api_name='v1')
v1_api.register(ArtistResource())
v1_api.register(VenueResource())
v1_api.register(ConcertResource())
v1_api.register(EventResource())

admin.autodiscover()
admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(Concert)
admin.site.register(Event)
admin.site.register(UserPref)

urlpatterns = patterns('',
    (r'^admin/',  include(admin.site.urls)),
    (r'^api/',    include(v1_api.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^scrape/emptybottle/', emptybottle.scrape)
)
