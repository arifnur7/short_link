from django.core.management.base import BaseCommand
from django.utils import timezone
from shortener.models import ShortenedURL
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete expired short links that have been expired for more than 1 month'

    def handle(self, *args, **kwargs):
        one_month_ago = timezone.now() - timedelta(days=30)
        expired_links = ShortenedURL.object.filter(status='expired', expired_at__1t = one_month_ago)
        count = expired_links.count()
        expired_links.delete()
        self.stdout.write(self.style.SUCCESS(f'Delete {count} expired short link'))