from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from bookmark.models import Bookmark
from django.http import Http404

def bookmark_list(request):
    bookmarks = Bookmark.objects.all() # SELECT * FROM bookmark;
    context = { 'bookmarks': bookmarks }
    return render(request, 'bookmark_list.html', context)

def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404
    bookmark = get_object_or_404(Bookmark, pk=pk)
    context = {'bookmark': bookmark}
    return render(request, "bookmark_detail.html", context)

def bookmark_50(request):
    bookmarks = Bookmark.objects.filter(pk__gte=50)
    context = {'bookmarks': bookmarks}
    return render(request, 'bookmark_50.html', context)