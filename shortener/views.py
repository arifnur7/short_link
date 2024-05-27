from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ShortenedURL, URLAccess
from .forms import URLForm
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm
from django.utils import timezone
import qrcode
from io import BytesIO
import base64


# Define the logger
logger = logging.getLogger(__name__)

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
            url_instance.set_expiration_date() # tambahan untuk expired short link
            url_instance.save()
            # qr_code = url_instance.generate_qr_code()
            qr_code_img = url_instance.generate_qr_code() # tambahan untuk menampilkan QR Code
            qr_code_base64 = base64.b64encode(qr_code_img.read()).decode('utf-8')
            return render(request,'index.html',{'form':form, 'url_instance':url_instance, 'qr_code':qr_code_base64})
            # return HttpResponse(f'Short URL is: {request.build_absolute_uri(url_instance.short_url)}')
    else:
        form = URLForm()
    return render(request, 'index.html', {'form': form})

# function membuat QR CODE
def qr_code(request, short_url):
    url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(request.build_absolute_uri(f'/{short_url}'))
    qr.make(fit=True)

    img=qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return HttpResponse(buffer,content_type="image/png")

# function untuk mendownload QR CODE
def download_qr_code(request, short_url):
    url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
    qr= qrcode.QRCode(
        version=1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(request.build_absolute_uri(f'/{short_url}'))
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = f'attachment; filename="{short_url}.png"'
    return response

def redirect_url(request, short_url):
    try:
        url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
        #menambahkan expired time short link
        if url_instance.expiration_date and timezone.now() > url_instance.expiration_date:
            url_instance.delete() # menghapus link expired untuk digunakan kembali
            return HttpResponse("This short link has expired.", status =410)
        # track url access
        URLAccess.objects.create(shortened_url=url_instance)
        return redirect(url_instance.original_url)
    except Exception as e:
        logger.error(f"Error in redirecting short URL {short_url}: {str(e)}")
        return HttpResponse("An error occurred.", status=500)
@login_required()
def analytics(request, short_url):
    # ambil object url
    # check owner url == user
    # if(request.user.id == url.owner)
    try:
        url_instance = get_object_or_404(ShortenedURL, short_url=short_url)
        # cek apakah login user adalah pemilik link
        if not (request.user.is_superuser or url_instance.user == request.user):
            return HttpResponseForbidden("You do not have permission to view this analytics page.")

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
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print("Form is Valid")
            user = form.save()
            auth_login(request,user)
            return redirect('index')
        else:
            print("Form is invalid")
            print(form.errors)
    else:
        form = RegisterUserForm()
    return render(request,'register.html', {'form':form})

@login_required
def user_links(request):
    user_links = ShortenedURL.objects.filter(user=request.user)
    print(user_links)
    qr_codes = {
        link.short_url: base64.b64encode(link.generate_qr_code().read()).decode('utf-8') for link in user_links}
    print(qr_codes)
    print(qr_codes.keys())
    print(qr_codes['aurora2'])
    return render(request, 'user_links.html', {'user_links': user_links, 'qr_codes':qr_codes})


@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def reactivation(request, short_url):
    url_instance = get_object_or_404(ShortenedURL, short_url=short_url, user=request.user)
    if request.method == 'POST':
        url_instance.set_expiration_date()
        url_instance.status = 'active'
        url_instance.save()
        return redirect('user_links')
    return render(request, 'reactivation.html', {'url_instance': url_instance})