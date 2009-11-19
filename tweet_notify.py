#!/usr/bin/env python

from httplib import HTTPConnection
from base64 import encodestring
import boto
from json import loads
import Growl as growl
import urllib

notifier = growl.GrowlNotifier("Twitter Update", [""])
notifier.register()

sdb = boto.connect_sdb(AWS_KEY, AWS_SECRET)
domain = sdb.create_domain("twitter")

b64string = encodestring("%s:%s" % (username, password))
conn = HTTPConnection("twitter.com")
conn.request("GET", "/statuses/friends_timeline.json", "", {"Authorization": \
    "Basic %s" % b64string})
tweets = loads(conn.getresponse().read())
for tweet in tweets:
  exists = domain.get_item(tweet['id'])
  if not exists:
    item = domain.new_item(tweet['id'])
    item['user_id'] = tweet['user']['id']
    item['source'] = tweet['source']
    item['text'] = tweet['text']
    item['created_at'] = tweet['created_at']
    item['screen_name'] = tweet['user']['screen_name']
    item.save()
    image_data = urllib.urlopen(tweet['user']['profile_image_url']).read()
    icon = growl.Image.imageWithData(image_data)
    notifier.notify(noteType = "", title = item['screen_name'], description = \
        item['text'], icon = icon)
