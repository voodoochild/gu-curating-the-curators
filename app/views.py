from django.shortcuts import render
from feeds.models import Story

def dashboard(request):
    """Dashboard view."""
    stories = Story.objects.filter(latest = True)
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


    context = {
        'feeds': feeds
    }

    return render(request, 'app/dashboard.html', context)
