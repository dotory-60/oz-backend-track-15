from django.contrib import admin

from bookmark.models import Bookmark

# Register your models here.

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'created_at', 'updated_at']
    list_display_links = ['name', 'url']
    list_filter = ['name', 'url']

# admin.site.register(Bookmark, BookmarkAdmin)