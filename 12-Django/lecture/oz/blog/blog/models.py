from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# title, content, author, created_at, updated_at, category, image, tag

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travel', '여행'),
        ('study', '공부'),
        ('dev', '개발'),
        ('daily', '일상'),
        ('review', '리뷰'),
        ('food', '음식'),
        ('health', '운동'),
        ('career', '진로'),
        ('etc', '기타'),
    )

    category = models.CharField('category', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField('title', max_length=100)
    content = models.TextField('content')
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 같이 삭제
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제가 불가능함 (유저를 삭제하려고 할 때 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL => Null을 넣음 => 유저 삭제시 블로그의 author가 null이 됨

    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    def __str__(self):
        # 객체를 사람이 읽기 좋은 문자열로 표현 (Admin-page 에서도)
        return f'({self.get_category_display()}) {self.title[:10]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'