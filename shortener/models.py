from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import qrcode
from io import BytesIO
from django.core.files import File
import string
import random
from django.utils.crypto import get_random_string


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ACCOUNT_TYPE_CHOICES = [
        ('free', 'Free'),
        ('premium', 'Premium'),
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='free')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ShortenedURL(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    original_url = models.URLField()
    short_url = models.CharField(max_length=20, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    last_updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shortened_urls')

    def set_expiration_date(self):
        if self.user:
            if self.user.profile.account_type == 'premium':
                self.expires_at = timezone.now() + timedelta(365)
            elif self.user.profile.account_type == 'free':
                self.expires_at = timezone.now() + timedelta(90)
        else:
            self.expires_at = timezone.now() + timedelta(30)
        self.save()

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = self.generate_unique_short_url()
        if not self.expires_at:
            self.set_expiration_date()
        super().save(*args, **kwargs)

    def generate_unique_short_url(self):
        import string, random
        while True:
            short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if not ShortenedURL.objects.filter(short_url=short_url).exists:
                return short_url
    def generate_qr_code(self):
        qr= qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'http://127.0.0.1:8000/{self.short_url}')
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def __str__(self):
        return f"{self.original_url} -> {self.short_url}"

class URLAccess(models.Model):
    shortened_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shortened URL: {self.shortened_url}, Accessed at: {self.accessed_at}"