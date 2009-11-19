Growl Tweet Notifier
====================

Introduction
------------

This is a bare-bones Twitter notifier for OS X. Every minute, it will check for new tweets and will update via Growl. Maybe this could become even more useful with more command-line functionality, but I'm too <del>lazy</del> busy to write that right now.

Requirements
------------

- [Python 2.6](http://www.python.org/ftp/python/2.6.4/Python-2.6.4.tar.bz2)
- [Boto 1.8d](http://boto.googlecode.com/files/boto-1.8d.tar.gz)
- [Growl Developer Tools](http://growl.googlecode.com/files/Growl-1.2-SDK.dmg)
- [An Amazon Web Services account](http://aws.amazon.com/)
- [A Twitter account](http://www.twitter.com/) (obviously)

Instructions
------------

1. Set the constants `AWS_KEY`, `AWS_SECRET`, `TWITTER_USERNAME`, and `TWITTER_PASSWORD` so that they match up with your credentials.
2. Add this line to your crontab:

        * * * * * $HOME/tweet_notify.py

3. You're done!

