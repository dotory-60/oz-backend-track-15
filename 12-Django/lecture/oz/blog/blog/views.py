from django.contrib.auth.decorators import login_required
from django.http import Http404
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


# is_authenticated : Django User Model에서 기본적으로 제공하는 속성
@login_required()
def blog_create(request):
    form = BlogForm(request.POST or None) # 데이터 규격화
    if form.is_valid(): # 검증 통과한 데이터 정제
        blog = form.save(commit=False) # DB call x, model만
        blog.author = request.user
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk})) # kwargs : 주소창 pk라는 자리에, 방금 저장한 blog객체의 pk 값을 넣어라

    # GET일 경우
    context = {'form': form}
    return render(request, 'blog/blog_create.html', context)

@login_required()
def blog_update(request, pk):
    # if request.user != blog.author:
    #     raise Http404
    blog = get_object_or_404(Blog, pk=pk, author=request.user) # pk가 같은지, author이 request.user인지 조건이 2개 들어간거다.
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        # blog = form.save(commit=False) # DB call x, model만
        # blog.author = request.user
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))
    context = {'blog': blog, 'form': form,}
    return render(request, 'blog/blog_update.html', context)