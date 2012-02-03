from django.shortcuts import render

def dashboard(request):
    """Dashboard view."""
    feeds = []
    feeds.append({
        'title': 'Storify',
        'stories': [
            {
                'key': 'first_item',
                'title': 'First item',
                'thumbnail': 'http://p.twimg.com/AkmwZP8CQAI8vXL.jpg',
                'permalink': 'http://storify.com/curious_scribe/egyptian-football-riots'
            },
            {
                'key': 'second_item',
                'title': 'Second item',
                'thumbnail': 'http://p.twimg.com/AkmwZP8CQAI8vXL.jpg',
                'permalink': 'http://storify.com/curious_scribe/egyptian-football-riots'
            },
            {
                'key': 'third_item',
                'title': 'Third item',
                'thumbnail': 'http://p.twimg.com/AkmwZP8CQAI8vXL.jpg',
                'permalink': 'http://storify.com/curious_scribe/egyptian-football-riots'
            },
            {
                'key': 'fourth_item',
                'title': 'Fourth item',
                'thumbnail': 'http://p.twimg.com/AkmwZP8CQAI8vXL.jpg',
                'permalink': 'http://storify.com/curious_scribe/egyptian-football-riots'
            },
            {
                'key': 'fifth_item',
                'title': 'Fifth item',
                'thumbnail': 'http://p.twimg.com/AkmwZP8CQAI8vXL.jpg',
                'permalink': 'http://storify.com/curious_scribe/egyptian-football-riots'
            }
        ]
    })

    context = {
        'feeds': feeds
    }

    return render(request, 'app/dashboard.html', context)
