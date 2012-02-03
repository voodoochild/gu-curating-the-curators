import json
import random
from django.http import HttpResponse
from feeds.models import Story

def storify_dummy_data(request):
    storyjson = []
    stories = Story.objects.filter(latest = True, source = 'Storify')

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
    return HttpResponse(json.dumps(data),
                        content_type='application/json; charset=utf-8')
