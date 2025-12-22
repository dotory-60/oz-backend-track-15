## 🚀 Django Practice – Day 1
Django 입문 1일차 학습 내용을 정리한 실습 프로젝트입니다.
URL 라우팅부터 View–Template 연결까지 Django의 기본 요청 흐름을
직접 구현하며 이해하는 것을 목표로 합니다.

## 📌 학습 목표
- Django 프로젝트 기본 구조 이해 
- urls.py를 이용한 URL 라우팅 
- 함수 기반 View (Function-Based View) 작성 
- render()를 사용한 Template 렌더링 
- Django Template Language (DTL) 기본 문법 학습 
- 템플릿 필터 (humanize, intcomma) 활용 
- 예외 처리 (Http404)
- View와 Template의 역할 분리 개념 이해

## ⚙️ 사용 기술
- Python 3 
- Django 5.0 
- SQLite3 
- Django Template Language (DTL)

## ✖️ 구구단 페이지 (Django 1일차 과제)
```
/gugudan/<int:dan>
```
URL로 전달받은 dan 값을 기준으로 구구단 출력  계산 로직은 View에서 처리  Template은 출력만 담당

Template: gugudan.html