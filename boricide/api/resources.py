from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields, utils
from boricide.models import Event, Artist, Venue, Concert
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication

class EventResource(ModelResource):
    def dehydrate_start_time(self, bundle):
        return bundle.obj.start_time.isoformat()
    def dehydrate_end_time(self, bundle):
        return bundle.obj.end_time.isoformat()
    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        queryset = Event.objects.all()
        resource_name = 'event'
        always_return_data = True

class ArtistResource(ModelResource):
    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        queryset = Artist.objects.all()
        resource_name = 'artist'
        always_return_data = True

class VenueResource(ModelResource):
    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        queryset = Venue.objects.all()
        resource_name = 'venue'
        always_return_data = True

class ConcertResource(EventResource):
    artists = fields.ToManyField(ArtistResource, 'artists', full=True)
    venue   = fields.ToOneField(VenueResource, 'venue', full=True)
    class Meta:
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        queryset = Concert.objects.all()
        resource_name = 'concert'
        always_return_data = True
        filtering = {
            'start_time': ALL,
            'end_time': ALL
        }