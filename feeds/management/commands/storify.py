from django.core.management.base import BaseCommand, CommandError
from feeds.models import Story

class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        """Connect to the Storify API, retrieve popular stories, and store."""
        pass
