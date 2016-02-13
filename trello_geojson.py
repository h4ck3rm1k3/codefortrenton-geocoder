#!/usr/bin/python

import sys
import json
import re
sys.path.append('../py-trello')
from trello import TrelloClient

sys.path.append('../python-geojson')

#import cartodb



import secrets

client = TrelloClient(
    api_key=secrets.trello_key,
    api_secret=secrets.trello_secret,
    token=secrets.trello_oauth_token,
    token_secret= secrets.trello_oauth_token_secret,
)
# https://github.com/opencagedata/python-opencage-geocoder

import pprint
import geojson

import geojson
#crs = geojson.crs.Named("urn:ogc:def:crs:OGC:1.3:CRS84")

points = []

for b in client.list_boards():
    #print b
    for l in b.all_lists():
        for c in l.list_cards():

            comments = c.get_comments()
            done = False
            done2 = False
            c.fetch()
            desc = c.description
            url = c.short_url
            
            for cmt in comments :
                #pprint.pprint(cmt)
                txt = cmt['data']['text']
                if txt.startswith('GeoCode: '):
                    j = txt[9:]
                    if j == 'Failed':
                        #continue
                        pass
                    else:
                        #print ("gc:"+j)
                        d = eval(j)
                        good = False
                        for l in d:
                            if 'geometry' in l:
                                if 'components' in l:
                                    if 'city' in l['components']:
                                        city = l['components']['city']
                                        if city != 'Trenton':
                                            print ("Skipping"+ city)                                            
                                        else:
                                        #pprint.pprint(l)
                                            good = True                                                
                                    else:
                                        pass
                                        #print ('no city')
                                        #pprint.pprint(l['components'])
                                else:
                                    #print ('no components')
                                    #pprint.pprint(l)
                                    pass
                                            
                                lat = l[u'geometry']['lat']
                                lng = l[u'geometry']['lng']
                                #print ()
                                p = geojson.Point((lng,lat))
                                f = geojson.Feature(
                                    geometry=p,
                                    properties={
                                        "short_url": url,
                                        "description": desc
                                    }
                                )
                                #print p
                                if good:
                                    points.append(f)
                                break
                                #print ("To carto", c)
                            else:
                                #pprint.pprint(l)
                                pass
                            
                else:
                    #print ("skip:"+txt)
                    pass
c =  str(geojson.FeatureCollection(points))
o = open('snow.geojson','w')
o.write(c)
o.close()
