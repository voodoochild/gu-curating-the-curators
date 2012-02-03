import json
import random
from django.http import HttpResponse
from django.conf import settings
from feeds.models import Story

def storify_dummy_data(request):
    """Returns shuffled JSON data for Storify."""
    storyjson = []
    stories = Story.objects.filter(latest=True, source='Storify')[:settings.STORIES_PER_FEED]

    for story in stories:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink,
        },)

    random.shuffle(storyjson)

    data = {
        'stories': storyjson
    }
    return HttpResponse(json.dumps(data, encoding='utf-8'),
                        content_type='application/json; charset=utf-8')


def tweetminster_dummy_data(request):
    storyjson = []
    stories = Story.objects.filter(latest=True, source='Tweetminster')[:settings.STORIES_PER_FEED]

    for story in stories:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink,
        },)

    random.shuffle(storyjson)
    data = {
        'stories': storyjson
    }
    return HttpResponse(json.dumps(data, encoding='utf-8'),
                        content_type='application/json; charset=utf-8')


def contentapi_dummy_data(request):
    storyjson = []
    stories = Story.objects.filter(latest=True, source='ContentAPI')[:settings.STORIES_PER_FEED]

    for story in stories:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink,
        },)

    random.shuffle(storyjson)
    data = {
        'stories': storyjson
    }
    return HttpResponse(json.dumps(data, encoding='utf-8'),
                        content_type='application/json; charset=utf-8')
