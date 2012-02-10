#!/usr/bin/env python
from google.appengine.ext import db


class StorifySnapshots(db.Model):
    hashtag = db.StringProperty(default='default')
    ordinal = db.IntegerProperty(default=0)
    json = db.TextProperty(default='')
    backfilled = db.IntegerProperty(default=0)
    last_update = db.DateTimeProperty(auto_now_add=True, required=True)
