# This version of the SimpleGoogleStreetView script addresses a bug in which
# Processing Python Mode on Windows cannot load files with the Python open()
# function. Thus, you can place your CSV locations into the 'data' variable
# in locationscsv.py instead.
#
# https://github.com/jdf/processing.py/issues/274
#
# Once the issue is resolved or a workaround found, this file will go away.

import csv

import urllib

import urllib2

import os

import sys

import goslate

from geopy.geocoders import Nominatim

import time

import pdb

import random

import datetime

from datetime import timedelta

# Put your Google Street View API key here.

api_key = ""

api_url = "https://maps.googleapis.com/maps/api/streetview?size=640x400&location={0},{1}&fov=90&heading={2}&pitch=10&key={3}"

script_dir = os.path.dirname(__file__)

proxies = []

proxy_file = script_dir + 'proxies.txt'

with open(proxy_file, 'rb') as text:

    content = text.readlines()

for proxy in content :

    proxy = proxy.replace('\n', '')

    proxies.append(proxy)


locations = []

geolocator = Nominatim(user_agent="google image app")

loc_path = script_dir + 'locationscsv.py'

with open(loc_path, 'rb') as text:

    content = text.readlines()

for row in content:

    proxy_handler = urllib2.ProxyHandler({"http" : "http://"+random.choice(proxies)})

    proxy_opener = urllib2.build_opener(urllib2.HTTPHandler(proxy_handler),
                                        urllib2.HTTPSHandler(proxy_handler))

    gs_with_proxy = goslate.Goslate(opener=proxy_opener)

    # row = gs_with_proxy.translate(row, "en")

    try:

        location = geolocator.geocode(row)

        geo_loc = (row.split('  ')[0], location.latitude, location.longitude)

        locations.append(geo_loc)

    except Exception as e:

        print e

        pass

row = 2

headings = [0, 90, 180, 270]

# Loop over every location, and for each location, loop over all the possible headings.

count = 1

for location in locations:

    for direction in headings:
        # Create the URL for the request to Google.
        addr, lat, lon = location

        url = api_url.format(lat, lon, direction, api_key)

        if row % 71  == 0:

            print "wait a minute, please !!!"

            # delay for 2~3 minutes
            time.sleep(150)

        # Create the filename we want to save as, e.g. location-2-90.jpg.
        filename = addr + "-{0}-{1}.jpg".format(count, direction)

        # Use the 'curl' command to actually make the request and save the file to disk.
        urllib.urlretrieve(url, filename)

        print "Got %s" % (filename,)

        # Increment the row to correlate with the Excel file.
        row += 1

    count += 1
    
print "Done"