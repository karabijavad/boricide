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
import re

class Command(BaseCommand):
    pageNum = 0
    maxResults = 200
    data_url = "http://www.ticketfly.com/api/events/upcoming.json?orgId=1"
    
    def handle(self, *args, **options):
      while True:
        print "on page " + str(self.pageNum)
        this_page = self.data_url + "&pageNum=" + str(self.pageNum) + "&maxResults=" + str(self.maxResults)
        data = simplejson.loads(urllib2.urlopen(this_page).read())
        if self.pageNum > data["totalPages"]:
          print "hit last page, stopping"
          break

        events = data["events"]
        for event in events:
          if not event["endDate"]:
            print "No end date, skipping show: " + event["name"]
            continue
          if event["ticketPrice"] == "FREE" or "No cover":
            event["ticketPrice"] = "0"

          try:
              this_venue,created       = Venue.objects.get_or_create(
                name = event["venue"]["name"],
                defaults = {
                  "address": event["venue"]["address1"] + ", " + event["venue"]["city"] + ", " + event["venue"]["stateProvince"]
                }
              )
          except Exception as e:
            print "Exception: " + str(e)
            continue

          if created:
            print "Created new venue: " + event["venue"]["name"] + ", " + event["venue"]["address1"] + ", " + event["venue"]["city"] + ", " + event["venue"]["stateProvince"]

          try:
            this_concert = Concert.objects.get_or_create(
              name        = event["name"],
              start_time  = timezone(event["org"]["timeZone"]).localize(dateutil.parser.parse(event["startDate"])),
              end_time    = timezone(event["org"]["timeZone"]).localize(dateutil.parser.parse(event["endDate"])),
              door_price  = re.sub('-.*' ,'', event["ticketPrice"].replace("$","")),
              venue       = this_venue
            )[0]
          except:
            traceback.print_exc(file=sys.stdout)
            continue
            #sys.exit()

          for artist in event["headliners"]:
            this_concert.artists.add(
              Artist.objects.get_or_create(
                name = artist["name"],
                defaults = {
                  "description": artist.get("description", "")
                }
              )[0]
            )
        self.pageNum += 1

