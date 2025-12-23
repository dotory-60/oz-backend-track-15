"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import path

from bookmark import views

movie_list = [
    {
        "title": "Avatar",
        "director": "James Cameron",
        "audience": 280000000,
        "year": 2009
    },
    {
        "title": "Avengers: Endgame",
        "director": "Anthony Russo, Joe Russo",
        "audience": 270000000,
        "year": 2019
    },
    {
        "title": "Avatar: The Way of Water",
        "director": "James Cameron",
        "audience": 250000000,
        "year": 2022
    },
    {
        "title": "Titanic",
        "director": "James Cameron",
        "audience": 230000000,
        "year": 1997
    },
    {
        "title": "Star Wars: The Force Awakens",
        "director": "J.J. Abrams",
        "audience": 210000000,
        "year": 2015
    },
    {
        "title": "Avengers: Infinity War",
        "director": "Anthony Russo, Joe Russo",
        "audience": 200000000,
        "year": 2018
    },
    {
        "title": "Spider-Man: No Way Home",
        "director": "Jon Watts",
        "audience": 190000000,
        "year": 2021
    },
    {
        "title": "Jurassic World",
        "director": "Colin Trevorrow",
        "audience": 185000000,
        "year": 2015
    },
    {
        "title": "The Lion King",
        "director": "Jon Favreau",
        "audience": 180000000,
        "year": 2019
    },
    {
        "title": "The Avengers",
        "director": "Joss Whedon",
        "audience": 175000000,
        "year": 2012
    },
    {
        "title": "Furious 7",
        "director": "James Wan",
        "audience": 170000000,
        "year": 2015
    },
    {
        "title": "Frozen II",
        "director": "Chris Buck, Jennifer Lee",
        "audience": 165000000,
        "year": 2019
    },
    {
        "title": "Avengers: Age of Ultron",
        "director": "Joss Whedon",
        "audience": 160000000,
        "year": 2015
    },
    {
        "title": "Black Panther",
        "director": "Ryan Coogler",
        "audience": 155000000,
        "year": 2018
    },
    {
        "title": "Harry Potter and the Deathly Hallows – Part 2",
        "director": "David Yates",
        "audience": 150000000,
        "year": 2011
    },
    {
        "title": "Star Wars: The Last Jedi",
        "director": "Rian Johnson",
        "audience": 145000000,
        "year": 2017
    },
    {
        "title": "Jurassic World: Fallen Kingdom",
        "director": "J.A. Bayona",
        "audience": 140000000,
        "year": 2018
    },
    {
        "title": "Frozen",
        "director": "Chris Buck, Jennifer Lee",
        "audience": 135000000,
        "year": 2013
    },
    {
        "title": "Beauty and the Beast",
        "director": "Bill Condon",
        "audience": 130000000,
        "year": 2017
    },
    {
        "title": "Incredibles 2",
        "director": "Brad Bird",
        "audience": 125000000,
        "year": 2018
    }
]
book_list = [
    {
        "title": "불편한 편의점",
        "author": "김호연",
        "audience": 2500000,
        "year": 2021
    },
    {
        "title": "아몬드",
        "author": "손원평",
        "audience": 2000000,
        "year": 2017
    },
    {
        "title": "달러구트 꿈 백화점",
        "author": "이미예",
        "audience": 2000000,
        "year": 2020
    },
    {
        "title": "82년생 김지영",
        "author": "조남주",
        "audience": 3000000,
        "year": 2016
    },
    {
        "title": "미움받을 용기",
        "author": "기시미 이치로, 고가 후미타케",
        "audience": 3500000,
        "year": 2014
    },
    {
        "title": "죽고 싶지만 떡볶이는 먹고 싶어",
        "author": "백세희",
        "audience": 1500000,
        "year": 2018
    },
    {
        "title": "나미야 잡화점의 기적",
        "author": "히가시노 게이고",
        "audience": 3000000,
        "year": 2012
    },
    {
        "title": "채식주의자",
        "author": "한강",
        "audience": 1000000,
        "year": 2007
    },
    {
        "title": "데미안 (한국어판)",
        "author": "헤르만 헤세",
        "audience": 4000000,
        "year": 1919
    },
    {
        "title": "사피엔스 (한국어판)",
        "author": "유발 하라리",
        "audience": 2500000,
        "year": 2015
    },
    {
        "title": "원씽",
        "author": "게리 켈러, 제이 파파산",
        "audience": 2000000,
        "year": 2013
    },
    {
        "title": "부의 추월차선",
        "author": "엠제이 드마코",
        "audience": 1500000,
        "year": 2012
    },
    {
        "title": "역행자",
        "author": "자청",
        "audience": 1000000,
        "year": 2022
    },
    {
        "title": "돈의 심리학",
        "author": "모건 하우절",
        "audience": 1200000,
        "year": 2020
    },
    {
        "title": "세이노의 가르침",
        "author": "세이노",
        "audience": 3000000,
        "year": 2023
    },
    {
        "title": "하얼빈",
        "author": "김훈",
        "audience": 800000,
        "year": 2022
    },
    {
        "title": "불변의 법칙",
        "author": "모건 하우절",
        "audience": 900000,
        "year": 2023
    },
    {
        "title": "참을 수 없는 존재의 가벼움 (한국어판)",
        "author": "밀란 쿤데라",
        "audience": 1500000,
        "year": 1984
    },
    {
        "title": "자존감 수업",
        "author": "윤홍균",
        "audience": 2000000,
        "year": 2016
    },
    {
        "title": "나는 나로 살기로 했다",
        "author": "김수현",
        "audience": 1800000,
        "year": 2016
    }
]

def index(request):
    return HttpResponse('<h1>Hello</h1>')

def books(request):
    return render(request, 'books.html', {'book_list': book_list})

def book(request, idx):
    if idx > len(book_list):
        raise Http404
    book_data = book_list[idx]
    return render(request, 'book.html', {'book_data': book_data})

def language(request, lang):
    return HttpResponse(f'language is {lang}')

def movies(request):
    # render을 안 하는 경우
    # titles_html = [f'<h3><a href="/movie/{index}">{movie['title']}</a></h3><br>' for index, movie in enumerate(movie_list)]
    # return HttpResponse(titles_html)

    # render을 하는 경우
    return render(request, 'movies.html', {'movie_list': movie_list})

def movie(request, idx):
    # 존재하지 않는 영화 인덱스일 경우 404 에러 반환
    if idx > len(movie_list) - 1:
        raise Http404
    movie_data = movie_list[idx]
    return render(request, 'movie.html', {'movie': movie_data})

def gugudan(request, dan):
    results = [dan * i for i in range(1, 10)] # dan * 1~9
    context = { "dan": dan, "results": results }
    return render(request, 'gugudan.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookmark/', views.bookmark_list),
    path('bookmark/<int:pk>', views.bookmark_detail),

    # path('', index),
    # path('book/all', books),
    # path('book/<int:idx>', book),
    # path('lang/<str:lang>', language), # str은 특별한 경우에만 사용
    # path('movie/all', movies),
    # path('movie/<int:idx>', movie),
    # path('gugudan/<int:dan>', gugudan),
]