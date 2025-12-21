from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect

# from config import settings # 폴더 경로 settings.py 가져온거, 파일명이 달라지면 오류가 날 수 있음
from django.conf import settings # 장고가 실행되고 있는 파일에서? 오류가 나지 않음
from django.urls import reverse


def sign_up(request):
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')
    #
    # print(username)
    # print(password1)
    # print(password2)

    # username 중복확인작업
    # password가 맞는지, password 정책과 일치한지 (대소문자)
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/accounts/login/')
    # else:
    #     form = UserCreationForm() # 회원가입관리 form, django 내장

    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST or None)
        if form.is_valid():
            django_login(request, form.get_user())

            next = request.GET.get('next')
            if next:
                return redirect(next)

            return redirect(reverse('blog:list')) # name을 찾아감
    else:
        form = AuthenticationForm(request)

    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)