from django.core.management.base import BaseCommand, CommandError
import urllib2
import simplejson
from boricide.models import *
import datetime
import dateutil
import iso8601
from pytz import timezone
import pytz

class Command(BaseCommand):
    eb_data = "http://api.ticketweb.com/snl/EventAPI.action?key=nnV81nDN29wo4yknB7dl&version=1&orgId=10461,125593,22241,10068,14084,27115,335395,10851&method=json"
    def handle(self, *args, **options):
      events = simplejson.loads(urllib2.urlopen(self.eb_data).read())["events"]
      datetime_format = "%Y%m%d%H%M%S%Z"
      for event in events:
        start_time = dateutil.parser.parse(event["dates"]["startdate"])
        end_time   = start_time.replace(hour=2, minute=0) + datetime.timedelta(days=1)
        if (event["dates"]["timezone"] is "CDT"):
          start_time = start_time.timedelta(hours=5)
          end_time   = end_time.timedelta(hours=5)
        new_concert = Concert.objects.get_or_create(name=event["eventname"],start_time=start_time, end_time=end_time, venue=Venue.objects.get_or_create(name=event["venue"]["name"]), door_price=event["prices"]["pricehigh"].replace("$", ""), description=event["description"])[0]
        for artist in event["attractionList"]:
          new_concert.artists.add(Artist.objects.get_or_create(name=artist["artist"])[0])

