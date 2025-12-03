from django.contrib import admin
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import path
from bookmark import views

# Movie
movie_list = [
    {"title": "기생충", "director": "봉준호"},
    {"title": "올드보이", "director": "박찬욱"},
    {"title": "악마를 보았다", "director": "김지운"},
    {"title": "인터스텔라", "director": "크리스토퍼 놀란"},
    {"title": "다크 나이트", "director": "크리스토퍼 놀란"},
    {"title": "라라랜드", "director": "데이미언 셔젤"},
    {"title": "위플래쉬", "director": "데이미언 셔젤"},
    {"title": "그녀", "director": "스파이크 존즈"},
    {"title": "매트릭스", "director": "워쇼스키 자매"},
    {"title": "아바타", "director": "제임스 카메론"}
]

def index(request):
    return HttpResponse("<h1>Hello world</h1>")

def book_list(request):
    book_text = ""
    for i in range(0, 10):
        book_text += f"book {i} <br>"
    return HttpResponse(book_text)

def book(request, book_id):
    book_text = f"book {book_id}번 페이지입니다"
    return HttpResponse(book_text)

def language(request, lang):
    return HttpResponse(f"<h1>{lang} 언어 페이지입니다.</h1>")

def python(request):
    return HttpResponse("python 페이지입니다.")

def movies(request):
    movie_titles = [
            f'<a href="/movie/{idx}/">{movie["title"]}</a>'
            for idx, movie
            in enumerate(movie_list)
        ]

    print(f"<br>movie_titles : {movie_titles}")

    # 위 리스트 내포(list comprehension)와 동일한 기능을 한다
    # movie_titles = []
    # for movie in movie_list:
    #     movie_titles.append(movie['title'])

    response_text = '<br>'.join(movie_titles)
    print(f"response_text : {response_text}")

    # for idx, title in enumerate(movie_titles):
    #     response_text += f'<a href="/movie/{idx}/">{title}</a><br>'
    return HttpResponse(response_text)

def movie_detail(request, index):
    # "사용자의 입력을 믿지마라"
    # 현재 movie_list에 10개의 데이터가 들어가있기 때문에 10 초과 값은 예외처리해야 한다.
    if index > len(movie_list)-1:
        raise Http404

    movie = movie_list[index-1] # 사용자 편의를 위해 -1 사용함

    response_text = f"<h1>{movie["title"]}</h1> <p>감독: {movie["director"]}</p>"
    return HttpResponse(response_text)

def movies_html(request):
    return render(request,"movies.html",{"movie_list": movie_list})

def movie_detail_html(request, index):
    if index > len(movie_list):
        raise Http404

    movie = movie_list[index-1]
    context = {
        "movie": movie,
        "index": index
    }
    return render(request, "movie.html", {"context": context})

# Gugudan
def gugudan(request, index):
    if index < 1:
        raise Http404

    gugudan = []

    for n in range(1, 10, 1):
        gugudan.append(f"{index} * {n} = {index * n}")
        print(f"{index} 단 : {index} * {n} = {index * n}")

    print(gugudan)
    context = {
        "gugudan": gugudan,
        "index": index
    }
    return render(request, "gugudan.html", {"context": context})

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name='index'),
    # path('book_list', book_list, name='book_list'),
    # path('book_list/<int:book_id>', book, name='book'),
    # path('language/<str:lang>', language, name="language"),
    #
    # # 위에 있는 route로 인해 language/python이 무시됨
    # # 해결방법: 코드상 language/python 라우터를 language/<str:lang> 보다 올림
    # # 그럼 language/<str:lang>를 만나기 전에 language/python를 만나서 괜찮음
    # # 그런데 보통 argument 타입으로 string를 사용하지 않고 사용해도 조심해야 함!
    # # 위와 같은 상황이 일어날 수 있기 때문에!!!
    # path('language/python', python, name="python"),
    #
    # path('movies', movies, name="movies"),
    # path('movie_detail/<int:index>', movie_detail, name="movie_detail"),
    #
    # # Render
    # path('movies_html/', movies_html, name="movies_html"),
    # path('movie_detail_html/<int:index>', movie_detail_html, name="movie_detail_html"),
    # path("gugudan/<int:index>", gugudan, name="gugudan"),

    # bookmark list
    path("bookmark/", views.bookmark_list),
    path('bookmark/<int:pk>', views.bookmark_detail),
    path("bookmark_50/", views.bookmark_50),
]
