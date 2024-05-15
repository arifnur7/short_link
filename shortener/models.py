from django.db import models
from django.utils.crypto import get_random_string

class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = self.generate_unique_short_url()
        super().save(*args, **kwargs)

    def generate_unique_short_url(self):
        import string, random
        while True:
            short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            if not ShortenedURL.objects.filter(short_url=short_url).exists:
                return short_url


    def __str__(self):
        return f"{self.original_url} -> {self.short_url}"

class URLAccess(models.Model):
    shortened_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shortened URL: {self.shortened_url}, Accessed at: {self.accessed_at}"