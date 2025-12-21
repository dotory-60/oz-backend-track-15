from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include
from django.views import View
from django.views.generic import TemplateView, RedirectView

from blog import views as views, cb_views
from member import views as member_views

# class AboutView(TemplateView):
#     template_name = 'about.html'
#
# class TestView(View):
#     def get(self, request):
#         return render(request, 'test_get.html')
#
#     def post(self, request):
#         return render(request, 'test_post.html')
#
# def test_view(request):
#     if request.method == "POST":
#         ...
#     else:
#         ...

urlpatterns = [
    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),
    path('admin/', admin.site.urls),
    # Auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

# CBV Blog
#     path('', cb_views.BlogListView.as_view(), name='blog_list'),
#     path('<int:pk>', cb_views.BlogDetailView.as_view(), name='blog_detail'),
#     path('create', cb_views.BlogCreateView.as_view(), name='blog_create'),
#     path('<int:pk>/update', cb_views.BlogUpdateView.as_view(), name='blog_update'),
#     path('<int:pk>/delete', cb_views.BlogDeleteView.as_view(), name='blog_delete'),

    # FBV Blog


    # ??
    # path('about/', TemplateView.as_view(template_name="about.html"), name="about"),
    # path('about/', AboutView.as_view(), name='about'),
    # path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'), # 추천!
    # path('redirect2/', lambda req: redirect('about')),
    # path('test/', TestView.as_view(), name='test')

    #

]