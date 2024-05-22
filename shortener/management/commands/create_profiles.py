# shortener/management/commands/create_profiles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shortener.models import Profile

class Command(BaseCommand):
    help = 'Create missing profile objects for users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Created profile for user {user.username}'))
        self.stdout.write(self.style.SUCCESS('All missing profiles have been created.'))
