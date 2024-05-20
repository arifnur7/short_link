from django import forms
from .models import ShortenedURL
import logging
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1','password2')

    def  __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class URLForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['original_url','short_url']
        widgets = {
            'short_url':forms.TextInput(attrs=
                                        {'placeholder':'Optional : Costum Short URL'})
        }

    forbidden_words = {'admin', 'root', 'support', 'help', 'login', 'register', 'logout', 'delete'}

    def clean_short_url(self):
        short_url = self.cleaned_data.get('short_url')
        if short_url:
            #cek bila custom URL sudah digunakan
            if ShortenedURL.objects.filter(short_url=short_url).exists():
                raise forms.ValidationError('This short URL is already taken.')
            #cek bila costum URL berisi kata yang dilarang
            if any(word in short_url.lower() for word in self.forbidden_words):
                raise forms.ValidationError('Costume URL contain Forbidden Words or is reserved.')
            #cek bila costum URL berisi selain alfanumeric
            if not short_url.isalnum():
                raise  forms.ValidationError('Costume Short URL can only contain alphanumeric characters.')
        return short_url
