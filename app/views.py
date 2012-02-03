from django.shortcuts import render
from feeds.models import Story

def dashboard(request):
    """Dashboard view."""
    storify = Story.objects.filter(source='Storify').order_by('-timestamp').distinct()

    context = {
        'feeds': {
            'storify': storify
        }
    }

    return render(request, 'app/dashboard.html', context)
