# admin.py
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type')
    list_filter = ('account_type',)
    search_fields = ('user__username', 'user__email')
    fields = ('user', 'account_type')
    readonly_fields = ('user',)

admin.site.register(Profile, ProfileAdmin)
