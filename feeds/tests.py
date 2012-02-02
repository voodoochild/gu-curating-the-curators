"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase
from feeds.models import Story


class SimpleTest(TestCase):
    def test_store_story(self):

        story = Story.objects.create(title="foo", published = datetime.datetime(2012,02,02,12,12), description = "This is a description of a story", source = "twitter", permalink = "http://www.linktostory.com", views = 14030)
        story.save()

        saved = Story.objects.get(title="foo")
        self.assertEqual(saved.title, "foo")
        self.assertEqual(saved.published, datetime.datetime(2012,02,02,12,12))
        self.assertEqual(saved.description, "This is a description of a story")
        self.assertEqual(saved.source, "twitter")
        self.assertEqual(saved.permalink, "http://www.linktostory.com")
        self.assertEqual(saved.views, 14030)

