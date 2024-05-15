from django import forms
from .models import ShortenedURL

class URLForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['original_url','short_url']
        widgets = {
            'short_url':forms.TextInput(attrs=
                                        {'placeholder':'Optional : Costum Short URL'})
        }

    def clean_short_url(self):
        short_url = self.cleaned_data.get('short_url')
        if short_url:
            if ShortenedURL.objects.filter(short_url=short_url).exists():
                raise forms.ValidationError('This short URL is already taken.')
            if not short_url.isalnum():
                raise  forms.ValidationError('Costume Short URL can only contain alphanumeric characters.')
        return short_url
