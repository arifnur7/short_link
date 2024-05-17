from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ShortenedURL, URLAccess
from .forms import URLForm
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

# Define the logger
# logger = logging.getLogger(__name__)

def testbug(request):
    return render(request,'testbug.html')

@login_required
def index(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_instance = form.save(commit=False)
            if not url_instance.short_url:
                url_instance.short_url = url_instance.generate_unique_short_url()
            url_instance.user = request.user # tambahan user login
            url_instance.save()
            return HttpResponse(f'Short URL is: {request.build_absolute_uri(url_instance.short_url)}')
    else:
        form = URLForm()
    return render(request, 'index.html', {'form': form})

def redirect_url(request, short_url):
    try:
        url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
        # track url access
        URLAccess.objects.create(shortened_url=url_instance)
        return redirect(url_instance.original_url)
    except Exception as e:
        logger.error(f"Error in redirecting short URL {short_url}: {str(e)}")
        return HttpResponse("An error occurred.", status=500)

def analytics(request, short_url):
    # ambil object url
    # check owner url == user
    # if(request.user.id == url.owner)
    try:
        url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
        accesses = URLAccess.objects.filter(shortened_url=url_instance)
        return render(request, 'analytics.html', {'url_instance': url_instance, 'accesses': accesses})
    except Exception as e:
        logger.error(f"Error in accessing analytics for short URL {short_url}: {str(e)}")
        return HttpResponse("An error occurred.", status=500)

#menambahkan user login
def register(request):
    print("register view called")
    # return HttpResponse("Test")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("Form is Valid")
            user = form.save()
            auth_login(request,user)
            return redirect('index')
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request,'register.html', {'form':form})

@login_required
def user_links(request):
    user_links = ShortenedURL.objects.filter(user=request.user)
    return render(request, 'shortener/user_links.html', {'user_links': user_links})

