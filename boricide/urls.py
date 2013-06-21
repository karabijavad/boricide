from django.conf.urls import patterns, include, url
from django.contrib import admin
from boricide.models import Artist, Venue, Concert
from tastypie.api import Api

v1_api = Api(api_name='v1')

admin.autodiscover()
admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(Concert)

urlpatterns = patterns('',
    (r'^admin/',  include(admin.site.urls)),
)
