import json
import random
from django.http import HttpResponse
from django.conf import settings
from feeds.models import Story

def storify_dummy_data(request):
    """Returns shuffled JSON data for Storify."""
    storyjson = []
    stories = Story.objects.filter(latest=True, source='Storify').order_by('-timestamp')

    for story in stories[:settings.STORIES_PER_FEED]:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink,
        },)

    random.shuffle(storyjson)
    data = {'stories': storyjson}
    return HttpResponse(json.dumps(data, encoding='utf-8'),
                        content_type='application/json; charset=utf-8')


def tweetminster_dummy_data(request):
    storyjson = []
    stories = Story.objects.filter(latest=True, source='Tweetminster').order_by('-timestamp')

    for story in stories[:settings.STORIES_PER_FEED]:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink,
        },)

    random.shuffle(storyjson)
    data = {'stories': storyjson}
    return HttpResponse(json.dumps(data, encoding='utf-8'),
                        content_type='application/json; charset=utf-8')


def contentapi_dummy_data(request):
    storyjson = []
    stories = Story.objects.filter(latest=True, source='ContentAPI').order_by('-timestamp')

    for story in stories[:settings.STORIES_PER_FEED]:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink,
        },)

    random.shuffle(storyjson)
    data = {'stories': storyjson}
    return HttpResponse(json.dumps(data, encoding='utf-8'),
                        content_type='application/json; charset=utf-8')
