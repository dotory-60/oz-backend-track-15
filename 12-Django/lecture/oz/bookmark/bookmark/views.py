from django.shortcuts import render, get_object_or_404

from bookmark.models import Bookmark


def bookmark_list(request):
    bookmarks = Bookmark.objects.all() # SELECT * FROM bookmark;
    context = { 'bookmarks': bookmarks }
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk) # SELECT * FROM bookmark WHERE id = pk; 실패하면 404
    context = { 'bookmark': bookmark }
    return render(request, 'bookmark_detail.html', context)