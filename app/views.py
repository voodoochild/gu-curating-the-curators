from django.shortcuts import render

def dashboard(request):
    """Dashboard view."""
    return render(request, 'base.html', {})
