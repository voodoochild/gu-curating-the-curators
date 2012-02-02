import datetime
import requests
import json
from django.core.management.base import BaseCommand, CommandError
from feeds.models import Story


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Connect to the Storify API, retrieve popular stories, and store."""
        r = requests.get('http://api.storify.com/v1/stories/browse/popular?per_page=10')
        
        if r.status_code != 200:
            raise CommandError('Storify API returned a %d status code' % r.status_code)

        stories = json.loads(r.text)['content']['stories']

        if len(stories) == 0:
            raise CommandError("Storify API didn't return any results")

        for story in stories:
            #print story['title']
            """
            1. Check to see if we know about this already.
            """
            try:
                existing_story = Story.objects.get(key = story['sid'])
            except Story.DoesNotExist:
               # print "no story found"
                print story['sid']
                new_story = Story.objects.create(key = story['sid'], title = story['title'], published = datetime.datetime(2012,02,02,12,12),
                                                 description = story['description'], source = "Storify", permalink = story['permalink'],
                                                 thumbnail = story['thumbnail'], views = story['stats']['views'])
                new_story.save()







            """
            2. If we do, look to see if any of the fields have changed.

            3. If they have, create a new Story object.

            4. If this story wasn't in the DB already, create a new Story object.

            This is going to be HILARIOUSLY bad for the database, with anywhere
            up to 20 queries for every 10 stories we request from the API. For the
            love of all that is good and holy, refactor this to not be PURE EVIL.
            """
            pass
