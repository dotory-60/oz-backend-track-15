from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at') # 정렬

    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )
        blogs = blogs.filter(content__icontains=q)

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    visits = int(request.COOKIES.get('visits', 0)) + 1
    request.session['count'] = request.session.get('count', 0) + 1
    context = {
        # 'blogs': blogs,
        'count': request.session['count'],
        'page_object': page_object,
    }
    response = render(request, 'blog_list.html', context)
    response.set_cookie('visits', visits)
    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)

@login_required()
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # DB에 반영되지 않음
        blog.author = request.user # AnonymousUser login 검사 객체
        blog.save()
        return redirect(reverse('blog_detail', kwargs = {'pk': blog.pk}))

    context = {'form': form}
    return render(request, 'blog_create.html', context)

@login_required()
def blog_update(request, pk):
    # Django가 제공하는 편의 함수
    # 객체가 없다면 None가 아니라 404 띄워라
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # if request.user != blog.author:
    #     raise Http404
    print(f'blog ============> {blog}')

    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        blog.save()
        return redirect(reverse('blog_detail', kwargs = {'pk': blog.pk}))

    context = {'form': form}
    return render(request, 'blog_update.html', context)

@login_required()
@require_http_methods(['POST'])
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http404

    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('blog_list'))