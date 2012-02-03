import datetime
from time import mktime
import requests
import json
import time
from django.core.management.base import BaseCommand, CommandError
from feeds.models import Story


class Command(BaseCommand):

    def save_story(self, story):
        pubdatestring = story['date']['published']
        timestamp = time.strptime(pubdatestring[:19], '%Y-%m-%dT%H:%M:%S')
        pubdate = datetime.datetime.fromtimestamp(mktime(timestamp))
        new_story = Story.objects.create(key = story['sid'], title = story['title'], published = pubdate,
                                         description = story['description'], source = "Storify", permalink = story['permalink'],
                                         thumbnail = story['thumbnail'], views = story['stats']['views'],
                                         latest=True)
        new_story.save()


    def check_for_updates(self, story, existing_story):
        if story['stats']['views'] != existing_story.views:
            self.save_story(story)
            print '[%s] views changed from %d to %d' % (story['sid'], existing_story.views, story['stats']['views'])
            existing_story.latest = False
            existing_story.save()
        if story['title'] != existing_story.title:
            self.save_story(story)
            print '[%s] title changed' % story['sid']
            existing_story.latest = False
            existing_story.save()
        if story['thumbnail'] != existing_story.thumbnail:
            self.save_story(story)
            print '[%s] thumbnail changed' % story['sid']
            existing_story.latest = False
            existing_story.save()


    def handle(self, *args, **options):
        """Connect to the Storify API, retrieve popular stories, and store."""
        r = requests.get('http://api.storify.com/v1/stories/browse/popular?per_page=10')
        
        if r.status_code != 200:
            raise CommandError('Storify API returned a %d status code' % r.status_code)

        stories = json.loads(r.text)['content']['stories']

        if len(stories) == 0:
            raise CommandError("Storify API didn't return any results")

        """
        This is going to be HILARIOUSLY bad for the database, with anywhere
        up to 20 queries for every 10 stories we request from the API. For the
        love of all that is good and holy, refactor this to not be PURE EVIL.
        """
        for story in stories:
            try:
                existing_story = Story.objects.filter(key = story['sid']).order_by('-timestamp')[0]
                self.check_for_updates(story, existing_story)
            except IndexError:
                self.save_story(story)
