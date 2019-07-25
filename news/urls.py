from django.conf.urls import url
from . import views

urlpatterns = [
    url('news/get', views.get_unclosed_posts),
    url('news/post', views.post_news),
]
