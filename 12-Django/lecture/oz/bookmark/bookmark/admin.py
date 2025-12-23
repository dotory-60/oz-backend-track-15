from django.contrib import admin

from bookmark.models import Bookmark

# Register your models here.

@admin.register(Bookmark)                   # Bookmark 모델을 Admin 사이트에 노출시킴
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']    # 관리자 목록 화면에 보여줄 컬럼
    list_display_links = ['name']           # 링크화하는 컬럼
    list_filter = ['name', 'url']

# @admin.register(Bookmark)를 없애고 아래 방법을 사용할 수도 있음
# admin.site.register(Bookmark, BookmarkAdmin) # Bookmark 모델을 Admin 사이트에 노출시킴