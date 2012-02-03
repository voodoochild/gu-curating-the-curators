import datetime
from time import mktime
import requests
import json
import time
from django.core.management.base import BaseCommand, CommandError
from feeds.models import Story


class Command(BaseCommand):

    def save_storify_story(self, story):
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
            self.save_storify_story(story)
            print '[%s] views changed from %d to %d' % (story['sid'], existing_story.views, story['stats']['views'])
            existing_story.latest = False
            existing_story.save()
        if story['title'] != existing_story.title:
            self.save_storify_story(story)
            print '[%s] title changed' % story['sid']
            existing_story.latest = False
            existing_story.save()
        if story['thumbnail'] != existing_story.thumbnail:
            self.save_storify_story(story)
            print '[%s] thumbnail changed' % story['sid']
            existing_story.latest = False
            existing_story.save()



    def fetch_from_storify(self):
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
                existing_story = Story.objects.get(key = story['sid'], latest = True)
                self.check_for_updates(story, existing_story)
            except Story.DoesNotExist:
                self.save_storify_story(story)

    def fetch_from_tweetminster(self):
        """Connect to the Storify API, retrieve popular stories, and store."""
        r = requests.get('http://tracking.tweetminster.co.uk/partner/api/metrics.json?channel=4e6decbf209fcbaf8e34eaf6&interval=daily&metric=links&limit=10')

        if r.status_code != 200:
            raise CommandError('Tweetminster API returned a %d status code' % r.status_code)

        #ustr_to_load = unicode(r.text, 'latin-1')
        #foo = r.text.encode('latin-1')
        stories = json.loads(r.text, encoding = 'latin-1')['links']

        print stories

        if len(stories) == 0:
            raise CommandError("Tweetminster API didn't return any results")

        for story in stories:
            try:
                existing_story = Story.objects.get(key = story['_id'], latest = True)
                self.check_for_updates(story, existing_story)
            except Story.DoesNotExist:
                self.save_tweetminster_story(story)

    def save_tweetminster_story(self, story):
        print story['domain']
        new_story = Story.objects.create(key = story['_id'], title = story['title'],
                                         description = story['description'], source = "Tweetminster", permalink = story['uri'],
                                         latest=True)
        new_story.save()



    def handle(self, *args, **options):
        self.fetch_from_storify()
        self.fetch_from_tweetminster()

