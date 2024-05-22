from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics/<str:short_url>/', views.analytics, name='analytics'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-links/', views.user_links, name='user_links'),
    path('reactivation/<str:short_url>/', views.reactivation, name='reactivation'),
    path('<str:short_url>/', views.redirect_url, name='redirect_url'),
    path('favicon.ico/', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    path('testbug/',views.testbug, name='testbug'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
