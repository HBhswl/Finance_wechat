from django.conf.urls import url
from . import views

urlpatterns = [
    url('news/get', views.get_unclosed_posts),
    url('news/post', views.post_news),
    url('news/<int:post_id>/upload_image', views.upload_post_image),
]
