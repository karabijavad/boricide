from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
import urllib2
import simplejson
from boricide.models import *
import datetime
import dateutil
from pytz import timezone
import pytz
import sys, traceback
import sys, os
from urllib2 import HTTPError

class Command(BaseCommand):
    page = 0
    data_url = "http://api.ticketweb.com/snl/EventAPI.action?&version=1&method=json&resultsPerPage=50"
    utc_offsets = {'CDT': -5, 'EDT': -4, 'PDT': -7, 'CEST': 2, 'MDT': -6, 'ADT': -3,'MST': -7, 'EST': -5 , 'PST': -8, 'CST': -6}
    def handle(self, *args, **options):
      for i in range(100):
        this_page = self.data_url + "&page=" + str(i)

        try:
          handler = urllib2.urlopen(this_page)
        except HTTPError as e:
          print "error at " + this_page
          continue
        print "on page " + this_page
        events = simplejson.loads(handler.read())["events"]
        for event in events:
          door_price = event["prices"]["pricehigh"].replace("$","").replace(" ","").replace(",", "").replace("CAD","")
          if not  door_price:
            door_price = "0"
          try:
            new_concert, new_concert_created = Concert.objects.get_or_create(
              name            = event.get("eventname", ""),
              description   = event.get("description", ""),
              start_time    = pytz.timezone('UTC').localize(dateutil.parser.parse(event["dates"]["startdate"]) - datetime.timedelta(hours=self.utc_offsets[event["dates"]["timezone"]])),
              end_time      = pytz.timezone('UTC').localize(dateutil.parser.parse(event["dates"]["enddate"]) - datetime.timedelta(hours=self.utc_offsets[event["dates"]["timezone"]])),
              door_price    = door_price,
              venue = Venue.objects.get_or_create(
                name     = event["venue"]["name"],
                defaults = {
                  "address": event["venue"]["address"] + ", " + event["venue"]["city"] + ", " + event["venue"]["state"],
                }
              )[0]
            )

            for artist in event["attractionList"]:
             new_concert.artists.add(Artist.objects.get_or_create(name=artist["artist"])[0])
          except Exception as e:
            print event["venue"]["name"]
            print event["venue"]["address"] + ", " + event["venue"]["city"] + ", " + event["venue"]["state"]
            print str(e)

