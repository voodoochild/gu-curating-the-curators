from django.db import models

import datetime

class Story(models.Model):
    key = models.CharField(max_length = 255, db_index = True, unique = True)
    timestamp = models.DateTimeField(
        default = datetime.datetime.now, db_index = True
    )
    published = models.DateTimeField(null=True)
    title = models.CharField(blank=True, max_length=255, default="")
    description = models.TextField()
    source = models.CharField(blank=True, max_length=255, default="")
    permalink = models.CharField(blank=True, max_length=255, default="")
    thumbnail = models.CharField(blank=True, max_length=255, default="")
    views = models.IntegerField(null=True)
    searchterm = models.CharField(blank=True, max_length=255, default="")
