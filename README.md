# codefortrenton-geocoder

## Create the indexes

    mongo code_for_trenton
    db.addresses.ensureIndex( { Name :1 }, { unique:true, dropDups:true})
    db.addresses.createIndex( { Name: 1 }, { unique: true } )

## Keys

secrets.py contains

    opencage_key = 'XXXX'

create it here https://geocoder.opencagedata.com/

## need libs

Using pymongodb

and MongoDB version: 2.4.14

Locally checked out python-opencage-geocoder

    git clone git@github.com:OpenCageData/python-opencage-geocoder.git


## Data is from fusion table to start with 

    https://www.google.com/fusiontables/exporttable?query=select+*+from+1L7eDqaZi9F5ZszM_URjC7k48mKLTZen1iWdChHon&o=csv

For shell access to this, see : https://fusion-tables-api-samples.googlecode.com/svn/trunk/ftapi/README.html


# Export

    mongoexport -d code_for_trenton -c addresses > addresses.json
    bzip2 addresses.json 


# Geocoding of google voice transcriptions :

1. using google voice to email trello
you need to get the trello email http://blog.trello.com/create-cards-via-email/
then in google you add that email as an alternative email for your account.
You will get a confirmation email as a ticket that you need to confirm.

2. trello as ticket storage
Then in google voice you have the email notications send to that email. Also
turn on do not disturb. 

3. using nltk to parse out text.
Setup nltk python http://www.nltk.org/ for parsing the text of the transcriptions

4. using opencage for geocoding

Setup of opencage :
https://geocoder.opencagedata.com/

get the private key.

using this lib:
https://github.com/opencagedata/python-opencage-geocoder

5. storing of geocode in ticket

get the trello api key.
Using github.com/sarumont/py-trello for the trello api. See secrets.py for some
tips on setting up the keys. 

The script that does this is : trello_geocode.py
it runs on a cron job every x minutes on linux.

    */2 * * * *  bash ~/experiments/codefortrenton/cron.sh

That calls into ~/experiments/codefortrenton/cron.sh

    cd ~/experiments/codefortrenton/
    python ./trello_geocode.py


All tickets that are not marked with a GeoCode will be marked.

6. Creating of the geojson
trello_geojson.py produces a geojson file, this is then copied into the webpage
branch. This is not automated yet.

I filter out all geocodes not in the city of trenton.

7. setup of trello connection to slac.


## TODO :

1. setup a way for people to subscribe to tickets based on an area
2. setup publishing geojson on new tickets.
3. setup a shell account for running the script (or do this on a website, but
   we will need a cron job)
