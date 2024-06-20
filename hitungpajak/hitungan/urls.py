from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "hitungan"
urlpatterns = [

    path("testbug/",views.testbug, name="testbug")
]
