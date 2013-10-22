from django.core.management.base import BaseCommand, CommandError
import urllib2
import simplejson
from boricide.models import *
import datetime
import dateutil

class Command(BaseCommand):

    def handle(self, *args, **options):
      Artist.objects.all().delete()
      Concert.objects.all().delete()
      Event.objects.all().delete()

