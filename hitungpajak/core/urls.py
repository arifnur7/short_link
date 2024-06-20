from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from hitungan.views import Index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index.as_view(), name='index'),
    path('', include('hitungan.urls', namespace='hitungan'))
]
