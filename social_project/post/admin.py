from django.contrib import admin

from .models import Post


# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'posted')
    list_display_links = ['id', 'title']
    list_filter = ['owner']
    list_per_page = 25


admin.site.register(Post, PostAdmin)
