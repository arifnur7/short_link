# Example of displaying analytics in a separate view
from django.shortcuts import render
from .models import ShortenedURL

def analytics(request, short_url):
    url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
    accesses = URLAccess.objects.filter(shortened_url=url_instance)
    return render(request, 'analytics.html', {'url_instance': url_instance, 'accesses': accesses})
