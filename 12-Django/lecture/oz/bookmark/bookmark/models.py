from django.db import models

# Create your models here.

# Model: DB Table, Field: DB Column

class Bookmark(models.Model):
    name = models.CharField('이름', max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일시', auto_now_add=True) # auto_now_add : 처음 생성할 때만
    updated_at = models.DateTimeField('수정일시', auto_now=True)     # auto_now : 저장할 때마다

    # 모델 객체를 문자열로 표현할 때 호출됨
    # Admin 화면, ForeignKey 선택 목록 등에서 표시될 값
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '북마크'
        verbose_name_plural = '북마크 목록'

    # makemigrations
    # → migrations 폴더에 DB 변경 내역을 기록한 migration 파일을 생성
    # → 실제 DB에는 아직 아무 영향 없음

    # migrate
    # → migrations 폴더에 있는 migration 파일들을 읽어서
    # → 실제 DB에 구조 변경을 적용