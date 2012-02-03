import requests
import json
import time
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from feeds.models import Story


class Command(BaseCommand):

    def save_storify_story(self, story):
        pubdatestring = story['date']['published']
        timestamp = time.strptime(pubdatestring[:19], '%Y-%m-%dT%H:%M:%S')
        pubdate = datetime.fromtimestamp(time.mktime(timestamp))
        new_story = Story.objects.create(key = story['sid'], title = story['title'], published = pubdate,
                                         description = story['description'], source = "Storify", permalink = story['permalink'],
                                         thumbnail = story['thumbnail'], views = story['stats']['views'],
                                         latest=True)
        new_story.save()


    def check_for_updates(self, story, existing_story):
        if story['stats']['views'] != existing_story.views:
            self.save_storify_story(story)
            existing_story.latest = False
            existing_story.save()
        if story['title'] != existing_story.title:
            self.save_storify_story(story)
            existing_story.latest = False
            existing_story.save()
        if story['thumbnail'] != existing_story.thumbnail:
            self.save_storify_story(story)
            existing_story.latest = False
            existing_story.save()



    def fetch_from_storify(self):
        """Connect to the Storify API, retrieve popular stories, and store."""
        r = requests.get('http://api.storify.com/v1/stories/browse/popular?per_page=%d' % settings.STORIES_PER_FEED)
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
        r = requests.get('http://tracking.tweetminster.co.uk/partner/api/metrics.json?channel=4e6decbf209fcbaf8e34eaf6&interval=daily&metric=links&limit=%d' % settings.STORIES_PER_FEED)

        if r.status_code != 200:
            raise CommandError('Tweetminster API returned a %d status code' % r.status_code)

        stories = json.loads(r.text, encoding='latin-1')['links']

        if len(stories) == 0:
            raise CommandError("Tweetminster API didn't return any results")

        for story in stories:
            try:
                existing_story = Story.objects.get(key = story['_id'], latest = True)
            except Story.DoesNotExist:
                self.save_tweetminster_story(story)

    def save_tweetminster_story(self, story):
        try:
            thumbnail =  story['embed'][0]['thumbnail_url']
        except KeyError:
            thumbnail = ''
        print thumbnail

        new_story = Story.objects.create(key = story['_id'], title = story['title'],
                                         description = story['description'], source = "Tweetminster", permalink = story['uri'],
                                         latest=True, thumbnail=thumbnail)
        new_story.save()


    def fetch_from_content_api(self):
        """Connect to the content API, retrieve popular stories, and store."""
        r = requests.get('http://content.guardianapis.com/search?tag=sport&page-size=50&format=json&show-fields=trailText&show-media=picture&api-key=techdev-internal')

        if r.status_code != 200:
            raise CommandError('content API returned a %d status code' % r.status_code)

        stories = json.loads(r.text)['response']['results']

        if len(stories) == 0:
            raise CommandError("content API didn't return any results")

        self.find_ten_with_images(stories)

    def find_ten_with_images(self, stories):
        withimages = []
        for story in stories:
            images = story['mediaAssets']
            hasImage = False
            for image in images:
                if image['fields']['width'] == '460':
                    hasImage = True
            if hasImage:
                withimages.append(story)



        for story in withimages[:10]:
            try:
                existing_story = Story.objects.get(key = story['id'], latest = True, source='ContentAPI')
            except Story.DoesNotExist:
                self.save_content_api_story(story)


    def save_content_api_story(self, story):
        images = story['mediaAssets']
        bigpicture = None
        for image in images:
            if image['fields']['width'] == '460':
                bigpicture = image

        new_story = Story.objects.create(key = story['id'], title = story['webTitle'],
                                         description = story['fields']['trailText'], source = "ContentAPI", permalink = story['webUrl'],
                                         latest=True, thumbnail=bigpicture['file'])
        new_story.save()


    def handle(self, *args, **options):
        self.fetch_from_storify()
        self.fetch_from_tweetminster()
        self.fetch_from_content_api()

