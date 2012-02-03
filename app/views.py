from django.shortcuts import render
from feeds.models import Story

def dashboard(request):
    """Dashboard view."""
    stories = Story.objects.filter(latest = True, source = 'Storify')
    storyjson = []
    for story in stories:
        storyjson.append({
            'key': story.key,
            'title': story.title,
            'thumbnail': story.thumbnail,
            'permalink': story.permalink
     },)
    feeds = []
    feeds.append({
        'title': 'Storify',
        'stories': storyjson

    })

    tweetminster_stories = Story.objects.filter(latest = True, source = 'Tweetminster')
    tweetjson = []
    for tweetstory in tweetminster_stories:
        tweetjson.append({
            'key': tweetstory.key,
            'title': tweetstory.title,
            'thumbnail': tweetstory.thumbnail,
            'permalink': tweetstory.permalink
        },)

    feeds.append({
        'title': 'Tweetminster',
        'stories': tweetjson

    })


    context = {
        'feeds': feeds
    }

    return render(request, 'app/dashboard.html', context)
