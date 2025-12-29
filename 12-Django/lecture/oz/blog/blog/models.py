from django.db import models

# Create your models here.

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
    # author
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateTimeField('updated_at', auto_now=True)

    def __str__(self):
        # 객체를 사람이 읽기 좋은 문자열로 표현 (Admin-page 에서도)
        return f'({self.get_category_display()}) {self.title[:10]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'