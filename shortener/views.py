from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ShortenedURL
from .forms import URLForm


def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_instance = form.save(commit=False)
            if not url_instance.short_url:
                url_instance.short_url = url_instance.generate_unique_short_url()
            url_instance.save()
            return HttpResponse(f'Short URL is: {request.build_absolute_uri(url_instance.short_url)}')
    else:
        form = URLForm()
    return render(request, 'index.html', {'form': form})

def redirect_url(request, short_url):
    url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
    # track url access
    URLAccess.objects.create(shortened_url=url_instance)
    return redirect(url_instance.original_url)

def analytics(request, short_url):
    url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
    accesses = URLAccess.objects.filter(shortened_url=url_instance)
    return render(request, 'analytics.html', {'url_instance': url_instance, 'accesses': accesses})
