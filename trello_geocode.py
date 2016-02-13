#!/usr/bin/python
import secrets
import sys
sys.path.append('../py-trello')
from trello import TrelloClient
import re

client = TrelloClient(
    api_key=secrets.trello_key,
    api_secret=secrets.trello_secret,
    token=secrets.trello_oauth_token,
    token_secret= secrets.trello_oauth_token_secret,
)
# https://github.com/opencagedata/python-opencage-geocoder
sys.path.append('./python-opencage-geocoder/')
import opencage
import opencage.geocoder

from secrets import opencage_key
geocoder = opencage.geocoder.OpenCageGeocode(opencage_key)

import parse_sms
import pprint

for b in client.list_boards():
    #print b
    for l in b.all_lists():
        for c in l.list_cards():

            comments = c.get_comments()
            done = False
            
            for cmt in comments :
                #pprint.pprint(cmt)
                txt = cmt['data']['text']
                if 'GeoCode' in  txt:
                    done = True
                else:
                    #print ('Hmm' + txt)
                    pass                    
            #print
            if done :
                print ("Done", c)
            else:
                print ("Todo",c)

                g = re.search(r'Transcript:(.+)',c.description)
                if g:
                    x = g.group(1)
                    for y in parse_sms.process(x):
                        # now we geocode this
                        gc = geocoder.geocode(y)
                        gc2 = pprint.pformat(gc)
                        c.comment("Identified Address: " +  y)
                        c.comment("GeoCode: " +  gc2)
                        done = True
                if not done:
                        c.comment("GeoCode: Failed" )
