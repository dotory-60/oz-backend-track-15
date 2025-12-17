from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지'),
    )

    # Field
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    content = models.CharField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제 불가능 (유저를 삭제하려고할때 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL => 널값을 넣습니다 => 유저 삭제시 블로그의 authro가 null이 됨

    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    # Django 모델 객체를 문자열로 표현할 때 어떤 문장을 보여줄지 결정하는 특별한 메서드
    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    # 관리자 화면에서 보이는 이름
    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'