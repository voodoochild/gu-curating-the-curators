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
        """
        Tests that 1 + 1 always equals 2.
        """
        story = Story.objects.create(title="foo", published = datetime.datetime(2012,02,02,12,12), )
        story.save()

        saved = Story.objects.get(title="foo")
        self.assertEqual(saved.title, "foo")
