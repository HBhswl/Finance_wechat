from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url('news/get', views.get_unclosed_posts),
    url('news/post', views.post_news),
    path('news/upload_image/<int:post_id>', views.upload_post_image),
]
