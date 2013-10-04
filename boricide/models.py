from django.db import models
from django.contrib.auth.models import User
from tastypie.models import create_api_key
from pygeocoder import Geocoder

models.signals.post_save.connect(create_api_key, sender=User)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    lat = models.DecimalField(max_digits=20, decimal_places=10, blank=True)
    lng = models.DecimalField(max_digits=20, decimal_places=10, blank=True)

    def save(self, *args, **kwargs):
        #user didnt provide coords so...
        if not self.lat and not self.lng:
            try:
                #...try geocoding the address...
                self.lat, self.lng = Geocoder.geocode(self.address).coordinates
            except:
                #...address couldnt be geocoding, bail out (dont save model)
                return
        super(Venue, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    venue = models.ForeignKey(Venue)
    door_price = models.DecimalField(max_digits=5, decimal_places=2)
    advance_price = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.advance_price:
            self.advance_price = self.door_price
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Concert(Event):
    artists = models.ManyToManyField(Artist)
    def __unicode__(self):
        return self.name

class UserPref(models.Model):
    user = models.OneToOneField(User)
    ArtistsStarred = models.ManyToManyField(Artist, blank=True)
    ConcertsStarred = models.ManyToManyField(Concert, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()
