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
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-links/', views.user_links, name='user_links'),
    path('qr/<str:short_url>/', views.qr_code, name='qr_code'),
    path('download-qr/<str:short_url>/', views.download_qr_code, name='download_qr_code'),
    path('reactivation/<str:short_url>/', views.reactivation, name='reactivation'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('<str:short_url>/', views.redirect_url, name='redirect_url'),
    path('favicon.ico/', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    path('testbug/',views.testbug, name='testbug'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
