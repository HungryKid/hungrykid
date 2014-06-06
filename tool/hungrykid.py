# google place crawler
import urllib2
import json

apiurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
parameter = 'location=35.6571942,139.7093825&radius=300&types=food&sensor=false&rankby=prominence&'
key = 'xxx' # insert google api key here

response = urllib2.urlopen(apiurl+parameter+key)
jsonplace = json.loads(response.read())
jsonlist = jsonplace['results']

for l in jsonlist:
    keys = l.keys()
    for k in keys:
        if k == 'name':
            print l[k]
