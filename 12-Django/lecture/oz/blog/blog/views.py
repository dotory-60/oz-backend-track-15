from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from blog.form import BlogForm
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at') # - : desc
    visits = int(request.COOKIES.get('visits', 0)) + 1
    request.session['count'] = request.session.get('count', 0) + 1
    context = {
        'blogs': blogs,
        'count': request.session['count']
    }
    response = render(request, 'blog/blog_list.html', context)
    response.set_cookie('visits', visits)
    return response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk) # 단일 객체 조회
    context = {
        'blog': blog
    }
    return render(request, 'blog/blog_detail.html', context)

@login_required()
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # DB call x, model만
        blog.author = request.user
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))

    form = BlogForm()
    context = {'form': form}
    return render(request, 'blog/blog_create.html', context)