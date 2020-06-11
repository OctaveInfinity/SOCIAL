from django.contrib import admin

from .models import Profile


# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    list_display_links = ['id']
    list_per_page = 25


admin.site.register(Profile, ProfileAdmin)
