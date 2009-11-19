#!/usr/bin/env python

from base64 import encodestring
from httplib import HTTPConnection
from json import loads
import urllib

from constants import *
import Growl as growl
import boto

LISTS = ['dwlz/news', 'dwlz/tech-cos']

notifier = growl.GrowlNotifier("Twitter Update", [""])
notifier.register()

sdb = boto.connect_sdb(AWS_KEY, AWS_SECRET)
domain = sdb.create_domain("twitter")

b64string = encodestring("%s:%s" % (TWITTER_USERNAME, TWITTER_PASSWORD))
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

for list in LISTS:
  username, list_name = list.split("/")
  conn.request("GET", "/1/%s/lists/%s/statuses.json" % (username, list_name), "", {})
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

