from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
import urllib2
import json
from boricide.models import *
import dateutil
from pytz import timezone
import sys
import traceback
import re


class Command(BaseCommand):
    pageNum = 0
    maxResults = 200
    data_url = "http://www.ticketfly.com/api/events/upcoming.json?orgId=1"

    def handle(self, *args, **options):
        while True:
            print "on page " + str(self.pageNum)
            this_page = self.data_url + "&pageNum=" + \
                str(self.pageNum) + "&maxResults=" + str(self.maxResults)
            data = json.loads(urllib2.urlopen(this_page).read())
            if self.pageNum > data["totalPages"]:
                print "hit last page, stopping"
                break

            for event in data["events"]:
                if not event["endDate"]:
                    endDate = timezone(event["org"]["timeZone"]).localize(
                        dateutil.parser.parse(event["startDate"]))
                    print "No end date, skipping show: " + event["name"]
                    continue
                if event["ticketPrice"] == "FREE" or "No cover":
                    event["ticketPrice"] = "0"

                try:
                    this_venue, created = Venue.objects.get_or_create(
                        name=event["venue"]["name"],
                        defaults={
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
                        name=event["name"],
                        start_time=timezone(event["org"]["timeZone"]).localize(
                            dateutil.parser.parse(event["startDate"])),
                        end_time=timezone(event["org"]["timeZone"]).localize(
                            dateutil.parser.parse(event["endDate"])),
                        door_price=re.sub(
                            '-.*', '', event["ticketPrice"].replace("$", "")),
                        venue=this_venue
                    )[0]
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue
                    # sys.exit()

                for artist in event["headliners"]:
                    this_concert.artists.add(
                        Artist.objects.get_or_create(
                            name=artist["name"],
                            defaults={
                                "description": artist.get("description", "")
                            }
                        )[0]
                    )
            self.pageNum += 1
