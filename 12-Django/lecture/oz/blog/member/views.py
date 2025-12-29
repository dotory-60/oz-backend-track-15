from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.conf import settings # 현재 장고가 실행되고 있는 경로에서 settings를 가져옴 (권장)
from django.urls import reverse


# UserCreationForm : Django 기본 제공 회원가입 폼
# username 중복 검사, password1/password2 일치 검사, 비밀번호 정책 검사, User 객체 생성

# is_valid : 모든 필드 검증 실행

# save : 객체생성, 비밀번호 해시 처리, DB 저장

# POST method일 경우 form에 request.POST 객체를 UserCreationForm 클래스에 바인딩하여 객체로 생성 후, 사용자를 검증하여 참일 경우 데이터베이스에 저장합니다.
# GET method일 경우 form에 UserCreationForm 클래스에 빈 값을 넣어 인스턴스를 생성하고 렌더링합니다.
def signup(request):
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
    #     form = UserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(reverse('blog_list')) # config/urls.py에서 찾은 path name

    context = { 'form': form }
    return render(request, 'registration/login.html', context)