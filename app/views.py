from django.shortcuts import render
from django.conf import settings
from feeds.models import Story

def dashboard(request):
    """Dashboard view."""
    stories = Story.objects.filter(latest=True, source='Storify').order_by('-timestamp')
    storyjson = []
    for story in stories[:settings.STORIES_PER_FEED]:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink
     },)
    feeds = []
    feeds.append({
        'identifier': 'Storify',
        'title': 'Storify &mdash; Popular',
        'stories': storyjson

    })

    tweetminster_stories = Story.objects.filter(latest=True, source='Tweetminster').order_by('-timestamp')
    tweetjson = []
    for tweetstory in tweetminster_stories[:settings.STORIES_PER_FEED]:
        tweetjson.append({
            'key': tweetstory.key,
            'title': tweetstory.title,
            'thumbnail': tweetstory.thumbnail,
            'permalink': tweetstory.permalink
        },)

    feeds.append({
        'identifier': 'Tweetminster',
        'title': 'Tweetminster &mdash; Latest',
        'stories': tweetjson
    })

    contentapi_stories = Story.objects.filter(latest=True, source='ContentAPI').order_by('-timestamp')
    contentapijson = []
    for contentapi_story in contentapi_stories[:settings.STORIES_PER_FEED]:
        contentapijson.append({
            'key': contentapi_story.key,
            'title': contentapi_story.title,
            'thumbnail': contentapi_story.thumbnail,
            'permalink': contentapi_story.permalink
        },)

    feeds.append({
        'identifier': 'ContentAPI',
        'title': 'Sport from The Guardian',
        'stories': contentapijson
    })

    return render(request, 'app/dashboard.html', {'feeds': feeds})
