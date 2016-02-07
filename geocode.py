#!/usr/bin/env python
import sys
import pprint

# https://github.com/opencagedata/python-opencage-geocoder
sys.path.append('./python-opencage-geocoder/')
import opencage
import opencage.geocoder
import csv

#from opencage.geocoder import OpenCageGeocoder
from secrets import opencage_key
geocoder = opencage.geocoder.OpenCageGeocode(opencage_key)

fn = 'trenton-data-set-2015.csv'
#of = open(fn, 'wb'):

import pymongo
client = pymongo.MongoClient('mongodb://admin:password@127.0.0.1')
db = client.code_for_trenton
data = db.addresses

alld = {}
for c in data.find({}):
    name = c['Name']
    alld[name]=c
    print "name", name

    
with open(fn, 'rb') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',', quotechar='"' ) # fieldnames=fieldnames
    for c in reader:
        name = c['Name']
        # unicode
        name = unicode(name, 'utf-8')
        
        if name not in alld:
            print "Adding",name
            alld[name]=c
            data.insert(c)
        


for n in alld:
    x = alld[n]
    if (x['Street']):
        if len(x['Zip Exten']) > 0:
            addr= x['Street'] +"\n" + x['City'] + " " + x['State'] + "  "+ x['Zip'] + "-" + x['Zip Exten'] + ", USA"
        else:
            addr= x['Street'] +"\n" + x['City'] + " " + x['State'] + " "+ x['Zip']  + ", USA"



    u = False
    if 'GeoCode' not in x:
        gc = geocoder.geocode(addr)
        x['GeoCode']=gc
        u = True
            
    #print addr
    if x['Full Address']!=addr:
        x['Full Address']=addr
        u = True

    if u:
        print "Updating" + x['Name']
        data.update(
            {
                'Name' : x['Name']
            },
            x,
            upsert=True            
        )
    else:
        print "Already done" + x['Name']        
        #pprint.pprint(x)
        #exit(0)
    
    
    #exit(0)
    
